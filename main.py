import cv2
import numpy as np
from PIL import Image
import os 

from paddleocr import PaddleOCR, draw_ocr

from solvers.consts import *

from solvers.game_map import init_game_map

# cv recog coloured blocks
target_color = ['blue', 'pink', 'grey','orange', 'purple', 'green']
# 调色盘
color_dist = {'red': {'Lower': np.array([0, 60, 60]), 'Upper': np.array([6, 255, 255])},
              'blue': {'Lower': np.array([200, 0, 0]), 'Upper': np.array([255, 100, 100])},
              'pink': {'Lower': np.array([248, 150, 250]), 'Upper': np.array([251, 155, 255])},
              'grey': {'Lower': np.array([150, 150, 150]), 'Upper': np.array([155, 155, 155])},
              'orange': {'Lower': np.array([0, 168, 255]), 'Upper': np.array([5, 170, 255])},
              'purple': {'Lower': np.array([255, 0, 210]), 'Upper': np.array([255, 5, 215])},
              'green': {'Lower': np.array([0 , 102   ,6]), 'Upper': np.array([14, 147, 35])},
              'black': {'Lower': np.array([252, 252, 252]), 'Upper': np.array([255,255,255])},
              }

# color -> terrain
color2terrian = {'orange': PLAINS,
                 'blue': RIVER,
                 'pink': VILLIAGE,
                 'green': FOREST,
                 'grey': ROAD,
                 'purple': HERMITS}

def getTerrainFromColor(color):
    return color2terrian[color]

# text -> head
text2head = {
    '隐者': CLUE_HERMIT,
    '飞鸟':CLUE_BIRD,
    '树灵': CLUE_DRYAD,
    '极目': CLUE_OVERLOOK
}

def getHeadFromText(txt):
    return text2head[txt]


def pre(img):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    # afterDilate = cv2.dilate(afterGsB, kernel, iterations=1)
    afterErode = cv2.erode(img, kernel, iterations=3)
    return afterErode


def isMask(rect):
    w = rect[3]
    h = rect[4]
    inTer = (w > 25 and h > 25 and w - h < 10)
    outTer= ()
    return inTer or outTer
   
def toKernel(head, rois):
    if head == CLUE_HERMIT:
        pass
    elif head == CLUE_DRYAD:
        pass 
    elif head == CLUE_BIRD:
        pass
    elif head == CLUE_OVERLOOK:
        pass
    
    for roi in rois[1:]:
        x = roi[1]
        y = roi[2]    
        
 
def post(head, roi_masks):
    roisp = list(filter(isMask, roi_masks))

    # to kernel 
    r1 = toKernel(head, roisp)
    return r1
         

def extractTerrian(img_path, head, target_color,  pre_process, post_process):
    img = cv2.imread(img_path)
    afterPre = pre_process(img)
    
    masks = []
    for color in target_color:
        print("finding...", color)
        lowerb = color_dist[color]['Lower']
        upperb = color_dist[color]['Upper']
        mask = cv2.inRange(afterPre, lowerb, upperb)

        masks.append((color, mask))
        
    roi_masks = []
    for mask in masks:
        mask_inner = mask[1]
        contours, _ = cv2.findContours(mask_inner, 
                                       cv2.RETR_EXTERNAL, 
                                       cv2.CHAIN_APPROX_SIMPLE)
        
        rois = []
        for cont in contours:
            color = mask[0]
            x, y, w, h = cv2.boundingRect(cont)
            # add region of interest
            m = (color, x, y, w, h)
            rois.append(m)
        
        roi_masks.extend(rois)
            
        
    print("ROI_MASKS:", roi_masks)
    afterPost = post_process(head, roi_masks)
    print("AFTERPOST:", afterPost)
    return afterPost
    
    # concat_image = np.concatenate(masks, axis=1)
    # showMultipleImg(concat_image)
    

def extractHead(img_path):
    """
    Using Paddle OCR: MAC M1 not supported. PYTHON VER. == 3.10
    """
    ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory

    result = ocr.ocr(img_path, cls=True)
    texts = []
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            text = line[1][0]
            # print("line:", line[1][0])
            texts.append(text)
    
    txt = list(filter(lambda x: x in {'极目','飞鸟','树灵','隐士', '隐者'}, texts))[0]
    
    print(txt)
    return getHeadFromText(txt)

def extractArrow():
    pass

if __name__ == '__main__':
    path = 'imgs/card_2.png'
    # step 0. read image
    img = cv2.imread(path)
    # step 1. extract header
    head = extractHead(path)
    # step 2. extract kernel
    extractTerrian(path, head, target_color, pre, post)

    if head == CLUE_OVERLOOK:
       direction = extractArrow()
    


