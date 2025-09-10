import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import curses
import subprocess

class StopRobotNode(Node):
    def __init__(self, stdscr):
        super().__init__('stop_robot_node')        
        self.publisher = self.create_publisher(Twist, "/cmd_vel", 1)
        self.stdscr = stdscr
        curses.curs_set(0)  # Hide cursor
        self.stdscr.nodelay(True)  # Don't block I/O calls

    def start(self):
        self.get_logger().warning("Use this terminal to stop the robot by pressing spacebar\n")
        try:
            while rclpy.ok():
                self.stdscr.refresh()
                key = self.stdscr.getch()
                if key == ord(' '):
                    self.get_logger().warning("!!! STOPPING ROBOT !!!\n")
                    self.publish_empty_twist()
                # Add a small delay so we don't consume too much CPU
                rclpy.spin_once(self, timeout_sec=0.1)
        finally:
            # Set everything back to normal after we're finished
            curses.nocbreak()
            self.stdscr.keypad(False)
            curses.echo()
            curses.endwin()

    def publish_empty_twist(self):
        
        # Publish emergency stop command
        twist = Twist()
        twist.angular.x = -99.0
        twist.angular.y = -99.0
        twist.angular.z = -99.0
        self.publisher.publish(twist)

def main(stdscr):
    if is_node_running('stop_robot_node'):
            raise SystemExit

    rclpy.init()
    stop_robot_node = StopRobotNode(stdscr)
    stop_robot_node.start()

def initialize():
    curses.wrapper(main) # Passes terminal reference to main (stdscr)
    

def is_node_running(node_name):
    result = subprocess.run(['ros2', 'node', 'list'], stdout=subprocess.PIPE)
    return node_name in result.stdout.decode('utf-8')