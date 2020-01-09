import numpy as np
from PIL import ImageGrab
import cv2
import time
import sys
sys.path.insert(0, '%cd%')
from directkeys import PressKey, ReleaseKey, W, A, S, D

def process_img(original_image):
    #convert to gray
    processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    #edge detection
    processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300)
    return processed_img    

def main():
        
    for i in list(range(4))[::-1]:
        print(i+1)
        time.sleep(1)
    
    last_time = time.time()
    while(True):
        screen =np.array(ImageGrab.grab(bbox = (0, 40, 800, 640)))
        #printscreen_numpy = np.array(printscreen_pil.getdata(), dtype='uint8').reshape((printscreen_pil.size[1], printscreen_pil.size[0], 3))
        new_screen = process_img(screen)
    
        # =============================================================================
        #     print('down')
        #     PressKey(W)
        #     time.sleep(3)
        #     print('up')
        #     ReleaseKey(W)
        #     
        #     print('down')
        #     PressKey(S)
        #     time.sleep(3)
        #     print('up')
        #     ReleaseKey(S)
        # =============================================================================
        
        print('Loop took {} seconds'.format(time.time()-last_time))
        last_time = time.time()
        
        cv2.imshow('window', new_screen)
        #cv2.imshow('window2', cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
        
main()
