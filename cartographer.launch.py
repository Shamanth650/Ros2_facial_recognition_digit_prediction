from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='cartographer_ros',
            executable='cartographer_node',
            name='cartographer_node',
            output='screen',
            parameters=[
                {'use_sim_time': True},  # Use simulated time in Gazebo
                {'--log-level':'debug'}
            ],
            arguments=[
                '-configuration_directory', '/home/shamanth/ros2_ws/src/my_robot_bringup/config/',  # Update with your config path
                '-configuration_basename', 'cartographer.lua', '--log-level','debug'  # Lua file name
            ],
        ),
        Node(
            package='cartographer_ros',
            executable='cartographer_occupancy_grid_node',
            name='occupancy_grid_node',
            output='screen',
            parameters=[
                {'use_sim_time': True},  # Use simulated time in Gazebo
            ],
        ),
    ])

