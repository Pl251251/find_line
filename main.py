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

cv2.waitKey(0)
cv2.destroyAllWindows()
