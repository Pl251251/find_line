import cv2
import numpy as np

#change name of image file
img = cv2.imread("image4.jpg",1)

height = img.shape[0]
width = img.shape[1]

#perspective transform
#pts1 = np.float32([[760, 2003], [2300, 2003],[248, 2923], [2805, 2923]])
pts1 = np.float32([[840, 1300], [2100, 1300],[350, 2523], [2605, 2523]])
pts2 = np.float32([[0, 0], [400, 0], [0, 400], [400, 400]])

matrix = cv2.getPerspectiveTransform(pts1, pts2)
#warp image
result = cv2.warpPerspective(img, matrix, (400, 400))


#gray and edge
gray = cv2.cvtColor(result,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,150,apertureSize = 3)

#find lines
linesP = cv2.HoughLinesP(edges, 1, np.pi / 180, 150, None, 50, 10)
#sort lines
c=9000
d=0
for i in linesP:
    l = i[0]
    cv2.line(result, (l[0], l[1]), (l[2], l[3]), (0, 0, 255), 3, cv2.LINE_AA)
    if (l[0]<c):
        line1 =i
        c= l[0]
    if (l[0]>d):
        line2 =i
        d=l[0]

#draw left most and right most lines
info1 = line1[0]
info2 =line2[0]
pt1 = (int(((info1[0]) +int(info2[0]))/2), int((info1[1] +info2[1])/2))
pt2 = (int((info1[2] +info2[2])/2), int((info1[3] +info2[3])/2))
cv2.arrowedLine(result, pt1, pt2, (255, 0, 0), 1, cv2.LINE_AA)

#tranform image back
matrix2 = cv2.getPerspectiveTransform(pts2, pts1)
final = cv2.warpPerspective(result, matrix2, (width, height))

#use a mask to overlap my images
roi = img[0:height, 0:width]
# Now create a mask of logo and create its inverse mask also
img2gray = cv2.cvtColor(final,cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(img2gray, 0, 255, cv2.THRESH_BINARY)
mask_inv = cv2.bitwise_not(mask)
# Now black-out the area of logo in ROI
img1_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)
# Take only region of logo from logo image.
img2_fg = cv2.bitwise_and(final,final,mask = mask)
# Put logo in ROI and modify the main image
dst = cv2.add(img1_bg,img2_fg)
img[0:height, 0:width ] = dst


#save image
cv2.imwrite('final.jpg',img)
