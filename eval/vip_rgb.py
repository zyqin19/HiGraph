import os
import argparse
import numpy as np
from PIL import Image
import cv2

colors = [[0, 0, 0], [255, 85, 0], [255, 170, 0], [255, 255, 0], [170, 255, 0], [85, 255, 0], [0, 255, 0],
              [0, 255, 85], [0, 255, 170], [0, 255, 255], [0, 170, 255], [0, 85, 255], [0, 0, 255], [85, 0, 255],
              [170,0,255],[255,0,255],
          [0, 255, 85], [0, 255, 170], [0, 255, 255], [0, 170, 255], [0, 85, 255], [0, 0, 255], [85, 0, 255],
          [170, 0, 255], [255, 0, 255]
          ]

PRE_DIR = '../results/vip/'
RGB_DIR = '../results/vip_rgb/'

parser = argparse.ArgumentParser()

parser.add_argument("-g", "--rgb_dir", type=str, default=RGB_DIR,
                    help="ground truth path")
parser.add_argument("-p", "--pre_dir", type=str, default=PRE_DIR,
                    help="prediction path")

args = parser.parse_args()

def init_path():
    image_dir = args.pre_dir
    rgb_dir = args.rgb_dir

    file_names = []
    # for vid in os.listdir(image_dir):
    #     for img in os.listdir(os.path.join(image_dir, vid)):
    #         file_names.append([vid, img])
    for img in os.listdir(image_dir):
        if os.path.splitext(img)[-1] == '.png':
            file_names.append(img)
    print ("result of", image_dir)

    image_paths = []
    rgb_paths = []
    for file_name in file_names:
        image_paths.append(os.path.join(image_dir, file_name))
        rgb_paths.append(os.path.join(rgb_dir, file_name))
    return image_paths, rgb_paths


if __name__ == '__main__':
    image_paths, rgb_paths = init_path()
    for img_path, rgb_path in zip(image_paths, rgb_paths):
        image = cv2.imread(img_path,cv2.IMREAD_GRAYSCALE)
        rgb_img = np.zeros((image.shape[0], image.shape[1], 3))
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                rgb_img[i, j, :] = colors[image[i][j]]

        cv2.imwrite(rgb_path, rgb_img)

        ori_img_dir = img_path.replace('_mask.png', '_blend.jpg')
        ori_img = cv2.imread(ori_img_dir)
        cat_img = np.zeros((image.shape[0], image.shape[1], 3))
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                if (rgb_img[i, j]==[0, 0, 0]).all():
                    cat_img[i, j, :] = ori_img[i, j, :]
                else:
                    cat_img[i,j,:] = rgb_img[i, j ,:]*0.7 + ori_img[i, j ,:] * 0.3

        cat_dir = img_path.replace('vip', 'vip_cat')
        cv2.imwrite(cat_dir, cat_img)
        # print(1)


