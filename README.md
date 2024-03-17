# yunshenzhidi
检验程序

云深之地

- 检验可行解
- CV程序，输入卡牌图片，返回结构布局，（极目：箭头方向）



- 把隐士线索（特殊）与普通线索分开
  - 输出把所有解列出来
- 限制可以修改（DSL？）

## CV Detection
- [x] 线索图标会降低算法的识别效果（识别错误率上升），统一的卡牌形式可以防止顾此失彼
- [ ] Detection Mask to Kernel Objects

## kernel design
- [(TERRIAN , (x,y)), ...] where x, y are relative coordinate of certain terrian

## solver
- Backtracking Algorithm
  - [x] List All Possible Hermit Layout
    - [x] common
      - [x] Override Hermit Nearby
      - [x] Hermit Occupy Empty 
      - [x] Contraints to 
    - [x] direction

## Verification
- 
  - Number of middle result(hermit):
