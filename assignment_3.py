# Edward Jesinsky
# CS-7375 Assignment 3: OpenCV Image Processing

import cv2

if __name__ == "__main__":
  fighter_5_orig = cv2.imread("fighter_noise_5.jpg")

  # perform smoothing (make blurry)
  fighter_5_blurry = cv2.GaussianBlur(fighter_5_orig, (9,9), 0) # gaussian (kernel size, sigma)
  cv2.imwrite("fighter_noise_5_blurry.jpg", fighter_5_blurry)

  # convert to grayscale (better edge detection)
  fighter_5_gray = cv2.cvtColor(fighter_5_blurry, cv2.COLOR_BGR2GRAY)
  
  # edge detection (sobel)
  fighter_5_edgy = cv2.Sobel(src=fighter_5_gray, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5) # x and y
  cv2.imwrite("fighter_noise_5_edgy.jpg", fighter_5_edgy)
  
  fighter_10_orig = cv2.imread("fighter_noise_10.jpg")

  # perform smoothing (make blurry)
  fighter_10_blurry = cv2.bilateralFilter(fighter_10_orig, 2, 75, 75) # bilateral filter (diameter, sigma color, sigma space)
  cv2.imwrite("fighter_noise_10_blurry.jpg", fighter_10_blurry)

  # convert to grayscale (better edge detection)
  fighter_10_gray = cv2.cvtColor(fighter_10_blurry, cv2.COLOR_BGR2GRAY)
  
  # edge detection (canny)
  fighter_10_edgy = cv2.Canny(image=fighter_10_gray, threshold1=255/3, threshold2=255)
  cv2.imwrite("fighter_noise_10_edgy.jpg", fighter_10_edgy)
  
