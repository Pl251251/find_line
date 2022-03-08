import cv2
import numpy as np

img = cv2.imread("lines.jpg",1)

height = img.shape[0]
width = img.shape[1]

#perspective transform
pts1 = np.float32([[854, 1227], [2308, 1227],[81, 2381], [2998, 2381]])
pts2 = np.float32([[0, 0], [400, 0], [0, 400], [400, 400]])

matrix = cv2.getPerspectiveTransform(pts1, pts2)
#warp image
result = cv2.warpPerspective(img, matrix, (400, 400))

#gray and edge
gray = cv2.cvtColor(result,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,150,apertureSize = 3)

#detect lines
lines = cv2.HoughLines(edges, 1, np.pi / 180, 150, None, 0, 0)

#draw lines
for i in lines:
    rho = i[0][0]
    theta = i[0][1]
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * (a)))
    pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * (a)))
    cv2.line(result, pt1, pt2, (0, 0, 255), 1, cv2.LINE_AA)

matrix2 = cv2.getPerspectiveTransform(pts2, pts1)
final = cv2.warpPerspective(result, matrix2, (width, height))

#save image
cv2.imwrite('test1.jpg',result)
cv2.imwrite('final.jpg',final)
