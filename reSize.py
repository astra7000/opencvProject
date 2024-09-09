import cv2, sys
from newMakePoly import makePoly

makePoly()

src = cv2.imread('saved_image.jpg')

if src is None:
    sys.exit('Image load failed')

h, w = src.shape[:2]

dst = cv2.resize(src, dsize=(int(h * 0.25), int(w * 0.25)), fx=0.25, fy=0.25)
print(dst.shape)

cv2.imshow('src', src)
cv2.imshow('dst', dst)
cv2.waitKey()
cv2.destroyAllWindows()