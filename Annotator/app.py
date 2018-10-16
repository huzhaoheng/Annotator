# coding=utf-8
import os
import sys
import json
from flask import Flask, jsonify, render_template, request
from pymatbridge import Matlab


app = Flask(__name__)
matlabAppPath = '/Applications/MATLAB_R2016a.app/bin/matlab'
matlabFilePath = 'read_segmentation_bin.m'
mlab = Matlab(executable=matlabAppPath)
mlab.start()


@app.route('/')
def home():
	return render_template('home.html')

@app.route('/getObjects')
def getObjects():
	root = sys.argv[1]
	# root = 'C:\\Users\\Zhaoheng Hu\\Desktop\\data'
	accessed, ret = {}, {}
	index = 0
	for path, subdirs, files in os.walk(root):
		for name in files:
			curr_path = os.path.join(path, '')
			if curr_path not in accessed:
				ret[index] = curr_path
				accessed[curr_path] = True
				index += 1
				break

	return jsonify(elements = ret)


@app.route('/getFrames')
def getFrames():
	object_path = json.loads(request.args.get('arg'))['object']
	file_list = os.listdir(object_path)
	ret = {}
	#-------------TO DO: rewrite frame ordering algorithm-----------------------
	for index, file in enumerate(file_list):
		ret[index] = file
	#---------------------------------------------------------------------------
	return jsonify(elements = ret)


@app.route('/getBitMap')
def getBitMap():
	object_path = json.loads(request.args.get('arg'))['object']
	frame = json.loads(request.args.get('arg'))['frame']
	path = '/'.join([object_path, frame])
	"""
	By default the host is localhost and the port is 4000. This can be changed, e.g.

	mlab = Matlab(matlab='/Applications/MATLAB_R2011a.app/bin/matlab',
					host='192.168.0.1', port=5151)
	"""
	
	res = mlab.run_func(matlabFilePath, path)
	ret = res['result'].tolist()

	return jsonify(elements = ret)


if __name__ == '__main__':
	app.debug = True
	app.run(host='127.0.0.1', port=8888)
