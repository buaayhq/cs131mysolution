import math

import numpy as np
from PIL import Image
from skimage import color, io


def load(image_path):
    """Loads an image from a file path.

    HINT: Look up `skimage.io.imread()` function.

    Args:
        image_path: file path to the image.

    Returns:
        out: numpy array of shape(image_height, image_width, 3).
    """
    out = None

    ### YOUR CODE HERE
    # Use skimage io.imread
    out = io.imread(image_path)
    ### END YOUR CODE

    # Let's convert the image to be between the correct range.
    out = out.astype(np.float64) / 255
    return out


def dim_image(image):
    """Change the value of every pixel by following

                        x_n = 0.5*x_p^2

    where x_n is the new value and x_p is the original value.

    Args:
        image: numpy array of shape(image_height, image_width, 3).

    Returns:
        out: numpy array of shape(image_height, image_width, 3).
    """

    out = None

    ### YOUR CODE HERE
    out = 0.5*np.square(image)
    ### END YOUR CODE

    return out


def convert_to_grey_scale(image):
    """Change image to gray scale.

    HINT: Look at `skimage.color` library to see if there is a function
    there you can use.

    Args:
        image: numpy array of shape(image_height, image_width, 3).

    Returns:
        out: numpy array of shape(image_height, image_width).
    """
    out = None

    ### YOUR CODE HERE
    out = color.rgb2gray(image)
    ### END YOUR CODE

    return out


def rgb_exclusion(image, channel):
    """Return image **excluding** the rgb channel specified

    Args:
        image: numpy array of shape(image_height, image_width, 3).
        channel: str specifying the channel. Can be either "R", "G" or "B".

    Returns:
        out: numpy array of shape(image_height, image_width, 3).
    """

    out = None
    out = np.array(image)
    ### YOUR CODE HERE
    if channel == "R":
        out[:,:,0] = 0
    elif channel == "G":
        out[:,:,1] = 0
    elif channel == "B":
        out[:,:,2] = 0
    ### END YOUR CODE

    return out


def lab_decomposition(image, channel):
    """Decomposes the image into LAB and only returns the channel specified.

    Args:
        image: numpy array of shape(image_height, image_width, 3).
        channel: str specifying the channel. Can be either "L", "A" or "B".

    Returns:
        out: numpy array of shape(image_height, image_width).
    """

    lab = color.rgb2lab(image)
    out = None

    ### YOUR CODE HERE
    if channel == "L":
        out = lab[:,:,0]
    elif channel == "A":
        out = lab[:,:,1]
    elif channel == "B":
        out = lab[:,:,2]
    ### END YOUR CODE
    return out


def hsv_decomposition(image, channel='H'):
    """Decomposes the image into HSV and only returns the channel specified.

    Args:
        image: numpy array of shape(image_height, image_width, 3).
        channel: str specifying the channel. Can be either "H", "S" or "V".

    Returns:
        out: numpy array of shape(image_height, image_width).
    """

    hsv = color.rgb2hsv(image)
    out = None

    ### YOUR CODE HERE
    if channel == "H":
        out = hsv[:,:,0]
    elif channel == "S":
        out = hsv[:,:,1]
    elif channel == "V":
        out = hsv[:,:,2]
    ### END YOUR CODE

    return out


def mix_images(image1, image2, channel1, channel2):
    """Combines image1 and image2 by taking the left half of image1
    and the right half of image2. The final combination also excludes
    channel1 from image1 and channel2 from image2 for each image.

    HINTS: Use `rgb_exclusion()` you implemented earlier as a helper
    function. Also look up `np.concatenate()` to help you combine images.

    Args:
        image1: numpy array of shape(image_height, image_width, 3).
        image2: numpy array of shape(image_height, image_width, 3).
        channel1: str specifying channel used for image1.
        channel2: str specifying channel used for image2.

    Returns:
        out: numpy array of shape(image_height, image_width, 3).
    """

    out = None
    ### YOUR CODE HERE
    rgb1 = np.array(image1)
    im1Shape = rgb1.shape
    leftHalf = rgb1[:,:im1Shape[1]//2,:]
    leftHalfExclude = rgb_exclusion(leftHalf,channel1)
    print(leftHalfExclude.shape)
    rgb2 = np.array(image2)
    im2Shape = rgb2.shape
    rightHalf = rgb2[:,im2Shape[1]//2:,:]
    rightHalfExclude = rgb_exclusion(rightHalf,channel2)
    print(rightHalfExclude.shape)
    out = np.concatenate((leftHalfExclude,rightHalfExclude), axis=1)
    ### END YOUR CODE

    return out


def mix_quadrants(image):
    """THIS IS AN EXTRA CREDIT FUNCTION.

    This function takes an image, and performs a different operation
    to each of the 4 quadrants of the image. Then it combines the 4
    quadrants back together.

    Here are the 4 operations you should perform on the 4 quadrants:
        Top left quadrant: Remove the 'R' channel using `rgb_exclusion()`.
        Top right quadrant: Dim the quadrant using `dim_image()`.
        Bottom left quadrant: Brighthen the quadrant using the function:
            x_n = x_p^0.5
        Bottom right quadrant: Remove the 'R' channel using `rgb_exclusion()`.

    Args:
        image1: numpy array of shape(image_height, image_width, 3).

    Returns:
        out: numpy array of shape(image_height, image_width, 3).
    """
    out = None

    ### YOUR CODE HERE
    rgb = np.array(image)
    rgbShape = rgb.shape 
    topLeft = rgb[:rgbShape[0]//2,:rgbShape[1]//2,:]
    topRight = rgb[:rgbShape[0]//2,rgbShape[1]//2:,:]
    bottomLeft = rgb[rgbShape[0]//2:,:rgbShape[1]//2,:]
    bottomRight = rgb[rgbShape[0]//2:,rgbShape[1]//2:,:]

    topLeft1 = rgb_exclusion(topLeft, "R")
    topRight1 = dim_image(topRight)
    bottomLeft1 = np.sqrt(bottomLeft)
    bottomRight1 = rgb_exclusion(bottomRight, "R")

    top = np.concatenate((topLeft1, topRight1), axis=1)
    bottom = np.concatenate((bottomLeft1, bottomRight1), axis=1)
    out = np.concatenate((top, bottom), axis=0)

    ### END YOUR CODE

    return out
