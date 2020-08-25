#!/usr/bin/env python
# coding: utf-8

import cv2
import numpy as np
from matplotlib import pyplot as plt


def obtain_heart(image_path):
    """
    将给定图像扣为心形
    """
    heart_im = cv2.imread('./assets/heart.jpg')

    heart_im = cv2.cvtColor(heart_im, cv2.COLOR_BGR2GRAY)

    im = cv2.imread(image_path)

    im = cv2.resize(im, (heart_im.shape[1], heart_im.shape[0]))

    im_back = np.zeros_like(im)

    rows, cols = heart_im.shape
    for i in range(rows):
        for j in range(cols):
            if heart_im[i, j] == 0:
                im_back[i, j, :] = im[i, j, :]
            else:
                im_back[i, j, :] = 255


    im_back = cv2.cvtColor(im_back, cv2.COLOR_BGR2RGB)
    return im_back


def split_nine_images(im: np.array):
    """
    将图像分为九部分，并保存到对应路径下
    """
    height, width = im.shape[:2]

    height, width

    big_line = max(height, width)

    newImg = np.zeros([big_line, big_line, 3], np.uint8) + 255

    if height > width:
        edge = (big_line - width) // 2
        newImg[:, edge: width+edge, :] = im
    else:
        edge = (big_line - height) // 2
        newImg[edge: height+edge, :, :] = im

    subHeight, subWidth = int(big_line / 3), int(big_line / 3)

    for i in range(3):
        for j in range(3):
            if i < 2:
                if j < 2:
                    tempImg = newImg[i*subHeight: (i+1)*subHeight, j*subWidth: (j+1)*subWidth, :]
                else:
                    tempImg = newImg[i*subHeight: (i+1)*subHeight, j*subWidth:, :]
            else:
                if j < 2:
                    tempImg = newImg[i*subHeight: , j*subWidth: (j+1)*subWidth, :]
                else:
                    tempImg = newImg[i*subHeight: , j*subWidth:, :]
            tempImg = cv2.cvtColor(tempImg, cv2.COLOR_BGR2RGB)
            cv2.imwrite(f'./assets/images/{i*3+j}.jpg', tempImg)


image_path =  './assets/1.jpg'
result = obtain_heart(image_path)
split_nine_images(result)
print('九宫格图已经保存在/assets/images/下，序号顺序为从左到右')
