#!/usr/bin/env python3
import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # launch file for tele-operation
    teleop_launch_path = os.path.join(
        get_package_share_directory("patasmonkey_teleop"),
        "launch",
        "patasmonkey_teleop_sim.launch.py",
    )
    teleop_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(teleop_launch_path)
    )

    # launch file to spawn the UGV in gazebo
    spawn_launch_path = os.path.join(
        get_package_share_directory("patasmonkey_gazebo"),
        "launch",
        "spawn_patasmonkey_sim.launch.py",
    )
    spawn_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(spawn_launch_path)
    )

    # bridge between ros2 and gazebo
    sim_cmd_vel_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=[["/sim_cmd_vel@geometry_msgs/msg/Twist]ignition.msgs.Twist"]],
        output="screen",
    )
    joint_states_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=[
            "/joint_states@sensor_msgs/msg/JointState[ignition.msgs.Model"
        ],
        # ],
        output="screen",
    )
    # joint_states_bridge = Node(
    #     package="ros_gz_bridge",
    #     executable="parameter_bridge",
    #     arguments=[
    #         ['/world/', world,
    #          '/model/', robot_name,
    #          '/link/rplidar_link/sensor/rplidar/scan' +
    #          '@sensor_msgs/msg/LaserScan[ignition.msgs.LaserScan']
    #     ],
    #     output="screen"
    # )

    return LaunchDescription(
        [
            # SetEnvironmentVariable("ROS_DOMAIN_ID", "30"),
            teleop_launch,
            spawn_launch,
            sim_cmd_vel_bridge,
            joint_states_bridge,
        ]
    )


if __name__ == "__main__":
    generate_launch_description()
