from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'rover_nav2'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        # Required by ROS2
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),

        # Include launch files
        (os.path.join('share', package_name, 'launch'),
            glob('launch/*.py')),

        # Include config files (nav2_params.yaml goes here)
        (os.path.join('share', package_name, 'config'),
            glob('config/*.yaml')),

        # Include map files
        (os.path.join('share', package_name, 'maps'),
            glob('maps/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='aanchal',
    maintainer_email='aanchal@todo.todo',
    description='Nav2 costmap tuner for URC rover with custom footprint',
    license='MIT',
    extras_require={
        'test': ['pytest'],
    },
    entry_points={
        'console_scripts': [
            'nav_client = rover_nav2.nav_client:main',
        ],
    },
)
