import math
import cv2
import numpy as np

# Compute distance and direction to object based on distance from two sensors
# Two sensors are assumed to be located at (-baseline/2,0) and (baseline/2,0) with Y-axis heading forward
# Object in positive Y-direction is triangulated
# Input:
# Ldist, Rdist - distance to object from left and right sensors
# baseline - distance between sensors
# Returns:
# Tuple [distance, heading(rad)] - positive heading - to the right, negative - to the left
def triangulate(Ldist, Rdist, baseline=0.6):
	# Check for validity
	if abs(Ldist-Rdist) > baseline - 1.e-8:
		print "Invalid distances!", Ldist, Rdist, baseline
		return
	# Compute
	b = 0.5*baseline
	dist = math.sqrt(0.5*(Ldist**2 + Rdist**2) - b**2)
	x = (Ldist**2 - Rdist**2)/(4*b)
	y = math.sqrt(Ldist**2 - (x+b)**2)
	heading = 0.5*math.pi - math.atan2(y, x)

	return [dist, heading]

# Draw distance and direction to object based on distance from two sensors
# Two sensors are assumed to be located at (-baseline/2,0) and (baseline/2,0) with Y-axis heading forward
# Input:
# img - input/output image
# Ldist, Rdist - distance to object from left and right sensors
# baseline - distance between sensors
# height - camera height above the ground
# pitch - camera pitch angle relative to the ground
# fx, fy - x- and y- focal length
# cx, cy - x- and y- principal points
# Returns:
# img - image with direction drawn
# Tuple [distance, heading(rad)] - positive heading - to the right, negative - to the left
def draw_direction(img, Ldist, Rdist, baseline=0.6, height = 1, pitch = 0, fx=640, fy=360, cx=640, cy=360, opacity = 0.5):
	w = img.shape[1]
	h = img.shape[0]
	
	# Triangulate
	[dist, heading] = triangulate(Ldist, Rdist, baseline)
	
	# Arrow params
	aZmin = 1.0
	aWidth = 0.05
	aHead = 0.5

	# Create arrow polygon
	xz = []
	xz.append((aWidth, aZmin))
	xz.append((aWidth, dist-aHead))
	xz.append((3*aWidth, dist-aHead))
	xz.append((0, dist))
	xz.append((-3*aWidth, dist-aHead))
	xz.append((-aWidth, dist-aHead))
	xz.append((-aWidth, aZmin))

	# Rotate by heading
	xyzr = []
	cosa = math.cos(heading)
	sina = math.sin(heading)
	for x,z in xz:
		xyzr.append((x*cosa + z*sina, height, -x*sina + z*cosa))

	# Project onto image
	uv = []
	for x,y,z in xyzr:
		uv.append((int(x/z*fx+cx), int(y/z*fy+cy)))

	# Draw arrow
	lineThickness = 2
	colorFill = (100,155,0)
	colorLine = (0,200,155)
	img1 = np.copy(img)
	cv2.fillPoly(img1, np.array([uv]), colorFill)
	cv2.polylines(img1, np.array([uv]), True, colorLine, lineThickness)
	cv2.addWeighted(img, (1-opacity), img1, opacity, 0, img)

	return [dist, heading]
