import cv2

import numpy as np

img = cv2.imread("lines.jpg",1)


pts1 = np.float32([[854, 1227], [2308, 1227],[81, 2381], [2998, 2381]])
pts2 = np.float32([[0, 0], [400, 0], [0, 400], [400, 400]])

# Apply Perspective Transform Algorithm
matrix = cv2.getPerspectiveTransform(pts1, pts2)
result = cv2.warpPerspective(img, matrix, (400, 400))

# Wrap the transformed image
"""cv2.imshow('frame', img)  # Initial Capture
cv2.imshow('frame1', result)  # Transformed Capture

cv2.waitKey(5000)
cv2.destroyAllWindows()
"""

gray = cv2.cvtColor(result,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,150,apertureSize = 3)

lines = cv2.HoughLines(edges, 1, np.pi / 180, 150, None, 0, 0)

if lines is not None:
    for i in range(0, len(lines)):
        rho = lines[i][0][0]
        theta = lines[i][0][1]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * (a)))
        pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * (a)))
        cv2.line(result, pt1, pt2, (0, 0, 255), 1, cv2.LINE_AA)
"""
gray = cv2.cvtColor(result,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,150,apertureSize = 3)

lines = cv2.HoughLines(edges,1,np.pi/180,200)
for rho,theta in lines[0]:
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))

    cv2.line(result,(x1,y1),(x2,y2),(0,0,255),2)
"""

cv2.imwrite('houghlines3.jpg',result)
