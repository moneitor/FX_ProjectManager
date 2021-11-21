from exif import Image
import cv2
import os
import numpy as np
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Uncomment the next line to dissable logging
#logging.disable(logging.CRITICAL)


cwd = os.path.dirname(os.path.realpath(__file__))
hdr_folder = os.path.join(cwd, "JPGS2")

def read_and_store_data(folder):
	"""
	Extract the exposure time and the brigthness value of the
	pictures stored inside the folder argument.
	Returns two lists with the path to the files and 
	the exposure time as seconds, 
	:images: list of images
	:exposures:  list of exposure of each picture in seconds

	"""

	files = os.listdir(folder)

	images = []
	exposures = []

	for frame in files:
		testFrame = os.path.join(hdr_folder, frame)

		im = cv2.imread(testFrame)
		images.append(im)

		with open(testFrame, "rb") as file:
			frame = Image(file)

		exposures.append(frame.exposure_time)



	exposures = np.array(exposures, dtype=np.float32)
	
	return images, exposures

	
def main(folder):
	"""
	Reads and process the images given by the read_and_store_data function
	and creates a new hdr file
	
	"""
	images, times = read_and_store_data(folder)
	
	"""
	Align the pictures using the brightest spots, it 
	doesn't matter the exposures are different
	"""
	logging.debug("Aligning pictures")
	alignMTB = cv2.createAlignMTB()
	alignMTB.process(images, images)
	
	"""
	Finds the camera response function
	"""
	logging.debug("Calculating Camera response function")
	calibrate = cv2.createCalibrateDebevec()
	response = calibrate.process(images, times)

	"""
	Putting everything together into a single hdr image
	"""
	logging.debug("Merging images...")
	merge = cv2.createMergeDebevec()
	hdr = merge.process(images, times, response)
	
	"""
	Saving the hdr file into the specified folder
	"""
	hdr_folder = os.path.join(cwd, "HDR")
	logging.debug("Saving HDR at {}....".format(hdr_folder))
	cv2.imwrite(hdr_folder + "/file2.hdr", hdr)
	logging.debug("Saved file")



if __name__ == "__main__":
	main(hdr_folder)


	


