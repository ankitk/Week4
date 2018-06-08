#!/usr/bin/env python3

'''
This is starter code for Lab 6 on Coordinate Frame transforms.

'''

import asyncio
import cozmo
import numpy as np
from cozmo.util import degrees
from time import sleep

def get_relative_pose(object_pose, reference_frame_pose):
	x_0 =  reference_frame_pose.position.x
	y_0 =  reference_frame_pose.position.y
	
	x_1 =  object_pose.position.x
	y_1 =  object_pose.position.y
	q_0 = object_pose.rotation.angle_z

	sin_q_0 = np.sin(q_0.radians)
	cos_q_0 = np.cos(q_0.radians)
	
	#rotation and translation
	matrixTranslationA = np.matrix([[cos_q_0, -sin_q_0, x_0], [sin_q_0, cos_q_0, y_0], [0, 0, 1]])
	matrixTranslationB = np.matrix([[x_1], [y_1], [1]])
	relativePosition = np.matmul(matrixTranslationA, matrixTranslationB)
	
	return relativePosition

def find_relative_cube_pose(robot: cozmo.robot.Robot):
	'''Looks for a cube while sitting still, prints the pose of the detected cube
	in world coordinate frame and relative to the robot coordinate frame.'''

	robot.move_lift(-3)
	robot.set_head_angle(degrees(0)).wait_for_completed()
	cube = None

	while True:
		try:
			cube = robot.world.wait_for_observed_light_cube(timeout=5)
			if cube:
				print("Robot pose: %s" % robot.pose)
				print("Cube pose: %s" % cube.pose)

				relative_pose = get_relative_pose(cube.pose, robot.pose)
				print("Cube pose in the robot coordinate frame: %s" % relative_pose)

				return relative_pose

		except asyncio.TimeoutError:
			print("Didn't find a cube")


if __name__ == '__main__':

	cozmo.run_program(find_relative_cube_pose)