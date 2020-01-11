import numpy as np
from PIL import ImageGrab
import cv2
import time
import os
import sys
sys.path.insert(0, 'Desktop/gta5/')

from grabscreen import grab_screen
from getkeys import key_check

from numpy import ones,vstack
from numpy.linalg import lstsq
from statistics import mean

def keys_to_output(keys):
	#[W,A,D]
	output = [0, 0, 0]

	if 'A' in keys:
		output[1] = 1
	elif 'D' in keys:
		output[2] = 1
	elif 'W' in keys:
		output[0] = 1

	return output

file_name = 'C:/Users/Helik Thacker/Desktop/gta5/training_data.npy'

print(os.path.isfile(file_name))
   
if os.path.isfile(file_name):
	training_data = list(np.load(file_name, allow_pickle=True))
else:
	training_data = []

# =============================================================================
# new_data = np.mat(np.load(file_name, allow_pickle=True))
# if len(new_file) == 0:
#     new_file = new_data
# else:
#     new_file = np.concatenate((new_file, new_data), axis=0)
# =============================================================================

def main():
    for i in list(range(4))[::-1]:
        print(i+1)
        time.sleep(1)


    last_time = time.time()


    paused = False
    while True:
        if not paused:
            screen = grab_screen(region=(0,40,800,640))
            last_time = time.time()
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
            screen = cv2.resize(screen, (80, 60))
            keys = key_check()
            output = keys_to_output(keys)
            training_data.append([screen, output])
            print(len(training_data))
            if len(training_data) % 100 == 0:
                np.save(file_name, training_data)
		
        keys = key_check()
        if 'T' in keys:
            if paused:
                paused = False
                print('unpaused')
                time.sleep(1)
            else:
                print('pausing')
                paused = True
                time.sleep(1)

main()
