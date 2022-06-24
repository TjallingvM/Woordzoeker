import cv2 
import pytesseract
import numpy as np
import os

# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# noise removal
def remove_noise(image):
    return cv2.medianBlur(image,5)
 
#thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[2]

#dilation
def dilate(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.dilate(image, kernel, iterations = 1)
    
#erosion
def erode(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.erode(image, kernel, iterations = 1)

#canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)

def getText():
    work_dir = os.getcwd()
    file_name = "wrdsrch1.jpg"
    img = cv2.imread(work_dir+"/Puzzels/"+file_name)

    # Adding custom options
    custom_config = r'--oem 3 --psm 6'

    #cv2.imshow("first", img)
    img = get_grayscale(img)
    #img = remove_noise(img)
    #img = canny(img)
    #cv2.imshow("out", img)
    #cv2.waitKey(0)
    text = pytesseract.image_to_string(img, config=custom_config)
    return text



