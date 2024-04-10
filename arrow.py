import cv2
import numpy as np
import math

def preprocess(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (5, 5), 1)#进行高斯滤波
    ret,img_thr = cv2.threshold(img_blur,70,255,cv2.THRESH_BINARY)#二值化，使得图片更加清晰没有中间模糊的像素点
    # cv2.imshow("2",img_thr)
    img_canny = cv2.Canny(img_thr, 50, 50)#边缘检测
    kernel = np.ones((3, 3),np.uint8)
    img_dilate = cv2.dilate(img_canny, kernel, iterations =2)#边缘膨胀膨胀 
    img_erode = cv2.erode(img_dilate, kernel, iterations =1)#边缘腐蚀腐蚀 
    return img_erode

img =cv2.imread("./imgs/card_14.png")
contours, hierarchy = cv2.findContours(preprocess(img), 
                                       cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)#获取图像轮廓


