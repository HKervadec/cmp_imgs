#!/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import cv2
from glob import glob
from sys import argv
from pprint import PrettyPrinter


def rgb2gray(img):
	return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

def resize(img, shape=(64,64)):
	resized = np.ndarray(shape)
	for (i,j),_ in np.ndenumerate(resized):
		f1 = img.shape[0] // shape[0]
		f2 = img.shape[1] // shape[1]

		slisse =  img[i*f1:(i+1)*f1,j*f2:(j+1)*f2]
		resized[i,j] = np.max(slisse)

	return resized

def pipeline(img_name):
	img = cv2.imread(img_name)
	gray_img = rgb2gray(img)

	return resize(gray_img)

def distance(img1, img2):
	assert(img1.shape == img2.shape)

	return np.sum(np.abs(img2 - img1))


if __name__ == "__main__":
	if len(argv) < 3:
		print("Use: {} <target> <folder>".format(argv[0]))
		exit(0)

	target = argv[1]

	exts = ["jpg", "png"]
	paths = ["{}/*.{}".format(argv[2], ext) for ext in exts]
	candidates = [e for path in paths for e in glob(path)]
	if target in candidates:
		candidates.remove(target)

	hashs = {}
	for img_name in [target] + candidates:
		piped = pipeline(img_name)

		hashs[img_name] = piped

	distances = [distance(hashs[target], hashs[i]) for i in candidates]

	results = list(zip(candidates, distances))
	results.sort(key=lambda i: i[1])

	pp = PrettyPrinter(indent=4)
	pp.pprint(results)