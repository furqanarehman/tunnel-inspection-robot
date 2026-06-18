import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess, TimerAction
from ament_index_python.packages import get_package_share_directory
import xacro

def generate_launch_description():
    pkg = get_package_share_directory('tunnel_inspection_robot')
    urdf_file = os.path.join(pkg, 'urdf', 'tunnel_robot.urdf.xacro')
    params_file = os.path.join(pkg, 'config', 'params.yaml')
    robot_description = xacro.process_file(urdf_file).toxml()

    return LaunchDescription([

        # Start Gazebo with clock publisher
        ExecuteProcess(
            cmd=['gazebo', '--verbose',
                 '-s', 'libgazebo_ros_init.so',
                 '-s', 'libgazebo_ros_factory.so'],
            output='screen'
        ),

        # Robot State Publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': robot_description,
                         'use_sim_time': True}]
        ),

        # Spawn robot in Gazebo
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=['-topic', 'robot_description', '-entity', 'tunnel_robot'],
            output='screen'
        ),

        # RViz
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', os.path.join(
                get_package_share_directory('lio_sam'),
                'config', 'rviz2.rviz')],
            output='screen'
        ),

        # LIO-SAM nodes delayed by 5 seconds
        TimerAction(period=5.0, actions=[
            Node(
                package='lio_sam',
                executable='lio_sam_imuPreintegration',
                name='lio_sam_imuPreintegration',
                parameters=[params_file, {'use_sim_time': True}],
                output='screen'
            ),
            Node(
                package='lio_sam',
                executable='lio_sam_imageProjection',
                name='lio_sam_imageProjection',
                parameters=[params_file, {'use_sim_time': True}],
                output='screen'
            ),
            Node(
                package='lio_sam',
                executable='lio_sam_featureExtraction',
                name='lio_sam_featureExtraction',
                parameters=[params_file, {'use_sim_time': True}],
                output='screen'
            ),
            Node(
                package='lio_sam',
                executable='lio_sam_mapOptimization',
                name='lio_sam_mapOptimization',
                parameters=[params_file, {'use_sim_time': True}],
                output='screen'
            ),
        ]),
    ])