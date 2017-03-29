#!/bin/env python3

import cv2
import numpy as np
from time import time
from pprint import PrettyPrinter

try:
	from comparator.common import *
except:
	from common import *


sift = cv2.ORB_create()
sift_f = lambda e: sift.detectAndCompute(e, None) #return (kp, des)
bf = cv2.BFMatcher(cv2.NORM_L1,crossCheck=False)


def distance(features1, features2):
	matches = bf.knnMatch(features1[1], features2[1], k=2)

	good = [m for m,n in matches if (m.distance < 0.75*n.distance)]

	if len(good) > 10:
		kp1 = features1[0]
		kp2 = features2[0]
		src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1,1,2)
		dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1,1,2)

		M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

		return len(mask)

	return -1


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
	results = [e for e in results if e[1] != -1]
	results.sort(key=lambda i: i[1], reverse=True)

	# return results[:size]
	return results


if __name__ == "__main__":
	t = time()
	target, candidates = parse_args()

	features = compute_features([target] + candidates, features)
	print(len(features[target][0]))

	print(time() - t)
	t = time()

	results = find_nn(target, candidates, features)
	print(time() - t)

	pp = PrettyPrinter(indent=4)
	pp.pprint(results)