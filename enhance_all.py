import cv2
import numpy as np

def enhance_night_image(img_path):
    """
    야경 이미지를 개선하는 함수

    Args:
        img_path (str): 입력 이미지 경로

    Returns:
        numpy.ndarray: 개선된 이미지
    """
    img = cv2.imread(img_path)

    # 1. 전처리: 노이즈 제거 (Non-local Means Denoising)
    denoised = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)

    # 2. 톤 매핑 (HDR 효과 적용)
    tonemapped = cv2.createTonemap(gamma=1.2).process(denoised.astype(np.float32))
    tonemapped = (tonemapped * 255).astype(np.uint8)

    # 3. 색상 조정
    # 3-1. 색상 균형 조정 (LAB 색 공간 활용)
    lab = cv2.cvtColor(tonemapped, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l = clahe.apply(l)
    merged_lab = cv2.merge((l, a, b))
    balanced = cv2.cvtColor(merged_lab, cv2.COLOR_LAB2BGR)

    # 3-2. 채도 조절 (HSV 색 공간 활용)
    hsv = cv2.cvtColor(balanced, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    s = cv2.addWeighted(s, 1.3, np.zeros_like(s), 0, 0)  # 채도 증가
    merged_hsv = cv2.merge((h, s, v))
    enhanced = cv2.cvtColor(merged_hsv, cv2.COLOR_HSV2BGR)

    # 4. 선명도 향상 (Unsharp Masking)
    blurred = cv2.GaussianBlur(enhanced, (5, 5), 1.5)
    sharpened = cv2.addWeighted(enhanced, 1.8, blurred, -0.8, 0)

    return sharpened

# 이미지 처리 및 저장
img_path = 'misson/misson_image05.png'  # 이미지 경로
enhanced_img = enhance_night_image(img_path)


# 결과 출력 (선택 사항)

cv2.imshow("Enhanced Night Image", enhanced_img)
cv2.waitKey(0)
cv2.destroyAllWindows()