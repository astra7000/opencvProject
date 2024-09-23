import cv2,sys
import numpy as np

# 이미지 불러오기
src = cv2.imread("/Users/shinminjae/Desktop/condaProject/opencvEX/opencvProject/opencv_0906/misson/misson_image03.png")

# 샤프닝 커널 설정 (직접 설정)
sharpen_kernel = np.array([
    [0, -1, 0],
    [-1, 5, -1],
    [0, -1, 0]
])

# 컨볼루션 연산을 통한 선명화
sharpened = cv2.filter2D(src,-1, sharpen_kernel)



# 이미지 출력 (선택 사항)
cv2.imshow('img',src)
cv2.imshow("Sharpened Image", sharpened)
cv2.waitKey(0)
cv2.destroyAllWindows()