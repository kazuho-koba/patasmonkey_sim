# !/usr/bin/env python3
import os
from launch import LaunchDescription
from launch.actions import (
    IncludeLaunchDescription,
    ExecuteProcess,
    SetEnvironmentVariable,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # set environmental parameters (model of tb3)
    tb3_model = "waffle_pi"

    # path to the empty world file
    world_file = os.path.join(
        get_package_share_directory("patasmonkey_gazebo"),
        "worlds",
        "empty.sdf"
    )

    # load URDF from turtlebot3_description directory
    robot_model_file = os.path.join(
        get_package_share_directory("turtlebot3_description"),
        "urdf",
        "turtlebot3_waffle_pi.urdf"
    )

    # read robot_description for robot_state_publisher via python
    try:
        with open(robot_model_file, 'r') as infp:
            robot_description_content = infp.read().replace('\n', ' ')
    except Exception as e:
        robot_description_content = ""
        print(f"Error reading robot model file: {e}")

    # launch gazebo
    ignition_launch = ExecuteProcess(
        cmd=[
            'ros2', 'launch', 'ros_gz_sim', 'gz_sim.launch.py',
            'gz_args:=' + world_file,
            'gui:=true',
            'paused:=false'
        ],
        output='screen'
    )

    # launch robot_state_publisher
    rsp_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description_content}]
    )

    # spawn the robot
    spawn_entity = ExecuteProcess(
        cmd=[
            'ros2', 'run', 'ros_gz_sim', 'create',
            '-name', 'turtlebot3_waffle_pi',
            '-file', robot_model_file,
            '-x', '0.0', '-y', '0.0', '-z', '0.0'
        ],
        output='screen'
    )

    return LaunchDescription(
        [
            SetEnvironmentVariable("TURTLEBOT3_MODEL", tb3_model),
            ignition_launch,
            rsp_node,
            spawn_entity,
        ]
    )

if __name__ == '__main__':
    generate_launch_description()