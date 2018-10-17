"""
Implementation of texture based inpainting from Criminisi et al 2004

This script requires that 'opencv' and 'numpy' are installed within the
environment you are running the script in.

"""

# import sys
import numpy as np
import cv2
# from matplotlib import pyplot as plt

# The patch size should be a square of equivalent size to the smallest
# distinguishable texture element (texel).
# It must be an odd number
PATCH_SIZE = 9


def is_omega_empty(mask):
    """
    Returns 1 if there are no pixel left to be inpainted
    """
    return not np.isin(255, mask)

def calculate_fill_front(mask):
    """
    Calculate fill front, i.e the border of the area to be inpainted
    """
    fill_front = []
    for x in range(mask.shape[1]):
        for y in range(mask.shape[0]):
            if mask[y, x] == 255 and np.isin(0, mask[y-1:y+2, x-1:x+2]):
                fill_front.append((y, x))
    return fill_front

def calculate_priority(point, img_gray, mask, c):
    """
        Calculate the priority of a given patch given it's central point
    """

    return calculate_c(point, mask, c)*calculate_d(point, img_gray, mask)

def calculate_c(point, mask, c):
    """
        Calculate the confidence value of a given patch givent it's central point
    """
    delta = PATCH_SIZE//2
    confidences_sum = 0

    for y in range(point[0]-delta, point[0]+ delta +1):
        for x in range(point[1]-delta, point[1]+ delta +1):
            if mask[y, x] == 0:
                confidences_sum += c[y, x]
    return confidences_sum/(PATCH_SIZE**2)

def calculate_d(point, img_gray, mask):
    """
        Calculate the 'data' at a given point, using alpha as a regularization
        factor.
        Here we will use Scharr kernel to evaluate the derivative at a given
        point
    """

    kernel_x = np.array([[-3, 0, 3],
                         [-10, 0, 10],
                         [-3, 0, 3]])
    kernel_y = np.array([[-3, -10, -3],
                         [0, 0, 0],
                         [3, 10, 3]])

    alpha = 255

    isophote_x = np.sum(np.multiply(img_gray[point[0]-1:point[0]+2, point[1]-1:point[1]+2], kernel_x))
    isophote_y = np.sum(np.multiply(img_gray[point[0]-1:point[0]+2, point[1]-1:point[1]+2], kernel_y))

    normal_x = np.sum(np.multiply(mask[point[0]-1:point[0]+2, point[1]-1:point[1]+2], kernel_x))
    normal_y = np.sum(np.multiply(mask[point[0]-1:point[0]+2, point[1]-1:point[1]+2], kernel_y))
    return abs(isophote_x*normal_x + isophote_y*normal_y)/alpha

def color_points(image, points):
    """
        Color points in red in rgb image
    """
    for point in points:
        image[point] = (0, 0, 255)

def main():
    """
    Main function that will do the inpainting
    """


    # Preprocessing, creating the necessary data for our algorithm
    img = cv2.imread("landscape.jpg", 1)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    mask = cv2.imread("mask.jpg", 0)
    mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)[1]
    # c will be our confidence array C(p)
    c = 1 - np.float64(mask)
    p = np.zeros(c.shape)

    print(mask[390,390])
    # Main loop
    while not is_omega_empty(mask):
        fill_front = calculate_fill_front(mask)
        for point in fill_front:
            p[point] = calculate_priority(point, img_gray, mask, c)

if __name__ == "__main__":
    main()
