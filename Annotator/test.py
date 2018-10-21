# import os
# import matlab.engine
# from PIL import Image
# import numpy as np
# from matplotlib import pyplot as plt


# eng = matlab.engine.start_matlab()
# eng.addpath(os.getcwd(),nargout=0)
# print ("engine started")
# maskPath = '/Users/kexin/Desktop/dataset/exl_3_ext/001/Prop_p_idol_case_s_000000000205314/000000.tiff.bin'
# imagePath = '/Users/kexin/Desktop/dataset/exl_3_ext/001/Prop_p_idol_case_s_000000000205314/000000.tiff'
# im = Image.open(imagePath)
# imarray = np.array(im)
# # plt.imshow(imarray)
# # plt.show()

# res = eng.draw_seg(eng.read_segmentation_bin(maskPath), imagePath)
# rgb_arr = np.array(res) * 255
# plt.imshow(rgb_arr)
# plt.show()
# # im_rgba = np.dstack((rgb_arr[:,:,0], rgb_arr[:,:,1], rgb_arr[:,:,2], imarray[:,:,3]))
# im_rgba = np.dstack((rgb_arr[:,:,0], rgb_arr[:,:,1], rgb_arr[:,:,2], imarray[:,:,3] * 255))
# print (im_rgba.shape)
# plt.imshow(im_rgba)
# plt.show()



import cv2
import matplotlib.pyplot as plt
import numpy as np

def d2b(d, n):
    d = np.array(d)
    d = np.reshape(d, (1, -1))
    power = np.flipud(2**np.arange(n))

    g = np.zeros((np.shape(d)[1], n))

    for i, num in enumerate(d[0]):
        g[i] = num * np.ones((1,n))
    b = np.floor((g%(2*power))/power)
    return b

maskPath = '/Users/kexin/Desktop/dataset/exl_3_ext/001/Prop_p_idol_case_s_000000000205314/000000.tiff.bin'
imagePath = '/Users/kexin/Desktop/dataset/exl_3_ext/001/Prop_p_idol_case_s_000000000205314/000000.tiff'

with open(maskPath, 'r') as f:
	data = f.read()
	# data = np.fromfile(f, dtype = np.int)

data = d2b(data, 8)
print(data.shape)
# plt.imshow(mask)
# plt.show()

