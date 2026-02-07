import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    
    package_name = 'agv_description'
    pkg_path = get_package_share_directory(package_name)
    urdf_file = os.path.join(pkg_path, 'urdf', 'AGV_WS.urdf')

    
    doc = xacro.process_file(urdf_file)
    robot_description = {'robot_description': doc.toxml()}

    
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description]
    )

    
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')])
    )

   
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description', '-entity', 'my_agv'],
        output='screen'
    )

 
    return LaunchDescription([
        node_robot_state_publisher,
        gazebo,
        spawn_entity,
    ])
