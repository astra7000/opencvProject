import cv2, sys
import numpy as np


# 좌표 저장을 위한 리스트
points_3 = []
points_4 = []


# 마우스 이벤트 콜백 함수
def draw_polygon(event, x, y, flags, param):
    img = param[0]
    global points_3, points_4
    
    if event == cv2.EVENT_LBUTTONDOWN:
        
        if flags & cv2.EVENT_FLAG_SHIFTKEY:
            # 좌표 저장
            points_3.append((x, y))
            # 다각형 그리기
            if len(points_3) == 3:
                cv2.polylines(img, [np.array(points_3)], True, (0, 255, 0), 1)
        else:
            points_4.append((x, y))
            if len(points_4) == 4:
                cv2.polylines(img, [np.array(points_4)], True, (0, 0, 255), 1)
    cv2.imshow('img', img)


def makePoly():
# 흰색 캔버스를 생성
    img = np.ones((512, 512, 3), dtype=np.uint8) * 255

    cv2.imshow('img', img)

    # 메인에서 setMouseCallback() 함수 호출하면서 콜백 함수를 지정
    cv2.setMouseCallback('img', draw_polygon, [img])

    if cv2.waitKey() == 13:  # Check if the pressed key is Enter (ASCII code 13)
        cv2.imwrite('saved_image.jpg', img)
    cv2.destroyAllWindows()