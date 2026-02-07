from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command
from launch_ros.parameter_descriptions import ParameterValue
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():

    pkg_path = get_package_share_directory('agv_description')
    urdf_file = os.path.join(pkg_path, 'urdf', 'AGV_WS.urdf')

    # Chuyển đổi file URDF sang dạng mà robot_state_publisher hiểu được
    robot_description = ParameterValue(
        Command(['xacro ', urdf_file]),
        value_type=str
    )

    return LaunchDescription([
        # 1. Node tính toán cây tọa độ (TF)
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': robot_description}],
            output='screen'
        ),
        
        # 2. THÊM NODE NÀY: Nó giúp tạo dữ liệu cho các bánh xe (Fix lỗi No Transform)
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui'
        ),

        # 3. Node mở RViz2
        Node(
            package='rviz2',
            executable='rviz2',
            output='screen'
        )
    ])
