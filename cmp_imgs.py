#!/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import imread

def rgb2gray(img):
	return np.dot(img, [0.299, 0.587, 0.114])



if __name__ == "__main__":
	img_name = "1920x1080.jpg"

	img = imread(img_name)

	gray_img = rgb2gray(img)
	plt.imshow(gray_img, cmap=plt.cm.gray)
	plt.show()

	resized = np.ndarray((64, 64))
	for (i,j),_ in np.ndenumerate(resized):
		f1, f2 = gray_img.shape[0] // 64, gray_img.shape[1] // 64
		slisse =  gray_img[i*f1:(i+1)*f1,j*f2:(j+1)*f2]
		resized[i,j] = np.max(slisse)

	plt.imshow(resized, cmap=plt.cm.gray)
	plt.show()