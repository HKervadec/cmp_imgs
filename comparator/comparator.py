#!/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import cv2
from skimage.measure import block_reduce
from glob import glob
from sys import argv
from pprint import PrettyPrinter


def rgb2gray(img):
	return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

def resize(img, size=(64,64)):
	X = img.shape[0]
	dx = size[0] - (X % size[0]) if (X % size[0]) != 0 else 0

	Y = img.shape[1]
	dy = size[1] - (Y % size[1]) if (Y % size[1]) != 0 else 0

	img = np.pad(img, ((0, dx),(0, dy)), 'constant')

	fx = img.shape[0] // size[0]
	fy = img.shape[1] // size[1]

	res = block_reduce(img, (fx,fy), np.max)

	return res

def pipeline(img_name):
	img = cv2.imread(img_name)

	gray_img = rgb2gray(img)

	return resize(gray_img)

def distance(img1, img2):
	try:
		assert(img1.shape == img2.shape)
	except:
		print(img1.shape)
		print(img2.shape)

	return np.sum(np.abs(img2 - img1))

def compute_hashes(img_list):
	hashes = {}

	for img_name in img_list:
		piped = pipeline(img_name)

		hashes[img_name] = piped

	return hashes

def find_nn(target_name, candidates, hashes, size=10):
	d = lambda i: distance(hashes[target_name], hashes[i])
	distances = [d(i) for i in candidates]

	results = list(zip(candidates, distances))
	results.sort(key=lambda i: i[1])

	return results[:size]

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

	hashes = compute_hashes([target] + candidates)
	results = find_nn(target, candidates, hashes)

	pp = PrettyPrinter(indent=4)
	pp.pprint(results)