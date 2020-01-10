import numpy as np
from PIL import ImageGrab
import cv2
import time
import sys
sys.path.insert(0, 'Desktop/windows tf testing/')
from directkeys import PressKey, ReleaseKey, W, A, S, D

# =============================================================================
# def make_coordinates(image, line_parameters):
#     slope, intercept = line_parameters
#     y1 = image.shape[0]
#     y2 = int(y1*(3/5))
#     x1 = int((y1 - intercept)/slope)
#     x2 = int((y2 - intercept)/slope)
#     return np.array([x1, y1, x2, y2])    
#     
# def average_slope_intercept(image, lines):
#     left_fit = []
#     right_fit = []
#     for line in lines:
#         x1, y1, x2, y2 = line.reshape(4)
#         #if(x1 >= 0 and x1 < image.shape[1] and x2 >= 0 and x2 < image.shape[1] and y1 >= 0 and y1 < image.shape[0] and y2 >= 0 and y2 < image.shape[0]):
#         #    continue
#         parameters = np.polyfit((x1, x2), (y1,y2), 1)
#         slope = parameters[0]
#         intercept = parameters[1]
#         if slope >= 0.3 or slope <= -0.3:
#             if slope < 0:
#                 left_fit.append((slope, intercept))
#             else:
#                 right_fit.append((slope, intercept))
#     
#     left_fit_average = np.average(left_fit, axis=0)
#     right_fit_average = np.average(right_fit, axis=0)
#     
#     left_line = make_coordinates(image, left_fit_average)
#     right_line = make_coordinates(image, right_fit_average)
# 
#     return np.array([left_line, right_line])
# 
# def canny(image):
#     gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
#     blur = cv2.GaussianBlur(gray, (5, 5), 0)
#     canny = cv2.Canny(blur, 100, 200)
#     return canny    
# 
# def display_lines(image, lines):
#     line_image = np.zeros_like(image)
#     if lines is not None:
#         for line in lines:
#             x1, y1, x2, y2 = line.reshape(4)
#             cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
#     #if lines is not None:
#     #    for x1, y1, x2, y2 in lines:
#     #        cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
#     return line_image
# =============================================================================

def make_coordinates(image, line_parameters):
    slope, intercept = line_parameters
    y1 = image.shape[0]
    y2 = int(y1*(3/5))
    x1 = int((y1 - intercept)/slope)
    x2 = int((y2 - intercept)/slope)
    return np.array([x1, y1, x2, y2]) 

def average_slope_intercept_left(image, lines):
    left_fit = []
    if lines is not None:
        for line in lines:
            #print(line)
            x1, y1, x2, y2 = line.reshape(4)
            parameters = np.polyfit((x1,x2), (y1,y2), 1)
            slope = parameters[0]
            intercept = parameters[1]
            if slope >= 0.3 or slope <= -0.3:
                if slope < 0:
                    left_fit.append((slope, intercept))
        
        left_fit_average_flag = False
        if(len(left_fit) > 0):
            left_fit_average = np.average(left_fit, axis=0)
            left_fit_average_flag = True
            
        if left_fit_average_flag == True:
            left_line = make_coordinates(image, left_fit_average)    
            return left_line
        
def average_slope_intercept_right(image, lines):
    right_fit = []
    if lines is not None:
        for line in lines:
            #print(line)
            x1, y1, x2, y2 = line.reshape(4)
            parameters = np.polyfit((x1,x2), (y1,y2), 1)
            slope = parameters[0]
            intercept = parameters[1]
            if slope >= 0.3 or slope <= -0.3:
                if slope > 0:
                    right_fit.append((slope, intercept))
        
        right_fit_average_flag = False
        if(len(right_fit) > 0):
            right_fit_average = np.average(right_fit, axis=0)
            right_fit_average_flag = True
            
        if right_fit_average_flag == True:
            right_line = make_coordinates(image, right_fit_average)    
            return right_line

def average_slope_intercept(image, lines):
    left_line = average_slope_intercept_left(image, lines)
    right_line = average_slope_intercept_right(image, lines)
    return np.array([left_line, right_line])

def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    canny = cv2.Canny(blur, 50, 150)
    return canny    

def display_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
    #if lines is not None:
    #    for x1, y1, x2, y2 in lines:
    #        cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
    return line_image

            
def region_of_interest(image):
    height = image.shape[0]
    polygons = np.array([[[10,500],[10,300], [300,200], [500,200], [800,300], [800,500]]])
    #polygons = np.array([
    #    [[10, 500], [10, 300], [300, 225], [500, 225], [800, 300], [800, 500]]
    #    ])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygons, 255)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image

# =============================================================================
# def process_img(original_image):
#     lane_image = np.copy(original_image)
#     canny_image = canny(lane_image)
#     cropped_image = region_of_interest(canny_image)
#     lines = cv2.HoughLinesP(cropped_image, 2, np.pi/180, 100, np.array([]), minLineLength=45, maxLineGap=5)    
#     average_lines = average_slope_intercept(lane_image, lines)
#     line_image = display_lines(lane_image, average_lines)
#     combo_image = cv2.addWeighted(lane_image, 0.8, line_image, 1, 1)
#     return combo_image 
# 
# =============================================================================
    #vertices = np.array([[10, 500], [10, 300], [300, 200], [500, 200], [800, 300], [800, 500]], dtype=np.int32)
    #processed_img = roi(original_image, [vertices]) #try to do this after converting to gray scale but this works temporarily
    #processed_img = cv2.cvtColor(processed_img, cv2.COLOR_BGR2GRAY)
    ##cv2.equalizeHist(processed_img)
    #processed_img = cv2.GaussianBlur(processed_img, (5, 5), 0)
    #processed_img = cv2.Canny(processed_img, threshold1=50, threshold2=150)
    #lines = cv2.HoughLinesP(processed_img, 1, np.pi/180, 180, np.array([]), 100, 5)
    #draw_lines(processed_img, lines)
    #return processed_img

def main():    
    last_time = time.time()
    generations = 0
    flag = False
    while(True):
        generations = generations + 1
        screen = np.array(ImageGrab.grab(bbox = (0, 40, 800, 640)))
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
        #new_screen = process_img(screen)
    
        lane_image = np.copy(screen)
        canny_image = canny(lane_image)
        cropped_image = region_of_interest(canny_image)
        lines = cv2.HoughLinesP(cropped_image, 2, np.pi/180, 100, np.array([]), minLineLength=60, maxLineGap=5)
        
        templineimage = display_lines(lane_image, lines)
        
        average_lines = average_slope_intercept(lane_image, lines)
        
        #print(len(average_lines))
        try:
            line_image = display_lines(lane_image, average_lines)
            store_average_lines = average_lines
            flag = True
        except:
            if generations > 100 or flag == False: #offroad
                line_image = display_lines(lane_image, lines)
                generations = 0
                flag = False
            else:
                line_image = display_lines(lane_image, store_average_lines)
                
        combo_image = cv2.addWeighted(lane_image, 0.8, line_image, 1, 1)
    
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
        
        cv2.imshow('final', combo_image)
        cv2.imshow('line', templineimage)
        cv2.imshow('cropped', cropped_image)
        cv2.imshow('canny', canny_image)
        #cv2.imshow('window2', cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
        
main()
