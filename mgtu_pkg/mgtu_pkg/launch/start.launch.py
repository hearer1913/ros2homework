from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import EnvironmentVariable

def generate_launch_description():
    video_publisher_node = Node(
        package='mgtu_pkg',
        executable='video_publisher',
        name='video_publisher',
        output='screen',
        parameters=[{'file_name': EnvironmentVariable('V_SRC')}],
        emulate_tty=True
    )

    yolo_seg_node = Node(
        package='mgtu_pkg',
        executable='yolo_seg_node',
        name='yolo_seg_node',
        output='screen',
        parameters=[{'file_name_dst': EnvironmentVariable('V_DST')}],
        emulate_tty=True
    )

    return LaunchDescription([
        video_publisher_node,
        yolo_seg_node  # Теперь оба узла запускаются сразу
    ])