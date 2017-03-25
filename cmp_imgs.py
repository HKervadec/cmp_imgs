#!/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import imread

def rgb2gray(img):
	return np.dot(img, [0.299, 0.587, 0.114])

def resize(img, shape=(64,64)):
	resized = np.ndarray(shape)
	for (i,j),_ in np.ndenumerate(resized):
		f1 = gray_img.shape[0] // shape[0]
		f2 = gray_img.shape[1] // shape[1]

		slisse =  gray_img[i*f1:(i+1)*f1,j*f2:(j+1)*f2]
		resized[i,j] = np.max(slisse)

	return resized

if __name__ == "__main__":
	img_name = "1920x1080.jpg"

	img = imread(img_name)

	gray_img = rgb2gray(img)
	plt.imshow(gray_img, cmap=plt.cm.gray)
	plt.show()

	resized = resize(gray_img)
	plt.imshow(resized, cmap=plt.cm.gray)
	plt.show()