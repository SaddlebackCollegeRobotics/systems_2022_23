import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node


def generate_launch_description():


    # Include the robot_state_publisher launch file, provided by our own package. Force sim time to be enabled
    # !!! MAKE SURE YOU SET THE PACKAGE NAME CORRECTLY !!!

    package_name='helios' 

    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','rsp.launch.py'
                )]), launch_arguments={'use_sim_time': 'true'}.items()
    )

    # Include the Gazebo launch file, provided by the gazebo_ros package
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py'
                )]), #launch_arguments={'gz_args' : 'src/systems_2022_23/helios/worlds/my_world.sdf'}.items()
                #TODO set up launch arguments to launch custom world, 
             )

    # Run the spawner node from the gazebo_ros package. The entity name doesn't really matter if you only have a single robot.
    #NOTE: need to change to work with ignition
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'helios'],
                        output='screen')

    #NOTE not currently working
    # Run spawner node for differential drive controller
    diff_drive_spawner = Node(
        package='controller_manager',
        executable='spawner.py',
        arguments=['diff_cont'],
    )

    #NOTE not currently working
    # Run spawner node for joint broadcaster
    joint_broad_spawner = Node(
        package='controller_manager',
        executable='spawner.py',
        arguments=['joint_broad'],
    )

    # Launch them all!
    return LaunchDescription([
        rsp,
        gazebo,
        spawn_entity,
        #diff_drive_spawner,
        #joint_broad_spawner,
    ])