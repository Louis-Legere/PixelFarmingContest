from timeit import default_timer
import rclpy
from odrive.enums import *
from rclpy.node import Node
import serial.tools.list_ports
from agrobot_msgs.srv import ArmPosition
import time
from enum import Enum

class ArmControllerNode(Node):
    crop_x = 0.0
    crop_y = 0.0
    crop_type = ""

    z_distance_to_crop = 485
    z_drop_off_distance = 50

    y_approach_distance = 50

    gripper_home_rotation = 0
    gripper_back_rotation = 0
    gripper_forward_rotation = 180
    gripper_drop_off_rotation = 270
    gripper_open = 100
    gripper_closed = 0

    bucket_locations = [100, 200, 730, 730]
    bucket_crop_types = ["Beetroot", "Carrot", "Lettuce", "Radish"]

    crops_collected = 0

    def __init__(self):
        # Set up node
        super().__init__('arm_controller_node')

        self.__node = rclpy.create_node('arm_controller_node')

        self.logger = self.get_logger() # Set up logger

        # Set up service
        self.create_service(ArmPosition, 'arm_target_position', self.__move_arm)

        # Set up ATMEL mega connection
        baud_rate = 19200
        ports = serial.tools.list_ports.comports()
        port = None
        for port in ports:
            if "FTDI" in port.manufacturer:
                self.logger.info("Connected to arm")
                port = port.device
                break

        self.atmega = serial.Serial(port, baud_rate)
        
        self.start()

    def start(self):
        # # For testing
        # self.crop_x = 200
        # self.crop_type = "Beetroot"
        # self.collect_crop()
        
        disable_command = self.create_command("$ACD")
        self.execute_commands([disable_command])

        pass

    def collect_crop(self):
        self.logger.info("Collecting crop")

        # Send enable command (because arm sometimes does not respond to the first command)
        enable_command = self.create_command("$ACE")
        self.execute_commands([enable_command])

        # # Move arm to home position
        # z_command = self.create_command("$APZ", 0)
        # y_command = self.create_command("$APY", 0)
        # self.execute_commands([z_command, y_command])

        # home_command = self.create_command("$ACH")
        # self.execute_commands([home_command])
        
        target = self.convert_pixel_to_coordinate(self.crop_x)
        self.logger.info("Target: " + str(target))

        # String to decide later on which side the arm will grab the crop
        # Seen from the perspective of the arm
        approach_direction = "" # "forward" or "backward"

        # Adjust on which side the arm will grab the crop
        if target > 220:
            approach_direction = "forward"
            # crop_x is the left side (back side from the perspective of the gripper) of the bounding box around the crop
            # we only need to adjust a little
            target -= 25
        else: 
            approach_direction = "backward"
            target += 100 # Vision publishes the top left corner of the bounding box, we need to target the other side

        # Move arm to the side of the target crop
        y_command = self.create_command("$APY", target)
        z_command = self.create_command("$APZ", self.z_distance_to_crop)
        self.execute_commands([z_command, y_command])

        # Rotate gripper
        gripper_rotation_command = None
        if approach_direction == "forward":
            gripper_rotation_command = self.create_command("$APA", self.gripper_forward_rotation)
        # Open gripper
        gripper_open_command = self.create_command("$APB", self.gripper_open)
        self.execute_commands([gripper_open_command, gripper_rotation_command])

        # Move arm into position
        y_command = ""
        if approach_direction == "backward":
            y_command = self.create_command("$APY", target - self.y_approach_distance)
        else:
            y_command = self.create_command("$APY", target + self.y_approach_distance)
        self.execute_commands([y_command])

        # Close gripper
        gripper_command = None
        if self.crop_type == "Lettuce":
            gripper_command = self.create_command("$APB", 20)
        else:
            gripper_command = self.create_command("$APB", 0)
        self.execute_commands([gripper_command])

        # Pull up
        z_command = self.create_command("$APZ", self.z_distance_to_crop - 100)
        self.execute_commands([z_command])

        self.wait(1)

        # Move gripper above desired bucket
        z_command = self.create_command("$APZ", self.z_drop_off_distance)
        # y_command depends on the type of crop
        bucket_index = self.bucket_crop_types.index(self.crop_type)
        y_command = self.create_command("$APY", self.bucket_locations[bucket_index])
        self.execute_commands([z_command, y_command])

        # Rotate gripper
        gripper_command = self.create_command("$APA", self.gripper_drop_off_rotation)
        self.execute_commands([gripper_command])

        # Open gripper  
        gripper_command = self.create_command("$APB", self.gripper_open)
        self.execute_commands([gripper_command])

        # Move arm back
        gripper_command = self.create_command("$APA", self.gripper_home_rotation)
        close_gripper_command = self.create_command("$APB", self.gripper_closed)
        self.execute_commands([gripper_command, close_gripper_command])
        y_command = self.create_command("$APY", 0)
        self.execute_commands([y_command])

        # Home
        if self.crops_collected == 3:
            crops_collected = 0
            home_command = self.create_command("$ACH")
            self.execute_commands([home_command])

        self.execute_commands([self.create_command("$ACD")]) # Disable

        self.logger.info("Done")

        crops_collected += 1

        self.crop_x = None
        self.crop_y = None
        self.crop_type = None
    
    def convert_pixel_to_coordinate(self, crop_x):
        if crop_x < 330:
            return 0
        elif crop_x > 1580:
            return 775
        else:
            return int((crop_x - 330) * 0.66)

    def create_command(self, cmd, value=None):
        # Input string: "$APY,200"
        # Output byte string: b"$APY,C8\r\n"

        command = b''
        if value == None:
            command = bytes(cmd + "\r\n", 'utf-8')
        else:
            value = hex(value)
            command = bytes(cmd + "," + value + "\r\n", 'utf-8').replace(b'0x', b'')
        
        return command

    def execute_commands(self, commands):
        ok_count = 0
        expected_ok_count = 0
        response = b''

        for command in commands:
            try:
                self.wait(0.3)
                self.atmega.write(command)

                if not b'ACE' in command and not b'ACD' in command: # ACE and ACD commands do not return an OK
                    expected_ok_count += 1

                self.logger.info("Sent command: " + str(command))
            except:
                self.logger.error("Failed to send command: " + str(command))
                return
            
        while ok_count < expected_ok_count:
            response += self.atmega.read_all().strip()
            if b'$OK' in response:
                ok_count += 1
                response = response.replace(b'$OK', b'')

        self.logger.info("Done exececuting")

    def wait(self, seconds):
        start_time = default_timer()
        while(True):
            if(default_timer() - start_time > seconds):
                break

    def __move_arm(self, request, response):
        self.crop_x = request.crop_x
        self.crop_y = request.crop_y
        self.crop_type = request.crop_type

        self.collect_crop()

        response.success = True
        return response

def main(args=None):
    rclpy.init(args=args)

    arm_controller = ArmControllerNode()

    rclpy.spin(arm_controller)

    arm_controller.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
