import cv2
import numpy as np
from glob import glob
import os

def getImageList():
    basePath = os.getcwd()
    dataPath = os.path.join(basePath, 'dat')
    fileNames = glob(os.path.join(dataPath, '*.jpg'))
    return fileNames

def drawROI(img, corners):
    cpy = img.copy()
    line_c = (128, 128, 255)
    lineWidth = 2
    
    if corners:
        cv2.rectangle(cpy, tuple(corners[0]), tuple(corners[1]), color=line_c, thickness=lineWidth)
    
    for x1, x2 in rect:
        cv2.rectangle(cpy, tuple(x1), tuple(x2), color=line_c, thickness=lineWidth)
    
    disp = cv2.addWeighted(img, 0.3, cpy, 0.7, 0)
    return disp

def onMouse(event, x, y, flags, param):
    global startPt, drawing, img, ptList, cpy, txtWrData, rect
    
    if event == cv2.EVENT_LBUTTONDOWN:  # 마우스 왼쪽 버튼을 눌렀을 때
        drawing = True
        startPt = (x, y)
    elif event == cv2.EVENT_MOUSEMOVE:  # 마우스를 움직였을 때
        if drawing == True:
            ptList = [startPt, (x, y)]
            cpy = drawROI(img, ptList)
            cv2.imshow('label', cpy)
    elif event == cv2.EVENT_LBUTTONUP:  # 마우스 왼쪽 버튼을 뗐을 때
        drawing = False
        
        endPt = (x, y)                      # 마우스를 떼었을 때의 좌표
        ptList = [startPt, endPt]           # 만들어진 사각형의 시작점과 끝점을 리스트로 저장
        cpy = drawROI(img, ptList)          # 이미지에 사각형을 그림
        
        rect.append(ptList)                 # 사각형의 좌표를 rect 리스트에 추가
        txtWrData = str(rect)               # rect 리스트를 문자열로 변환하여 txtWrData에 저장
        
        cv2.imshow('label', cpy)
        print("rect입니다", rect)
    

def main():
    global img, cpy, rect, ptList, drawing, txtWrData
    
    ptList = []
    drawing = False
    txtWrData = None
    rect = []
    fileNames = getImageList()
    next = 0
    
    if not fileNames:
        print("이미지 파일을 찾을 수 없습니다.")
        return
    
    img = cv2.imread(fileNames[next])
    if img is None:
        print(f"이미지를 불러올 수 없습니다: {fileNames[0]}")
        return
    
    
    cv2.namedWindow('label')
    cv2.setMouseCallback('label', onMouse)
    cv2.imshow('label', img)
    
    while True:
        key = cv2.waitKey(1)
        if key == 27:  # ESC 키
            break
        elif key == ord('s'):
            next += 1
            filename, ext = os.path.splitext(fileNames[next])
            txtFilename = filename + '.txt'
            print(f"저장할 텍스트: {txtWrData}")
            with open(txtFilename, 'w') as f:
                f.write(txtWrData)
            print(f"텍스트 파일이 저장되었습니다: {txtFilename}")
        elif key == ord('g'):# 오른쪽 방향키의 ASCII 값
            print("오른쪽 방향키가 눌렸습니다.")
            next += 1
            rect = []
            img = cv2.imread(fileNames[next])
            cv2.namedWindow('label')
            cv2.setMouseCallback('label', onMouse)
            cv2.imshow('label', img)
        elif key == ord('d'):  # 왼쪽 방향키의 ASCII 값
            print("왼쪽 방향키가 눌렸습니다.")
            rect.pop()
            cpy = drawROI(img, None)
            cv2.imshow('label', cpy)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()