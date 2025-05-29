from setuptools import setup

package_name = 'mgtu_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
            ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
            ('share/' + package_name, ['package.xml']),
            ('share/' + package_name, [package_name  + '/launch/start.launch.py']),
        ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='root',
    maintainer_email='root@todo.todo',
    description='ROS2 package with video publisher and YOLO node',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'video_publisher = mgtu_pkg.video_publisher:main',
            'yolo_seg_node = mgtu_pkg.yolo_seg_node:main',
        ],
    },
)
