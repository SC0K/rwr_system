cmake_minimum_required(VERSION 3.15)
project(hand_control)

## Use C++17
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

## By adding -Wall and -Werror, the compiler does not ignore warnings anymore,
## enforcing cleaner code.
add_definitions(-Wall)

find_package(rclpy REQUIRED)
find_package(std_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)

###########
## Build ##
###########

## Specify additional locations of header files


#############
## Install ##
#############

install(PROGRAMS
    hand_controller_node.py
  DESTINATION lib/${PROJECT_NAME}
)

# install the launch file
install(DIRECTORY
  launch
  DESTINATION share/${PROJECT_NAME}
)


ament_package()