# Texture based inpainting

Implementation of a texture based inpainting algorithm from *Region filling and object removal by exemplar-based image inpainting* by Criminisi et al.

## Requirements

You will need to have installed in your environment :

* Python 3
* NumPy
* OpenCV 
* *Numba* (will probably be removed in final version)
* *Mapltolib* (currently used to display images, will be removed)

## Run the script

To run the script use the following scheme :

 python3 texture\_based\_inpainting.py IMAGE\_PATH MASK\_PATH

## Basic explanation of the algorithm

To simplify, the algorithm does the following steps :

Repeat the following until the image is entirely filled:

1. Find the *fill front*. The *fill front* is the border of our zone to be filled, our mask.
2. For every pixel in our *fill front*, calculate it's patch priority. A patch is a square centered on our pixel. It will be calculated with two terms, one representing our confidence in the patch value (C) and a data term depending on our patch data and to the curvature of the *fill front* (D) 
3. Find the patch with the biggest priority, we will fill this one
4. Calculate the difference between our patch and every patch in the picture using the Sum of Square Differences with all the pixels not in the mask/area to be filled.
5. Take the patch with the smallest difference to our patch, which we will call our *donor patch*. Then copy the data from our *donor patch* to our patch.

## Current state of the program

Currently the inpainting is not working correctly, nonetheless the algorithm is globally correct (in my humble opinion, as my knowledge of the algorithm is not perfect).
However some tweaks in the step 2 (priority calculation) and step 4 (calculating the difference between patches) are needed for a correct result.
