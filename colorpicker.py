'''
Author: XPectuer
LastEditor: XPectuer
'''
import cv2

# 定义鼠标交互函数
def mouseColor(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(str.upper(out), color[y, x])  #输出图像坐标(x,y)处的HSV的值

path, out = "imgs/card_0.png","bgr"
img = cv2.imread(path)  #读进来是BGR格式
# 进行颜色格式的转换
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  #变成灰度图
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  #变成HSV格式
if out == 'bgr':
    color = img
if out == 'gray':
    color = gray
if out == 'hsv':
    color = hsv
    
    
cv2.namedWindow("Color Picker")
cv2.setMouseCallback("Color Picker", mouseColor)
cv2.imshow("Color Picker", img)
if cv2.waitKey(0):
    cv2.destroyAllWindows()
