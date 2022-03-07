import cv2

import numpy as np

img = cv2.imread("lines.jpg",1)


pts1 = np.float32([[834, 1227], [2328, 1227],[61, 2381], [3018, 2381]])
pts2 = np.float32([[400, 400], [800, 400], [400, 800], [800, 800]])

# Apply Perspective Transform Algorithm
matrix = cv2.getPerspectiveTransform(pts1, pts2)
result = cv2.warpPerspective(img, matrix, (1000, 1000))

# Wrap the transformed image
cv2.imshow('frame', img)  # Initial Capture
cv2.imshow('frame1', result)  # Transformed Capture

cv2.waitKey(5000)
cv2.destroyAllWindows()



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

    cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)

cv2.imwrite('houghlines3.jpg',img)

