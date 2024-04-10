'''
Author: XPectuer
LastEditor: XPectuer
'''

import cv2
import numpy as np
from PIL import Image
from consts import *


# import pytesseract
import os 

path = 'imgs/card_10.png'
img = cv2.imread(path)

color2terrain = {
    "purple" : HERMITS,
    "green": FOREST,
    "orange": PLAINS,
    "blue": RIVER,
    "pink": VILLIAGE,
    "grey": ROAD,
}
text2terrain = {
    '隐者': HERMITS,
    '森林': FOREST,
    '道路': ROAD,
    '河流': RIVER,
    '村庄': VILLIAGE,
    '平原': PLAINS,
}

text2clue = {
    '隐士': CLUE_HERMIT,
    '飞鸟': CLUE_BIRD,
    '树灵': CLUE_DRYAD,
    '极目': CLUE_OVERLOOK
} 


EPSILON = 5


from paddleocr import PaddleOCR, paddleocr
paddleocr.logging.disable(paddleocr.logging.DEBUG)
# Paddleocr目前支持的多语言语种可以通过修改lang参数进行切换
# 例如`ch`, `en`, `fr`, `german`, `korean`, `japan`



def ocr(img = './imgs/card_0.png', lang='ch'):
    ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory
    
    result = ocr.ocr(img, cls=True)
    texts = []
    result = list(filter(lambda x: x!=None, result))
    
    for res in result:
        for line in res:
            text = line[1][0]
            # print("line:", line[1][0])
            texts.append(text)
    return texts

def getClueType(texts):
    
    clueType = -1
    for txt in texts:
        if txt in text2clue.keys():
            clueType = text2clue[txt]
    
    return clueType


str2DireMap = {"西北":NORTH_WEST, "东南": SOUTH_EAST, "东北":NORTH_EAST, "西南":SOUTH_WEST}

def getClueDire(texts):
    sdires = ["西北", "东南", "东北", "西南"]    
    direR = -1
    for txt in texts:
        for sdire in sdires:
            if sdire in txt:
                direR =  str2DireMap[sdire]
    return direR

def getClueTask(path):
    texts = ocr(path)
    t = getClueType(texts)
    d = getClueDire(texts)
    print(path, GetClueDesc(t), GetDirectionDesc(d))
    return (path, t, d)

def process_directory(directory, f):
    """
    This function will process all PNG files in the specified directory
    """
    r = []
    abs = os.path.abspath(directory)
    for filename in os.listdir(abs):
        if filename.endswith(".png"):
            print(f"Processing {filename}")
            path = os.path.join(directory, filename)
            r.append(f(path))
    return r

def unify(raw:list[tuple])->list[tuple]:
    xcoors = list(map(lambda roi: roi[0], raw))
    ycoors = list(map(lambda roi: roi[1], raw))
    
    def denoise(x):
        xcoors = [_ for _ in x]
        for i, c1 in enumerate(xcoors):
            for j in range(i, len(xcoors)):
                c2 = xcoors[j]
                if abs(c1 - c2) < EPSILON:
                    m = min(c1, c2)
                    xcoors[i] = m
                    xcoors[j] = m
        return xcoors

    xcoors = denoise(xcoors)
    ycoors = denoise(ycoors)
    print(xcoors, ycoors)
    def snd_min(A):
        Ap = sorted(set(A))
        return Ap[1] if len(Ap) > 1 else Ap[0]


    def unify_inner(A):
        sndm = snd_min(A)
        m = min(A)
        # print(sndm,m)
        
        # !!! divided by zero
        
        offst = 1 if sndm - m == 0 else sndm - m
        return list(map(lambda x: (x - m) // offst, A))
        
    # coordinate tranlate (x,y) ==> (y,x)
    r = list(zip(unify_inner(ycoors),unify_inner(xcoors)))

    return r


def find_arrow_direction(image_path):
    # Load the image
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV)
    
    cv2.imwrite("test.png", thresh)
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Assume the largest contour is the arrow.
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    if contours:
        cnt = contours[0]

        # Approximate the contour to reduce the number of vertices
        epsilon = 0.01 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)

        # Find the bounding box and its center
        rect = cv2.minAreaRect(approx)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        center = np.mean(box, axis=0)

        # Find the tip of the arrow by identifying the vertex farthest from the center
        tip = max(approx, key=lambda x: np.linalg.norm(x-center))

        # Determine direction based on the tip's position relative to the center
        dx = tip[0][0] - center[0]
        dy = tip[0][1] - center[1]

        if abs(dx) > abs(dy):  # Horizontal arrow
            direction = WEST if dx < 0 else EAST
        else:  # Vertical arrow
            direction = NORTH if dy < 0 else SOUTH

        return direction
    else:
        return NO_DIRECTION



# 调色盘
color_dist = {'red': {'Lower': np.array([0, 60, 60]), 'Upper': np.array([6, 255, 255])},
              'blue': {'Lower': np.array([200, 0, 0]), 'Upper': np.array([255, 120, 100])},
              'pink': {'Lower': np.array([200, 110, 230]), 'Upper': np.array([251, 155, 255])},
              'grey': {'Lower': np.array([150, 150, 150]), 'Upper': np.array([155, 155, 155])},
              'orange': {'Lower': np.array([0, 126, 253]), 'Upper': np.array([5, 170, 255])},
              'purple': {'Lower': np.array([230, 0, 130]), 'Upper': np.array([255, 5, 215])},
              'green': {'Lower': np.array([0 , 128   ,0]), 'Upper': np.array([100, 255, 100])},
              'black': {'Lower': np.array([252, 252, 252]), 'Upper': np.array([255,255,255])},
              }

# cv recog coloured blocks
target_color = ['blue', 'pink', 'grey','orange', 'purple', 'green']

def parseKernelFromPath(path):
    img = cv2.imread(path)
    return parseKernel(img)


def parseKernel(img):
    masks = []
    for color in target_color:
        #print(color)
        terrainType = color2terrain[color]
        mask = cv2.inRange(img, color_dist[color]['Lower'], 
                           color_dist[color]['Upper'])
        print(mask)
        masks.append((terrainType, mask))
    
    terrains = []
    roi_masks = []
    
    
    for ttype, mask in masks:
        
        contours, _ = cv2.findContours(mask, 
                                        cv2.RETR_EXTERNAL, 
                                        cv2.CHAIN_APPROX_SIMPLE)
        
        rois = []
        t = []
        for cont in contours:
            x, y, w, h = cv2.boundingRect(cont)
            # add region of interest
            m = (x, y, w, h)
            if(w > EPSILON and h > EPSILON):
                print(m)
                rois.append(m)
                t.append(ttype)
                
            
        roi_masks.extend(rois)
        terrains.extend(t)

    
    coors = list(map(lambda roi: (roi[0], roi[1]), roi_masks))
    print("coors", coors)
    coors = unify(raw=coors)
    
    print(list(zip(terrains, coors)))
    
    return list(set(zip(terrains, coors)))
    
def parseArrow(path):
    return find_arrow_direction(path)

def fillOUTER(k):
    n = len(k)
    if n < 5:
        terrains = list(map(lambda x: x[0], k))
        coors = list(map(lambda x: x[1], k)) 
        
        # cornor cases
        if (0,0) in coors:
            terrains += [OUTER]
            if n == 4:
                if (2,0) in coors:
                    coorsp = list(map(lambda p: (p[0],p[1]+1), coors)) + [(1,0)]
                    return list(zip(terrains, coorsp))
                if (0,2) in coors:
                    coorsp = list(map(lambda p: (p[0]+1,p[1]), coors)) + [(0,1)]
                    return list(zip(terrains, coorsp))
            elif n == 3:
                terrains += [OUTER, OUTER]
                # 00 10 11
                # 00 01 10
                if (1,1) in coors:
                    coorsp = list(map(lambda p: (p[0],p[1]+1), coors)) + [(1,0), (2,1)]
                    return list(zip(terrains, coorsp))
                if (0,1) in coors:
                    coorsp = list(map(lambda p: (p[0]+1,p[1]+1), coors)) + [(0,1)]
                    return list(zip(terrains, coorsp))
        
        else:
            coorDrayd = [(0,1), (1,1), (1,0), (1,2), (2, 1)]
            print("coors:", coors)
            
            coSet = set(coors)
            for co in coorDrayd:
                if co not in coSet:
                    coors.append(co)
                    terrains.append(OUTER)
            
            return list(zip(terrains, coors))
    elif n == 5:
        return k
    else:
        assert False

def parseBird(path):
    return (CLUE_BIRD, [parseKernelFromPath(path)])
    
def parseDrayd(path):
    k = parseKernelFromPath(path)
    k_filled = fillOUTER(k)
    return (CLUE_DRYAD, [k_filled]) 

def preprocess(image):
    # preprocess
    scaled_image = cv2.resize(image, None, fx=1.2, fy=1.2,
                              interpolation=cv2.INTER_CUBIC)
    
    blur_image = cv2.GaussianBlur(scaled_image, (5,5), 0)
    
    gray_image = cv2.cvtColor(scaled_image, cv2.COLOR_BGR2GRAY)
    
    # cv2.imwrite("testout_gray.png", gray_image) 
    
    # Apply threshold to get binary image
    _, binary_image = cv2.threshold(gray_image, 170, 255, cv2.THRESH_BINARY_INV)  
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    morph_image = cv2.morphologyEx(binary_image, cv2.MORPH_CLOSE, kernel)
    # cv2.imwrite("testout.png", morph_image)
    return binary_image

def parseNumbersFromPath(path):
    img = cv2.imread(path)
    return parseNumbers(img)

def parseNumbers(image):
    
    processed_img = preprocess(image)
    cv2.imwrite("test.png", processed_img)
    # == ocr ==
    texts = ocr(processed_img)
    numbers = list(filter(lambda s: s.isdigit(), texts))
    ret = list(map(lambda x: int(x), numbers))
    return ret

def splitKernels(path):
    img = cv2.imread(path)
    # preprocess
    # scaled_image = cv2.resize(img, None, fx=1.2, fy=1.2,
                              # interpolation=cv2.INTER_CUBIC)
    
    blur_image = cv2.GaussianBlur(img, (5,5), 0)
    
    gray_image = cv2.cvtColor(blur_image, cv2.COLOR_BGR2GRAY)
   
    # Apply threshold to get binary image
    _, binary_image = cv2.threshold(gray_image, 254, 255, cv2.THRESH_BINARY_INV)  
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    morph_image = cv2.morphologyEx(binary_image, cv2.MORPH_CLOSE, kernel)
    # cv2.imwrite("testout.png", morph_image)

    edges = cv2.Canny(morph_image, 50, 150)
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # find and crop by number feature
    cropped_imgs = []
    nums = []
    for idx, cnt in enumerate(contours):
        if len(cnt) >= 4:
            [x,y,w,h] = cv2.boundingRect(cnt)
            cropped_img = img[y:y+h, x:x+w]
            # cv2.imwrite(f"testout_{idx}.png", cropped_img)
            n = parseNumbers(cropped_img) 
            if len(n) == 1:
                nums.extend(n)
                cropped_imgs.append(cropped_img)
                # cv2.imwrite(f"testout_{idx}.png", cropped_img)
    
    return cropped_imgs, nums            
    
def parseHermit(dire, path):
    
    # breakpoint()
    if dire == NO_DIRECTION:
        ks, nums = splitKernels(path)
        kernels = list(map(lambda x: parseKernel(x), ks))
        print(kernels)
        return (CLUE_HERMIT, kernels, nums, dire)
    else: # direction
        numbers = parseNumbersFromPath(path)
        k = parseKernelFromPath(path)
        print(k)
        return (CLUE_HERMIT, [k], numbers, dire)    
    
def parseOverlook(path):
    dire = parseArrow(path)
    k = parseKernelFromPath(path)
    return (CLUE_OVERLOOK, [k], dire)
    
def parseClue(clueType, dire, path):
    if clueType == CLUE_HERMIT:
        return parseHermit(dire, path)
    if clueType == CLUE_BIRD:
        return parseBird(path)
    if clueType == CLUE_DRYAD:
        return parseDrayd(path)
    if clueType == CLUE_OVERLOOK:
        return parseOverlook(path)

def test_batch():
    tasks = process_directory('./imgs', getClueTask)
    clues = []
    for t in tasks:
        path, clueType, dire = t
        clue = parseClue(clueType, dire, path)
        clues.append((path, clue))
    
    for r in clues:
        print("RESULT:", r)
    
    
    toWrite = str(list(map(lambda x: x[1], clues)))
    with open("clues.txt","w") as f:
        print(f'WRITING TO... {f.name}')
        f.write(toWrite)
    
            
def test1(path):
    t = getClueTask(path)
    path, clueType, dire = t
    clue = parseClue(clueType, dire, path)        
    print("result:", clue)
    
            

if __name__ == '__main__':
    test_batch()
    # test1("./imgs/card_4.png")
    # test1("./imgs/card_7.png")
    # test1("./imgs/card_0.png")
