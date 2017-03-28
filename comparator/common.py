#!/bin/env python3

import cv2
from glob import glob
from sys import argv

def rgb2gray(img):
	return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

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
