import cv2
import numpy as np


img = cv2.imread("image4.jpg",1)

height = img.shape[0]
width = img.shape[1]
print(height)
print(width)

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

#detect lines
lines = cv2.HoughLines(edges, 1, np.pi / 180, 144, None, 0, 0)

#draw lines
c=9000
d=0
for i in lines:
    rho = i[0][0]
    theta = i[0][1]
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * (a)))
    pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * (a)))
    #cv2.line(result, pt1, pt2, (0, 0, 255), 1, cv2.LINE_AA)


    if (x0<c):
        line1 =i
        c= x0
    if (x0>d):
        line2 =i
        d=x0


lst =[line1,line2]
lst2 =[]
for i in lst:
    rho = i[0][0]
    theta = i[0][1]
    a = np.cos(theta)
    b = np.sin(theta)
    x1 = a * rho
    y1 = b * rho
    pt1 = (int(x1 + 1000 * (-b)), int(y1 + 1000 * (a)))
    pt2 = (int(x1 - 1000 * (-b)), int(y1 - 1000 * (a)))
    lst2.append([a, b, x1, y1])
    cv2.line(result, pt1, pt2, (255, 0, 0), 1, cv2.LINE_AA)
    #cv2.circle(result,(int(x1),int(y1)),10,(255,0,0),10)

info1 =(lst2[1][2] + lst2[0][2])/2
info2 = (lst2[1][2]+lst2[0][2])/2

pt1 = (int(info1 + 1000 * ((-1) * lst2[0][1])), int((lst2[1][3]-lst2[0][3]) + 1000 * ((1) * lst2[0][0])))
pt2 = (int(info2 - 1000 * ((-1) * lst2[0][1])), int((lst2[1][3]-lst2[0][3]) - 1000 * ((1) * lst2[0][0])))
cv2.line(result, pt1, pt2, (0, 255, 0), 1, cv2.LINE_AA)



matrix2 = cv2.getPerspectiveTransform(pts2, pts1)
final = cv2.warpPerspective(result, matrix2, (width, height))

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
cv2.imwrite('test1.jpg',result)
cv2.imwrite('final.jpg',final)
cv2.imwrite('idk.jpg',img)
