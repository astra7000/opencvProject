import cv2
import numpy as np
import matplotlib.pyplot as plt

# 이미지 불러오기
src = cv2.imread("/Users/shinminjae/Desktop/condaProject/opencvEX/opencvProject/opencv_0906/misson/01.png")

# 2. 노이즈 제거 (Non-local Means Denoising 적용)

dst = cv2.fastNlMeansDenoisingColored(src, None, 10, 10, 7, 21)
dst = cv2.normalize(src, None, 0, 255, cv2.NORM_MINMAX)
# 3. 선명도 향상 (Unsharp Masking 적용)
blurred = cv2.GaussianBlur(dst, (0, 0), 2)
sharpened = cv2.addWeighted(dst, 1.5, blurred, -0.5, 0)


# 히스토그램 계산
hist1 = cv2.calcHist([dst], [0], None, [256], [0, 256])

# 이미지를 Matplotlib로 시각화
plt.plot(hist1)  # OpenCV 이미지를 Matplotlib에서 사용하기 위해 BGR을 RGB로 변환
plt.show()

cv2.imshow('img', src)
cv2.imshow('dst', dst)

cv2.waitKey()
cv2.destroyAllWindows()
