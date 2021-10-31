# coding=gbk
"""
作者：川川
@时间  : 2021/10/30 15:51
群：970353786
"""
#检测模块封装：
import paddlehub as hub
import cv2

def Mask_detect(image):
    state = '未戴口罩'
    module = hub.Module(name="pyramidbox_lite_mobile_mask")  # 加载paddlehub预训练模型
    input_dict = {"data": [image]}

    results = module.face_detection(data=input_dict)  # 口罩检测预测
    result = results[0]
    for item in result['data']:#paddlehub的口罩检测可以检测多张人脸，本项目默认每次视频中只出现一个学生，故for循环仅执行一次
        x1 = item['left']
        y1 = item['top']
        x2 = item['right']
        y2 = item['bottom']
        kz = item['label']

        image = cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image, str(kz), (x1 - 5, y1 - 10), cv2.FONT_HERSHEY_COMPLEX, 1.0, (0, 0, 255), 1)
        if kz == 'MASK':
            state = '已戴口罩'

    return image,len(result['data']),state#返回检测结果，检测到人脸的个数，口罩佩戴情况