import numpy as np

def parseObject(objectDir):
	splited = objectDir.split("_")
	prefix = splited[0]
	if prefix in ['Ped', 'Vehicle']:
		return prefix, '_'.join(splited[:2])
	else:
		return prefix, '_'.join(splited[:-1])

def stripHelper(row):
	return row.strip()

def parseListFile(data):
	result = map(stripHelper, data)
	return list(result)

def readMask(maskPath):
	Bytes = np.fromfile(maskPath, dtype="uint8")
	Bits = np.unpackbits(Bytes)
	tmp = np.fliplr(np.reshape(Bits, [-1,8]))
	mask = np.reshape(tmp, [800, 1280])
	return mask