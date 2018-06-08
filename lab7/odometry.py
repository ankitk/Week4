#!/usr/bin/env python3

import cozmo
from cozmo.util import degrees, Angle, Pose, distance_mm, speed_mmps
import math
import time

# Wrappers for existing Cozmo navigation functions

def cozmo_drive_straight(robot, dist, speed):
    """Drives the robot straight.
        Arguments:
        robot -- the Cozmo robot instance passed to the function
        dist -- Desired distance of the movement in millimeters
        speed -- Desired speed of the movement in millimeters per second
    """
    robot.drive_straight(distance_mm(dist), speed_mmps(speed)).wait_for_completed()

def cozmo_turn_in_place(robot, angle, speed):
    """Rotates the robot in place.
        Arguments:
        robot -- the Cozmo robot instance passed to the function
        angle -- Desired distance of the movement in degrees
        speed -- Desired speed of the movement in degrees per second
    """
    robot.turn_in_place(degrees(angle), speed=degrees(speed)).wait_for_completed()

def cozmo_go_to_pose(robot, x, y, angle_z):
    """Moves the robot to a pose relative to its current pose.
        Arguments:
        robot -- the Cozmo robot instance passed to the function
        x,y -- Desired position of the robot in millimeters
        angle_z -- Desired rotation of the robot around the vertical axis in degrees
    """
    robot.go_to_pose(Pose(x, y, 0, angle_z=degrees(angle_z)), relative_to_robot=True).wait_for_completed()

# Functions to be defined as part of the labs

def get_front_wheel_radius():
    """Returns the radius of the Cozmo robot's front wheel in millimeters."""
    # observe one full rotation and calculate radius by C = 2*Pi*r, C = distance of full rotation.
    #circumference=85
    #cozmo_drive_straight(robot, circumference, 25)
    #radius = circumference/(math.pi*2)
    #print("Radius:" + str(radius))
    
    return 13.5

def get_distance_between_wheels():
    """Returns the distance between the wheels of the Cozmo robot in millimeters."""
    # Move robot 180 degrees and calculate the distance between orginal pose and current pose. Then multiply by 2, as the distance covered was only half.
    #(x, y) = (robot.pose.position.x, robot.pose.position.y)
    #cozmo_turn_in_place(robot, 180, 45)
    #(x1, y1) = (robot.pose.position.x, robot.pose.position.y)
    #distance = math.sqrt(math.pow((y - y1), 2) + math.pow((x - x1), 2)) * 2
    #print("Distance between wheels:" + str(distance))
    
    return 86

def rotate_front_wheel(robot, angle_deg):
    """Rotates the front wheel of the robot by a desired angle.
        Arguments:
        robot -- the Cozmo robot instance passed to the function
        angle_deg -- Desired rotation of the wheel in degrees
    """
    constant = math.pi * get_front_wheel_radius() * 2
    distance = constant * (angle_deg / 360)
    robot.drive_wheels(45, 45, duration=(distance/45)+0.5)

def my_drive_straight(robot, dist, speed):
    """Drives the robot straight.
        Arguments:
        robot -- the Cozmo robot instance passed to the function
        dist -- Desired distance of the movement in millimeters
        speed -- Desired speed of the movement in millimeters per second
    """
    robot.drive_wheels(speed, speed, 200, 200, duration=(dist/speed)+0.5)

def my_turn_in_place(robot, angle, speed):
    """Rotates the robot in place.
        Arguments:
        robot -- the Cozmo robot instance passed to the function
        angle -- Desired distance of the movement in degrees
        speed -- Desired speed of the movement in degrees per second
    """
    diameter = get_distance_between_wheels()
    circumference = math.pi * diameter
    
    travel_angle = angle % 360
    if travel_angle > 180 and angle < 0:
        travel_angle -= 180
    
    travel_distance = circumference*(travel_angle/360)
    travel_speed = circumference*(speed/360)
    
    left_speed = travel_speed
    right_speed = -travel_speed
    if angle < 0:
        left_speed = -travel_speed
        right_speed = travel_speed
    
    robot.drive_wheels(left_speed, right_speed, duration=(travel_distance/travel_speed)+0.5)
    
def my_go_to_pose1(robot, x, y, angle_z):
    """Moves the robot to a pose relative to its current pose.
        Arguments:
        robot -- the Cozmo robot instance passed to the function
        x,y -- Desired position of the robot in millimeters
        angle_z -- Desired rotation of the robot around the vertical axis in degrees
    """
    # ####
    # TODO: Implement a function that makes the robot move to a desired pose
    # using the my_drive_straight and my_turn_in_place functions. This should
    # include a sequence of turning in place, moving straight, and then turning
    # again at the target to get to the desired rotation (Approach 1).
    # ####
    
    rotation_angle = math.degrees(math.atan2(y,x))
    my_turn_in_place(robot, rotation_angle, 45)
    time.sleep(.15)
    my_drive_straight(robot, math.sqrt((x*x)+(y*y)), 30)
    time.sleep(.15)
    my_turn_in_place(robot, angle_z-rotation_angle, 45)

def run(robot: cozmo.robot.Robot):

    print("***** Front wheel radius: " + str(get_front_wheel_radius()))
    print("***** Distance between wheels: " + str(get_distance_between_wheels()))

    ## Example tests of the functions
    #cozmo_go_to_pose(robot, 100, 100, 45)

    #rotate_front_wheel(robot, 90)
    #my_drive_straight(robot, 170, 42.5)
    #my_turn_in_place(robot, -270, 30)

    my_go_to_pose1(robot, 100, 100, 45)
    #my_go_to_pose2(robot, 100, 100, 45)
    #my_go_to_pose3(robot, 100, 100, 45)


if __name__ == '__main__':

    cozmo.run_program(run)



