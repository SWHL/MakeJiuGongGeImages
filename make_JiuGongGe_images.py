#!/usr/bin/env python
# coding: utf-8
from pathlib import Path
import cv2
import numpy as np
from matplotlib import pyplot as plt


def obtain_heart(bg_path, image_path):
    """将给定图像扣为心形"""
    
    heart_im = cv2.imread(bg_path)
    heart_im = cv2.cvtColor(heart_im, cv2.COLOR_BGR2GRAY)

    im = cv2.imread(image_path)
    im = cv2.resize(im, (heart_im.shape[1], heart_im.shape[0]))
    im_back = np.zeros_like(im)

    rows, cols = heart_im.shape[:2]
    for i in range(rows):
        for j in range(cols):
            if heart_im[i, j] == 0:
                im_back[i, j, :] = im[i, j, :]
            else:
                im_back[i, j, :] = 255

    im_back = cv2.cvtColor(im_back, cv2.COLOR_BGR2RGB)
    return im_back


def split_nine_images(im, image_path):
    """将图像分为九部分，并保存到对应路径下"""

    height, width = im.shape[:2]
    big_line = max(height, width)

    new_img = np.zeros([big_line, big_line, 3], np.uint8) + 255

    if height > width:
        edge = (big_line - width) // 2
        new_img[:, edge: width+edge, :] = im
    else:
        edge = (big_line - height) // 2
        new_img[edge: height+edge, :, :] = im

    sub_height, sub_width = int(big_line / 3), int(big_line / 3)

    save_result_dir = Path('./assets/results') / Path(image_path).stem
    save_result_dir.mkdir(parents=True, exists_ok=True)

    for i in range(3):
        for j in range(3):
            if i < 2:
                if j < 2:
                    temp_img = new_img[i*sub_height: (i+1)*sub_height, j*sub_width: (j+1)*sub_width, :]
                else:
                    temp_img = new_img[i*sub_height: (i+1)*sub_height, j*sub_width:, :]
            else:
                if j < 2:
                    temp_img = new_img[i*sub_height: , j*sub_width: (j+1)*sub_width, :]
                else:
                    temp_img = new_img[i*sub_height: , j*sub_width:, :]
            temp_img = cv2.cvtColor(temp_img, cv2.COLOR_BGR2RGB)

            save_full_path = save_result_dir / f'{i * 3 + j}.jpg'
            cv2.imwrite(str(save_full_path), temp_img)
    print(f'九宫格图已经保存在{save_result_dir}，序号顺序为从左到右')


if __name__ == '__main__':
    # 指定扣的形状
    bg_path = './assets/background/heart.jpg'

    # 原图
    image_path =  './assets/raw_images/1.jpg'

    # 扣除指定背景图
    result = obtain_heart(bg_path, image_path)

    # 分为九宫格
    split_nine_images(result)
