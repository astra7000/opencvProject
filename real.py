import cv2, sys, os
import numpy as np
from glob import glob

"""
1. 우선 opencv_0912에 있는 폴더 "Org"의 경로를 입력받는다.
2. Org 폴더에 있는 모든 이미지를 읽어와서, 각 이미지에 대해 다음을 수행한다.
    1) 이미지를 읽어온다.
    2) 각각의 이미지를 MAT 변수로서 저장한다.
    
"""
#class DataAugmenter():
    
# 이미지가 들어있는 폴더를 입력받는다. 리턴값은 폴더의 경로이다.
def read_path():
    global folder_path
    folder_path = input("Enter the path of the folder: ")
    return folder_path

# 폴더 안의 이미지들의 경로, 이름, 이미지의 행렬을 읽어온다. 리턴값은 파일명, 이미지행렬의 딕셔너리이다.
def read_file_names():
    global folder_path, file_dict
    file_path = glob(folder_path + "/*.jpeg")
    file_names = [os.path.basename(file) for file in file_path]
    images = [cv2.imread(file) for file in file_path]
    file_dict = {name: img for name, img in zip(file_names, images)}
    return file_dict

# Augmentation을 위한 폴더를 생성한다. (인수로는 폴더 저장경로와(전역변수로 빼버림) Augmentation<적용한효과> 이름을 입력받는다.)
def make_aug_folder(aug_name):
    global folder_path
    aug_folder_path = os.path.join(folder_path, aug_name)
    if not os.path.exists(aug_folder_path):
        os.makedirs(aug_folder_path)
    return aug_folder_path

def save_img(aug_folder_path, img, split):
    save_path = os.path.join(aug_folder_path, split[1])
    cv2.imwrite(save_path, img)
    print("저장 완료")
    return save_path
    
# (우선 학습을 위해) 224*224로 이미지를 resize한다.
def resize_images():
    global file_dict
    resize_mat = []
    rename = []
    
    for name, mat in file_dict.items():
        resize_mat.append(cv2.resize(mat, (224, 224), interpolation=cv2.INTER_LANCZOS4))
        rename.append(name.split(".")[0] + "_resize.jpeg")
    resize_dict = {name: mat for name, mat in zip(rename, resize_mat)}
    
    
    save_path = make_aug_folder("resize")
    
    for name, mat in resize_dict.items():
        cv2.imwrite(os.path.join(save_path, name), mat)
        
    return resize_dict

# 이미지를 회전시키는 함수
def rotate_images(degree):
    global file_dict
    rotate_mat = []
    rename = []
    
    for name, mat in file_dict.items():
        rows, cols = mat.shape[:2]
        M = cv2.getRotationMatrix2D((cols/2, rows/2), degree, 1)
        rotate_mat.append(cv2.warpAffine(mat, M, (cols, rows), borderMode=cv2.BORDER_REPLICATE))
        #rename.append(name.split(".")[0] + "_rotate%d.jpeg", degree)
        rename.append(f"{name.split('.')[0]}_rotate{degree}.jpeg")  # 문자열 포맷팅 사용
    rotate_dict = {name: mat for name, mat in zip(rename, rotate_mat)}
        
    save_path = make_aug_folder(f"rotate{degree}")
    
    for name, mat in rotate_dict.items():
        cv2.imwrite(os.path.join(save_path, name), mat)    
    
    return rotate_dict

# 이미지를 수평으로 뒤집는 함수
def hflip_images():
    global file_dict
    hflip_mat = []
    rename = []
    
    for name, mat in file_dict.items():
        hflip_mat.append(cv2.flip(mat, 1))
        rename.append(name.split(".")[0] + "_hflip.jpeg")
    hflip_dict = {name: mat for name, mat in zip(rename, hflip_mat)}
        
    save_path = make_aug_folder("hflip")
    
    for name, mat in hflip_dict.items():
        cv2.imwrite(os.path.join(save_path, name), mat)
        
    return hflip_dict

# 이미지를 수직으로 뒤집는 함수
def vflip_images():
    global file_dict
    vflip_mat = []
    rename = []
    
    for name, mat in file_dict.items():
        vflip_mat.append(cv2.flip(mat, 0))
        rename.append(name.split(".")[0] + "_vflip.jpeg")
    vflip_dict = {name: mat for name, mat in zip(rename, vflip_mat)}
        
    save_path = make_aug_folder("vflip")
    
    for name, mat in vflip_dict.items():
        cv2.imwrite(os.path.join(save_path, name), mat)   
    
    return vflip_dict

# /Users/shinminjae/Desktop/condaProject/opencvEX/opencvProject/opencv_0912/Org
read_path()
read_file_names()

resize_images()
rotate_images(30)
hflip_images()
vflip_images()
