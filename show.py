import cv2
import numpy as np
from PIL import Image

def showImg(mat):
    rgbMAT = cv2.cvtColor(mat, cv2.COLOR_BGR2RGB)

    return Image.fromarray(rgbMAT)

def showMultipleImg(mats):
    from matplotlib import pyplot as plt
    def inner(x):
        x1 = cv2.cvtColor(x, cv2.COLOR_BGR2RGB)
        return Image.fromarray(x1) 
    
    l = list(map(inner, mats))
    for p in l:
        plt.figure()
        plt.imshow(p)
    plt.show()
