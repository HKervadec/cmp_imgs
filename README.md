# Compare Images
The goal of this project is to create a image comparator, to help find duplicates and similar images in an image folder.

At the moment, it is using the ORB feature extractor with a Ransac algorithm to detect similar images.
It will output a sorted list of possible matches. The threshold is still fairly low during development, to maintain a high recall.


## Use
### Command line
Just type
```bash
./comparator/comparator.py <target> <folder>
./comparator/orb.py <target> <folder>
```
`target` is the file we want to compare, and `folder` is where we want to look for duplicates. It is not recursive yet.

It will then print a sorted list of the matched images, with the best matching first. A higher score means a higher match.

### GUI to display results
The syntax is similar
```bash
./interface.py <target> <folder>
```
It will display the results in the following way:

![window](readme_imgs/app.png)

## Todos and stuff
### Todo
* Support recursion in folders
* Use a more robust framework for the script parameters
* Find a way to use FLANN in a multi-process way for knn matching
* Handle mirrored images
* Tweak thresholds when matching features
* Handle case for images without features
* Save features in a file to speedup mutltiple searchs

### Done
* Profile the script
* Find a usable feature extractor to improve performances
	* ORB is used at the moment.
	* Started with SIFT, but really really slow during generation and matching.
* Display score in GUI

### Dropped
* Add option for the number of nearest neighbors we want to have
	* The algorithm can now make a decision, so not useful anymore