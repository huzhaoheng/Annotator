import os
import sys
import json
import numpy as np
from helpers import parseObject
import numpy as np

def generateObjectList(root):
	accessedObjects, objects = {}, {}
	index = 0
	videoList = os.listdir(root)
	for video in videoList:
		if video != ".DS_Store":
			videoPath = os.path.join(root, video)
			shotList = os.listdir(videoPath)
			for shot in shotList:
				if shot != ".DS_Store":
					if len(shot) == 3:
						try:
							allDigits = int(shot)
							shotPath = os.path.join(videoPath, shot)
							objectList = os.listdir(shotPath)
							for objectDir in objectList:
								if objectDir != ".DS_Store":
									_, parsedObject = parseObject(objectDir)
									if parsedObject not in accessedObjects:
										accessedObjects[parsedObject] = 1
										objectPath = os.path.join(shotPath, objectDir)
										objects[index] = objectPath
										index += 1
									else:
										accessedObjects[parsedObject] += 1
						except Exception as e:
							continue



	with open('objects.txt', 'w') as fp:
		fp.write('0\n')
		objectList = list(objects.values())
		for each in objectList:
			fp.write(each + '\n')

	return objectList

def generateFrameList(objectList, mode = 'random'):
	if mode == 'random':
		generateRandomFrameList(objectList)
	elif mode == 'sorted':
		generateSortedFrameList(objectList)
	else:
		return

def generateRandomFrameList(objectList):
	ret = {}
	for each in objectList:
		print ('Object:', each)
		ret[each] = {}
		fileList = os.listdir(each)
		dic = {}
		arr = []
		for file in fileList:
			if file.endswith('.bin'):
				print ('File:', file)
				arr.append(file)

		for index, file in enumerate(arr):
			ret[each][index] = file.rstrip('.tiff.bin')

	with open("frames.json", "w") as fp:
		json.dump(ret, fp)
	
	return ret

def generateSortedFrameList(objectList):
	ret = {}
	for each in objectList:
		print ('Object:', each)
		ret[each] = {}
		fileList = os.listdir(each)
		dic = {}

		for file in fileList:
			if file.endswith('.bin'):
				print ('File:', file)
				path = '/'.join([each, file])
				# res = np.array(eng.read_segmentation_bin(path))
				res = readMask(path)
				ones = np.count_nonzero(res == 1)
				if ones not in dic:
					dic[ones] = [file.rstrip('.tiff.bin')]
				else:
					dic[ones].append(file.rstrip('.tiff.bin'))

		counts = list(dic.keys())
		counts.sort(reverse=True)
		arr = []
		for count in counts:
			for file in dic[count]:
				arr.append(file)

		for index, file in enumerate(arr):
			ret[each][index] = file

	with open("frames.json", "w") as fp:
		json.dump(ret, fp)
	
	return ret

def generateClassesList():
	classes = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush']
	with open('classes.txt', 'w') as fp:
		for each in classes:
			fp.write(each + '\n')
		
def createNecessaryFiles():
	json.dump({}, open("result.json", "w"))
	json.dump({}, open("frames.json", "w"))
	open("classes.txt", "w").close()
	open("objects.txt", "w").close()
	

if __name__ == '__main__':
	root = sys.argv[1]
	createNecessaryFiles()
	generateClassesList()
	objectList = generateObjectList(root)
	framesDict = generateFrameList(objectList, mode = 'random')