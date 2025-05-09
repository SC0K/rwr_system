from setuptools import find_packages, setup

package_name = 'pressure_sub'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools', 'pyserial', 'dynamixel_sdk', 'numpy'],
    zip_safe=True,
    maintainer='ubuntu',
    maintainer_email='chooaron1@yahoo.com.sg',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'serial_subscriber = pressure_sub.serial_subscriber:main',
            'motor_control = pressure_sub.motor_control:main',
        ],
    },
)
