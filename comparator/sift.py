#!/bin/env python3

import cv2
import numpy as np
from pickle import dump, load
from time import time
from pprint import PrettyPrinter

from common import *


sift = cv2.xfeatures2d.SIFT_create()
sift_f = lambda e: sift.detectAndCompute(e, None) #return (kp, des)
bf = cv2.BFMatcher()


def distance(features1, features2):
	matches = bf.knnMatch(features1[1], features2[1], k=2)

	good = [m for m,n in matches if (m.distance < 0.75*n.distance)]

	return sum((m.distance for m in good))

def compute_features(img_list, features=None):
	if features == None:
		features = {}

	for img_name in img_list:
		if img_name not in features:
			piped = gen_features(img_name, sift_f)

			features[img_name] = piped

	return features

def find_nn(target_name, candidates, features, size=10):
	d = lambda i: distance(features[target_name], features[i])
	distances = [d(i) for i in candidates]

	results = list(zip(candidates, distances))
	results.sort(key=lambda i: i[1])

	return results[:size]


if __name__ == "__main__":
	t = time()
	target, candidates = parse_args()

	savefile = "features.sift"
	try:
		with open(savefile, 'rb') as f:
			features = load(f)
			print("Loaded data from {}".format(savefile))
	except:
		print("No features file found")
		features = None

	features = compute_features([target] + candidates, features)

	print(time() - t)
	t = time()

	# with open(savefile, 'wb') as f:
	# 	print("Saving features to {}".format(savefile))
	# 	dump(features, f)

	# print(features[target][0])
	# print(len(features[target][0]))

	results = find_nn(target, candidates, features)
	print(time() - t)

	pp = PrettyPrinter(indent=4)
	pp.pprint(results)