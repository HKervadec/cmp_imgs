#!/bin/env python3

import numpy as np
import cv2
from skimage.measure import block_reduce
from pprint import PrettyPrinter

try:
	from comparator.common import *
except:
	from common import *


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

def distance(img1, img2):
	assert(img1.shape == img2.shape)

	return np.sum(np.abs(img2 - img1))

def compute_features(img_list):
	hashes = {}

	for img_name in img_list:
		piped = gen_features(img_name, resize)

		hashes[img_name] = piped

	return hashes

def find_nn(target_name, candidates, hashes, size=10):
	d = lambda i: distance(hashes[target_name], hashes[i])
	distances = [d(i) for i in candidates]

	results = list(zip(candidates, distances))
	results.sort(key=lambda i: i[1])

	return results[:size]


if __name__ == "__main__":
	target, candidates = parse_args()

	hashes = compute_features([target] + candidates)
	results = find_nn(target, candidates, hashes)

	pp = PrettyPrinter(indent=4)
	pp.pprint(results)