import glob
import time
import rclpy
import serial
import serial.tools.list_ports
from rclpy.node import Node
from geometry_msgs.msg import Twist
from timeit import default_timer
from std_msgs.msg import String
from agrobot_msgs.msg import CropTypeLocation
from agrobot_msgs.srv import ArmPosition


'''
The movement controller has timing issues with nodes not detecting crops quickly enough. This can be resolved by writing more efficient nodes that use rclpy.spin_once(node) instead of timers to process subscriber and service callbacks.
This function updates one callback if it has received a message, making the logic cleaner and easier to work with.
Alternatively, a stronger computer or multiple computers using the supported ROS2 networking could be used 
'''

class MovementControllerNode(Node):

    lock_detected_crop = False # Locks detected crop data so that the position is not updated unexpectedly
    detected_crop = None # Holds object which is currently being collected
    detected_marker = False # Holds whether a marker is currently detected

    calibration_time = 13 # Time to wait before starting (seconds)
    
    movement_speed = 0.6
    full_speed_braking_force = -0.4
    full_speed_braking_time = 0.3

    adjustment_movement_speed = 0.4
    adjustment_speed_braking_force = -0.2
    adjustment_speed_braking_time = 0.2

    target_crop_y = 20 # Position at which the robot should stop (expected crop location in pixels)
    max_crop_y_difference = 5 # Maximum crop position difference to stop at in pixels
    adjustment_count_target = 1 # Adjustment iterations to perform
    adjustment_count = 0 # Current adjustment iteration
    harvesting_blind_time = 2.0 # Time to wait before detecting crops again after attempting to collect (seconds)

    crops_collected = 0 # Number of crops collected
    delivery_cycle_count = 0 # Number of delivery cycles completed
    delivery_open_command = "!1O,3O\n" # Command to open delivery boxes
    delivery_close_command = "!1C,3C\n" # Command to close delivery boxes
    delivery_marker_blind_time = 3.0 # Time to wait before detecting marker again after stopping (seconds)

    moving_slow = False
    last_command_sent = None

    serial_com = None

    def __init__(self):

        # Set up node
        super().__init__('movement_controller_node')

        self.node = rclpy.create_node('movement_controller_node')

        # Set up publishers
        self.cmd_vel_pub = self.create_publisher(Twist, "/cmd_vel", 1) # Sends vel commands to the odrive controller
        self.harvested_crop_pub = self.create_publisher(CropTypeLocation, "harvested_crop", 1) # Sends harvested crop data to the vision processing node

        # Set up services
        self.arm_cmd_srv = self.create_client(ArmPosition, "arm_target_position") # Sends arm commands to the arm controller

        # Set up subscribers
        self.create_subscription(CropTypeLocation, 'detected_crop', self.__update_crop, 1)
        self.create_subscription(String, 'detected_marker', self.__update_marker, 1)
        
        # Set up logger
        self.logger = self.get_logger()
        self.logger.info("Start movement controller")

        # Set up communication port to Arduino
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            if "Arduino" in p.manufacturer:
                self.serial_com = serial.Serial(p.device, 9600, write_timeout=0.5)  
                self.logger.info("Connected to arduino")
                break

        if self.serial_com == None:
            self.logger.error("Arduino not connected")

        # Set up loop timers
        # These are necessary to replace while loops
        # Because while loops cause the node to not update subscriber callbacks
        self.harvest_timer = self.create_timer(0.1, self.harvest_loop)
        self.harvest_timer.cancel()
        self.adjustment_timer = self.create_timer(0.4, self.adjust_position)
        self.adjustment_timer.cancel()
        self.delivery_timer = self.create_timer(0.1, self.deliver_loop)
        self.delivery_timer.cancel()

        self.start() # Start movement script

    def __update_crop(self, object):

        if(not self.lock_detected_crop):
            if object.crop_type == "":
                self.detected_crop = None
            else:
                self.detected_crop = object
                self.logger.info("Crop location: " + str(self.detected_crop.crop_x) + ", " + str(self.detected_crop.crop_y))

    def __update_marker(self, marker):
        self.detected_marker = True

    def start(self):

        # Wait for direct drive motors to calibrate
        # TODO: Replace this with some system to start this node when odrive calibration is finished
        self.wait(self.calibration_time)

        self.logger.info("Start harvesting")
        self.start_harvesting()

        #
        # TODO: Write code to make robot harvest the planter boxes in column two
        #

        # Position self to drive over column two
        # self.start_harvesting()
        # Position self to deliver plants
        # self.start_delivering()

    def start_harvesting(self):
        self.detected_crop = None # Remove last detected crop
        self.harvest_timer.reset()

    def harvest_loop(self):
        if not self.moving_slow:
            # Keep moving forward
            self.execute_movement_command(self.movement_speed)

            if self.crops_collected % 3 == 0: # If a whole row has been harvested
                self.wait(self.harvesting_blind_time) # Keep driving, without detecting crops

        # If there is no object detected, keep driving
        if self.detected_crop != None:
            self.logger.info("Detected crop, slowing down")
            self.driving_slow = True
            # Slow down
            self.execute_movement_command(self.adjustment_movement_speed)

            if(self.detected_crop.crop_y <= self.target_crop_y):
                self.harvest_timer.cancel()
                self.logger.info("Crop in position, stopping")

                # self.execute_movement_command(self.adjustment_speed_braking_force)
                # self.wait(self.adjustment_speed_braking_time)

                self.execute_movement_command(0.0)


                # self.wait(0.2)
                # if abs(self.detected_crop.crop_y - self.target_crop_y) > self.max_crop_y_difference:
                #     self.adjust_position()

                # Call gripper service and wait for future to be complete
                self.logger.info("Calling gripper service")
                request = ArmPosition.Request()
                response = ArmPosition.Response()
                request.crop_x = self.detected_crop.crop_x
                request.crop_y = self.detected_crop.crop_y
                request.crop_type = self.detected_crop.crop_type
                self.future = self.arm_cmd_srv.call_async(request=request)

                result = None
                while rclpy.ok():
                    rclpy.spin_once(node=self.node)
                    if self.future.done():
                        result = self.future.result()
                        break

                if self.future.result != None:
                    self.logger.info("Crop successfully harvested")
                else:
                    self.logger.warning("An error occured during crop collection")

                self.logger.info("Harvested crops: " + str(self.crops_collected) + "/18")
                self.harvested_crop_pub.publish(self.detected_crop)
                self.crops_collected += 1
                self.driving_slow = False

                if self.crops_collected == 18:
                    self.logger.info("All crops collected")
                    self.harvest_timer.cancel()
                    self.delivery_timer.reset()
                else:
                    self.harvest_timer.reset()

    def adjust_position(self):

        self.adjustment_timer.cancel()

        self.logger.info("Adjusting position")
        crop_y = self.detected_crop.crop_y
        target_diff = abs(crop_y - self.target_crop_y)

        # Calculate multiplier to incrementally decrease movement speed
        multiplier =  1 - (self.adjustment_count / self.adjustment_count_target)
        self.logger.info("Multiplier: " + str(multiplier))
        
        # Calculate time to move
        target_time = (abs(target_diff)) / 35 # Convert crop distance to time to move

        self.logger.info("Target position difference: " + str(target_diff))
        self.logger.info("Target time: " + str(target_time))
        self.logger.info("Iteration: " + str(self.adjustment_count))

        if(target_time < 0.3): # If target position is close enough
            return

        # Determine direction to move
        if(crop_y > self.target_crop_y):
            self.execute_movement_command(self.adjustment_movement_speed * multiplier) # Adjust forwards
        else:
            self.execute_movement_command(-self.adjustment_movement_speed * multiplier) # Adjust backwards

        # Wait for calculated time
        self.wait(target_time)
        
        # Stop
        self.execute_movement_command(0.0)
        self.wait(self.adjustment_speed_braking_time * multiplier)

        self.adjustment_count += 1
        if self.adjustment_count < self.adjustment_count_target: # If not done adjusting
            # Keep adjusting
            self.adjustment_timer.reset()
        else:
            # Done adjusting
            self.logger.info("Done adjusting")
            
    def deliver_loop(self):
        if self.detected_marker:
            self.harvest_timer.cancel()
            self.delivery_timer.cancel()

            self.logger.info("Detected marker, stopping")

            # Apply braking force
            self.execute_movement_command(self.full_speed_braking_force)
            self.wait(self.full_speed_braking_time)
            
            # Stop
            self.execute_movement_command(0.0)

            self.logger.info("Opening boxes")
            self.execute_collection_bucket_command(self.delivery_open_command)

            self.logger.info("Closing boxes")
            self.execute_collection_bucket_command(self.delivery_close_command)

            self.execute_movement_command(self.adjustment_movement_speed)
            self.wait(self.delivery_marker_blind_time)

            self.detected_marker = False

            self.delivery_cycle_count += 1
            if self.delivery_cycle_count == 2:
                self.delivery_timer.cancel()
                return
            else:
                self.delivery_open_command = "!2O,4O\n"
                self.delivery_close_command = "!2C,4C\n"
                self.delivery_timer.reset()
                self.execute_movement_command(self.adjustment_movement_speed)

    def execute_movement_command(self, speed):
        if self.last_command_sent != speed:
            self.logger.info("Sending to odrive: " + str(speed))
            self.move_cmd = Twist()
            self.move_cmd.linear.x = speed
            self.cmd_vel_pub.publish(self.move_cmd)
            self.last_command_sent = speed

    def execute_collection_bucket_command(self, command):
        self.logger.info("Executing arduino command: " + command)
        
        if(self.serial_com == None):
            self.logger.error("Arduino not connected")
            return
        
        self.serial_com.read_all()
        self.serial_com.write(command.encode('utf-8'))

        # Wait for !OK responses
        output = b""
        instruction_count = len(command.split(','))
        count = 0
        while (count < instruction_count):
            output += self.serial_com.readline()
            if b"!OK" in output:
                count += 1
                output = b""
        
        self.logger.info("Arduino command executed")
    
    def wait(self, seconds):
        start_time = default_timer()
        while(True):
            if(default_timer() - start_time > seconds):
                time.sleep(0.1)
                break

def main(args=None):
    rclpy.init(args=args)

    movementController = MovementControllerNode()

    rclpy.spin(movementController)

    movementController.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()