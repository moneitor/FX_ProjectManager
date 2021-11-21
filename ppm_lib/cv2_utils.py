import os
import sys
import glob
import pprint as pp
import numpy as np
import cv2
import rawpy 
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import imageio

        
    
def show_cv2_image(img):
    while True:
        cv2.imshow("Texture", img)
        if cv2.waitKey(0) & 0xFF==27:
            break
    cv2.destroyAllWindows()


### WORK IN PROGRESS#################
'''
path = "../DATA/img.dng"

with rawpy.imread(path) as raw:
    img = raw.postprocess()
    
img = img[:,:,::-1]
img = img.astype("float32")


new_name = "../DATA/img.exr"

#norm_image = cv2.normalize(img, None, alpha = 0, beta = 1, norm_type = cv2.NORM_MINMAX, dtype = cv2.CV_32F)

cv2.imwrite(new_name, img  )
'''

