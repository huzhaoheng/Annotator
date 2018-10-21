import json
import cv2
import numpy as np
from flask import Flask, jsonify, render_template, request
from helpers import readMask

app = Flask(__name__)

@app.route('/getImageArray')
def getImageArray():
	object_path = json.loads(request.args.get('arg'))['object']
	frame = json.loads(request.args.get('arg'))['frame']
	tiff_postfix = ".tiff"
	imagePath = '/'.join([object_path, frame + tiff_postfix])

	im = cv2.imread(imagePath, cv2.IMREAD_UNCHANGED)
	shape = im.shape
	im_rgb = np.ascontiguousarray(im[:,:,:3])

	# maskPath = imagePath + '.bin'
	# Bytes = np.fromfile(maskPath, dtype="uint8")
	# Bits = np.unpackbits(Bytes)
	# tmp = np.fliplr(np.reshape(Bits, [-1,8]))
	# mask = np.reshape(tmp, [800, 1280])
	mask = readMask(imagePath+'.bin')

	im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cv2.drawContours(im_rgb, contours, -1, (255,0,0), 5)

	imarray_RGBA = np.stack((im_rgb[:,:,0], im_rgb[:,:,1], im_rgb[:,:,2], im[:,:,3]), axis = -1)

	ret = {'height' : shape[0], 'width' : shape[1], 'array' : imarray_RGBA.flatten().tolist()}
	return jsonify(elements = ret)


@app.route('/test')
def test():
	print ('test function running')

if __name__ == '__main__':
	app.debug = False
	app.run(host='0.0.0.0', port=8888)
