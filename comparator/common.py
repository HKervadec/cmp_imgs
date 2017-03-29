#!/bin/env python3

import cv2
from glob import glob
from sys import argv


def parse_args():
	if len(argv) < 3:
		print("Use: {} <target> <folder>".format(argv[0]))
		exit(0)

	target = argv[1]

	exts = ["jpg", "png"]
	paths = ["{}/*.{}".format(argv[2], ext) for ext in exts]
	candidates = [e for path in paths for e in glob(path)]
	if target in candidates:
		candidates.remove(target)

	return target, candidates

def gen_features(img_name, function):
	gray_img = cv2.imread(img_name,0)

	r_factor = 1000 / max(gray_img.shape[0], gray_img.shape[1])
	x = int(gray_img.shape[0] * r_factor)
	y = int(gray_img.shape[1] * r_factor)

	resized_img = cv2.resize(gray_img, (x, y))

	return function(gray_img)