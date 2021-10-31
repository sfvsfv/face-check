# coding=gbk
"""
作者：川川
@时间  : 2021/10/28 14:55
群：970353786
"""
with open('mask.txt', 'r') as f:
    try:
        test_img_path=[]
        for line in f:
            test_img_path.append(line.strip())
    except:
        print('图片加载失败')

import cv2

imgs=[cv2.imread(test_img_path[1])]#意思是这里只预测txt中第一张图片
#加载模块
import paddlehub as hub

module = hub.Module(name="pyramidbox_lite_mobile_mask")
# module = hub.Module(name="pyramidbox_lite_server_mask")
# 口罩检测预测
visualization=True #将预测结果保存图片可视化
output_dir='detection_result' #预测结果图片保存在当前运行路径下detection_result文件夹下
results = module.face_detection(images=imgs, use_multi_scale=True, shrink=0.6, visualization=True, output_dir='detection_result')
for result in results:
    print(result)

# 预测结果展示
import matplotlib.image as im
import matplotlib.pyplot as plt
import os

# 需要读取的路径
path_name = r'./detection_result'

for item in os.listdir(path=path_name):
    img = im.imread(os.path.join(path_name, item))
    plt.imshow(img)
    plt.show()
