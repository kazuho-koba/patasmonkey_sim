#!/usr/bin/env python3
import os
from launch import LaunchDescription
from launch.actions import SetEnvironmentVariable, ExecuteProcess
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # model identifier
    ugv_model = "patasmonkey_model"

    # path for world file (select a single file)
    world_file = os.path.expanduser(
        # "~/.ignition/gazebo/worlds/simple_baylands/simple_baylands.sdf",
        # "~/.ignition/gazebo/worlds/kazu_playground1/kazu_playground1.sdf",
        # "~/.ignition/gazebo/worlds/baylands/baylands.sdf",
        # "~/.ignition/gazebo/worlds/harmonickazu/harmonickazu.sdf",
        "~/.ignition/gazebo/worlds/harmonicworld/harmonicworld.sdf",
    )

    # urdf file path for UGV(for visualization in rviz)
    robot_model_file = os.path.join(
        get_package_share_directory("patasmonkey_gazebo"),
        "urdf",
        "patasmonkey_model.urdf",
    )

    # sdf file path for UGV(for simulation in gazebo fortress)
    robot_model_sdf = os.path.join(
        get_package_share_directory("patasmonkey_gazebo"),
        "sdf",
        "patasmonkey_model.sdf",
    )

    # read robot model for robot_state_publisher
    try:
        with open(robot_model_file, "r") as f:
            robot_description_content = f.read().replace("\n", " ")
    except Exception as e:
        robot_description_content = ""
        print(f"Error reading robot model file: {e}")

    # launch ignition gazebo fortress
    ignition_launch = ExecuteProcess(
        cmd=[
            "ros2",
            "launch",
            "ros_gz_sim",
            "gz_sim.launch.py",
            "gz_args:=" + world_file,
            "gui:=true",
            "paused:=false",
        ],
        output="screen",
    )

    # launch robot state publisher
    rsp_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[{"robot_description": robot_description_content}],
    )

    # spawn your robot
    spawn_entity = ExecuteProcess(
        cmd=[
            "ros2",
            "run",
            "ros_gz_sim",
            "create",
            "-name",
            ugv_model,
            "-file",
            robot_model_sdf,
            "-x",
            "1.0",
            "-y",
            "0.0",
            "-z",
            "0.5",
            "-R", "0.0",    #
            "-P", "0.0",    # 
            "-Y", "3.1416"  # 
        ],
        output="screen",
    )

    return LaunchDescription(
        [
            SetEnvironmentVariable("PATASMONKEY_MODEL", ugv_model),
            ignition_launch,
            rsp_node,
            spawn_entity,
        ]
    )


if __name__ == "__main__":
    generate_launch_description()
