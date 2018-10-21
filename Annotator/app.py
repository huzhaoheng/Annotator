# coding=utf-8
import os
import sys
import json
from flask import Flask, jsonify, render_template, request
from PIL import Image
import numpy as np
import argparse
import requests
from difflib import SequenceMatcher
from helpers import *
import cv2
from flask_cors import CORS

parser = argparse.ArgumentParser(description='Server of Annotator')
parser.add_argument('-o','--objects', required=False, default='objects.txt',
						help='Specify the location of objects.txt file, you can run generateFiles.py to generate one')
parser.add_argument('-f','--frames', required=False, default='frames.json',
						help='Specify the location of frames.json file, you can run generateFiles.py to generate one')
parser.add_argument('-r','--result', required=False, default='result.json',
						help='Specify the location of result.json file, you can run generateFiles.py to generate one')
parser.add_argument('-c','--classes', required=False, default='classes.txt',
						help='Specify the location of classes.txt file, you can run generateFiles.py to generate one')

args = parser.parse_args()
# objectsPath = args['objects']
# framesPath = args['frames']
# resultPath = args['result']
# classesPath = args['classes']
objectsPath = args.objects
framesPath = args.frames
resultPath = args.result
classesPath = args.classes


app = Flask(__name__)
CORS(app)
# eng = matlab.engine.start_matlab()
# eng.addpath(os.getcwd(),nargout=0)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/getObjects')
def getObjects():
	data = open(objectsPath, 'r').readlines()
	objectPointer = int(data[0])
	objectList = parseListFile(data[1:])
	ret = {'objectPointer' : objectPointer, 'objectList' : objectList}
	return jsonify(elements = ret)


@app.route('/getFrames')
def getFrames():
	objectPath = json.loads(request.args.get('arg'))['object']
	data = json.load(open(framesPath, "r"))
	ret = data[objectPath]
	return jsonify(elements = ret)


@app.route('/getImageArray')
def getImageArray():
	object_path = json.loads(request.args.get('arg'))['object']
	frame = json.loads(request.args.get('arg'))['frame']

	# url = "http://192.168.1.2:8888/getImageArray"
	url = "az001.csl.illinois.edu:8889/getImageArray"
	params = {
		'object' : object_path,
		'frame' : frame
	}
	r = requests.get(url = url, params = params)
	data = r.json()['elements']
	print (sys.getsizeof(data))
	return jsonify(elements = data)

@app.route('/getAllClasses')
def getAllClasses():
	data = open(classesPath, 'r').readlines()
	classesList = parseListFile(data)
	ret = {'classesList' : classesList}
	return jsonify(elements = ret)


@app.route('/storeClassSelection')
def storeClassSelection():
	obj = json.loads(request.args.get('arg'))['object']
	className = json.loads(request.args.get('arg'))['class']
	allClasses = json.loads(request.args.get('arg'))['allClasses']

	with open(classesPath, 'w') as fp:
		for each in allClasses:
			fp.write(each + '\n')

	fp = open(resultPath, "r")
	data = json.load(fp)
	fp.close()

	_, parsedObject = parseObject(obj)
	objectName = parsedObject.split('/')[-1]

	data[objectName] = className

	fp = open(resultPath, "w")
	json.dump(data, fp)
	fp.close()

	return jsonify(elements = data)


@app.route('/updateObjectPointer')
def updateObjectPointer():
	objectPointer = json.loads(request.args.get('arg'))['objectPointer']
	data = open(objectsPath, 'r').readlines()
	data[0] = str(objectPointer) + '\n'
	with open(objectsPath, 'w') as fp:
		for each in data:
			fp.write(each.strip() + '\n')

	return jsonify(elements = {})


@app.route('/getTopKClasses')
def getTopKClasses():
	k = json.loads(request.args.get('arg'))['K']
	allClasses = json.loads(request.args.get('arg'))['allClasses']
	curr_object = json.loads(request.args.get('arg'))['curr_object']

	objectType, objectName = parseObject(curr_object.split('/')[-1])

	pairs = list(map(lambda x: [x, objectName], allClasses))
	similarities = sorted(pairs, key=lambda pair: SequenceMatcher(None, pair[0], pair[1]).ratio(), reverse=True)
	classes = [ s[0] for s in similarities[:k] ]

	return jsonify(elements = classes)


if __name__ == '__main__':
	app.debug = False
	app.run(host='0.0.0.0', port=8888)
