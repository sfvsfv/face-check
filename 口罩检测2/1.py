# coding=gbk
"""
作者：川川
@时间  : 2021/10/28 14:42
群：970353786
"""
# 待预测图片
test_img_path = ["./0.png"]

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

img = mpimg.imread(test_img_path[0])

# 展示待预测图片
plt.figure(figsize=(10,10))
plt.imshow(img)
plt.axis('off')
plt.show()
