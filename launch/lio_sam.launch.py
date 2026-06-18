
import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
from ament_index_python.packages import get_package_share_directory
import xacro

def generate_launch_description():
    pkg = get_package_share_directory('tunnel_inspection_robot')
    urdf_file = os.path.join(pkg, 'urdf', 'tunnel_robot.urdf.xacro')
    params_file = os.path.join(pkg, 'config', 'params.yaml')
    robot_description = xacro.process_file(urdf_file).toxml()

    return LaunchDescription([

        # Start Gazebo
        ExecuteProcess(
            cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_factory.so'],
            output='screen'
        ),

        # Robot State Publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': robot_description}]
        ),

        # Spawn robot in Gazebo
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=['-topic', 'robot_description', '-entity', 'tunnel_robot'],
            output='screen'
        ),

        # LIO-SAM nodes
        Node(
            package='lio_sam',
            executable='lio_sam_imuPreintegration',
            name='lio_sam_imuPreintegration',
            parameters=[params_file],
            output='screen'
        ),

        Node(
            package='lio_sam',
            executable='lio_sam_imageProjection',
            name='lio_sam_imageProjection',
            parameters=[params_file],
            output='screen'
        ),

        Node(
            package='lio_sam',
            executable='lio_sam_featureExtraction',
            name='lio_sam_featureExtraction',
            parameters=[params_file],
            output='screen'
        ),

        Node(
            package='lio_sam',
            executable='lio_sam_mapOptimization',
            name='lio_sam_mapOptimization',
            parameters=[params_file],
            output='screen'
        ),

        # RViz for visualization
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen'
        ),
    ])