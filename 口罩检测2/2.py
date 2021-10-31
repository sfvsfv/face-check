# coding=gbk
"""
作者：川川
@时间  : 2021/10/28 14:45
群：970353786
"""
with open('mask.txt', 'r') as f:
    try:
        test_img_path=[]
        for line in f:
            test_img_path.append(line.strip())
    except:
        print('图片加载失败')
print(test_img_path)
