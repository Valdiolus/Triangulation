#!/usr/bin/env python

import cv2
import numpy as np
import math
import direction

def main():
	img = cv2.imread("test.jpg")
	# Init
	baseline=0.6
	theta = 0 # Heading
	L = 2 # Distance
	L1 = L # Left distance
	L2 = L # Right distance
	while True:

		# Compute L1, L2 from L, theta
		#(x,z) = (L*math.sin(theta), L*math.cos(theta))
		#L1 = math.sqrt((x+baseline/2)**2 + z**2)
		#L2 = math.sqrt((x-baseline/2)**2 + z**2)

		# Compute and show direction
		img1 = np.copy(img)
		[dist, heading] = direction.draw_direction(img1, L1, L2, baseline)
		print "dist", dist, "| heading(deg)", heading/math.pi*180
		cv2.imshow('Image', img1)

		# Process keyboard
		key = cv2.waitKey(50)
		ascii_code = key & 0xFF
		# Stop
		if (ascii_code == 27):
			break
		# Increase L1
		if (ascii_code == ord('w') or ascii_code == ord('W')):
			L1 += 0.1
			#L += 0.1
		# Decrease L1
		if (ascii_code == ord('x') or ascii_code == ord('X')):
			L1 -= 0.1
			#L -= 0.1
		# Decrease L2
		if (ascii_code == ord('a') or ascii_code == ord('A')):
			L2 -= 0.1
			#theta -= 1/180.0*math.pi
		# Increase L2
		if (ascii_code == ord('d') or ascii_code == ord('D')):
			L2 += 0.1
			#theta += 1/180.0*math.pi

if __name__ == '__main__':
	main()