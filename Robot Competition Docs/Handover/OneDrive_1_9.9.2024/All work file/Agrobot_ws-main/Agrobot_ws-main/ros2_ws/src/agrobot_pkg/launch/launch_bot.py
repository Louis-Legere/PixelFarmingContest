import os
import pathlib
import launch
from launch_ros.actions import Node
from launch import LaunchDescription
from launch.actions import ExecuteProcess, LogInfo, RegisterEventHandler
from launch.event_handlers import (OnShutdown)
from launch.substitutions import (FindExecutable)
from ament_index_python.packages import get_package_share_directory
from webots_ros2_driver.webots_launcher import WebotsLauncher
from webots_ros2_driver.webots_controller import WebotsController
from webots_ros2_driver.utils import controller_url_prefix


def generate_launch_description():
    package_dir = get_package_share_directory('agrobot_pkg')

    stop_robot = ExecuteProcess(
        cmd=[[
            FindExecutable(name='ros2'),
            ' topic pub --once ',
            ' /cmd_vel ',
            ' geometry_msgs/msg/Twist ',
            '"{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"'
        ]],
        shell=True
    )

    odrive_controller = Node(
        package="agrobot_pkg",
        name="odrive_controller_node",
        executable="odrive_controller_node"
    )

    movement_controller = Node(
        package="agrobot_pkg",
        name="movement_controller_node",
        executable="movement_controller_node"
    )

    vision_controller = Node(
        package="agrobot_pkg",
        name="vision_processing_node",
        executable="vision_processing_node"
    )

    arm_controller = Node(
        package="agrobot_pkg",
        name="arm_controller_node",
        executable="arm_controller_node"
    )

    emergency_stop = ExecuteProcess(
        cmd=[
            'gnome-terminal', '--',
            'ros2', 'run',
            'agrobot_pkg', 'stop_robot_node'
        ],
        name='emergency_stop',
        output='screen'
    )

    return LaunchDescription([
        odrive_controller,
        movement_controller,
        vision_controller,
        arm_controller,
        emergency_stop,
        RegisterEventHandler(
            OnShutdown(
                on_shutdown=[
                    LogInfo(msg='Exiting'),
                    LogInfo(msg='Stopping robot'),
                    stop_robot,
                    LogInfo(msg='Stopping done'),
                ]
            )
        )
    ])