#################################################################
# FILE : image_editor.py
# WRITER : amitai turkel

#################################################################

##############################################################################
#                                   Imports                                  #
##############################################################################
import os

from ex5_helper import *
from typing import Optional
import copy
import math
import ex5_helper
import sys
from pathlib import Path

##############################################################################
#                                  Functions                                 #
##############################################################################

import os
import copy
import math
import sys
from pathlib import Path

import ex5_helper


def separate_channels(image_with_colors: list) -> list:
    """Separates the channels of an image and rearranges them.

    Args:
        image_with_colors (list): The image matrix with channels.

    Returns:
        list: The rearranged matrix with channels.

    """
    color_on_rows_on_column_list = []
    for color in range(len(image_with_colors[0][0])):
        color_in_a_row_list = []
        for row in range(len(image_with_colors)):
            color_in_a_column_list = []
            for column in range(len(image_with_colors[0])):
                color_in_a_column_list.append(image_with_colors[row][column][color])
            color_in_a_row_list.append(color_in_a_column_list)
        color_on_rows_on_column_list.append(color_in_a_row_list)
    return color_on_rows_on_column_list


def combine_channels(channels: list) -> list:
    """Combines the channels of an image and rearranges them.

    Args:
        channels (list): The matrix with channels.

    Returns:
        list: The rearranged image matrix with channels.

    """
    image_with_color = []
    for row in range(len(channels[0])):
        image_with_color_row = []
        for column in range(len(channels[0][0])):
            image_with_color_column = []
            for color in range(len(channels)):
                image_with_color_column.append(channels[color][row][column])
            image_with_color_row.append(image_with_color_column)
        image_with_color.append(image_with_color_row)
    return image_with_color


def make_square_matrix(size: int) -> list:
    """Creates a square matrix of the given size.

    Args:
        size (int): The size of the matrix.

    Returns:
        list: The square matrix.

    """
    matrix = []
    for row in range(size):
        column_list = []
        for column in range(size):
            column_list.append([])
        matrix.append(column_list)
    return matrix


def make_matrix(rows: int, columns: int) -> list:
    """Creates a matrix with the given number of rows and columns.

    Args:
        rows (int): The number of rows in the matrix.
        columns (int): The number of columns in the matrix.

    Returns:
        list: The matrix.

    """
    matrix = []
    for row in range(rows):
        column_list = []
        for column in range(columns):
            column_list.append([])
        matrix.append(column_list)
    return matrix


def average_color_to_black_white(red, green, blue: float) -> int:
    """Calculates the average of three colors and converts it to black and white.

    Args:
        red (float): The red color value.
        green (float): The green color value.
        blue (float): The blue color value.

    Returns:
        int: The converted black and white color value.

    """
    black_white = round(float(red) * 0.299 + float(green) * 0.587 + float(blue) * 0.114)
    return black_white


def kernel_in_limit(sum_of_kernel: float) -> int:
    """Checks if the sum of the kernel is within the limit (0-255).

    Args:
        sum_of_kernel (float): The sum of the kernel values.

    Returns:
        int: The adjusted sum within the limit.

    """
    if sum_of_kernel > 255:
        return 255
    elif sum_of_kernel < 0:
        return 0
    else:
        return round(sum_of_kernel)


def RGB2grayscale(colored_image: list) -> list:
    """Converts an RGB image to grayscale.

    Args:
        colored_image (list): The RGB image matrix.

    Returns:
        list: The grayscale image matrix.

    """
    grayscale_image = copy.deepcopy(colored_image)
    for row in range(len(grayscale_image)):
        for column in range(len(grayscale_image[0])):
            average = average_color_to_black_white(grayscale_image[row][column][0], grayscale_image[row][column][1], grayscale_image[row][column][2])
            grayscale_image[row][column] = [average, average, average]
    return grayscale_image


def blur(image: list) -> list:
    """Applies a blur effect to an image.

    Args:
        image (list): The image matrix.

    Returns:
        list: The blurred image matrix.

    """
    kernel = [
        [1 / 9, 1 / 9, 1 / 9],
        [1 / 9, 1 / 9, 1 / 9],
        [1 / 9, 1 / 9, 1 / 9]
    ]
    kernel_size = len(kernel)
    kernel_radius = kernel_size // 2
    image_with_blur = copy.deepcopy(image)
    for row in range(kernel_radius, len(image) - kernel_radius):
        for column in range(kernel_radius, len(image[0]) - kernel_radius):
            sum_of_kernel = [0, 0, 0]
            for kernel_row in range(kernel_size):
                for kernel_column in range(kernel_size):
                    sum_of_kernel[0] += image[row - kernel_radius + kernel_row][column - kernel_radius + kernel_column][0] * kernel[kernel_row][kernel_column]
                    sum_of_kernel[1] += image[row - kernel_radius + kernel_row][column - kernel_radius + kernel_column][1] * kernel[kernel_row][kernel_column]
                    sum_of_kernel[2] += image[row - kernel_radius + kernel_row][column - kernel_radius + kernel_column][2] * kernel[kernel_row][kernel_column]
            sum_of_kernel[0] = kernel_in_limit(sum_of_kernel[0])
            sum_of_kernel[1] = kernel_in_limit(sum_of_kernel[1])
            sum_of_kernel[2] = kernel_in_limit(sum_of_kernel[2])
            image_with_blur[row][column] = sum_of_kernel
    return image_with_blur


def resize(image: list, new_width: int, new_height: int) -> list:
    """Resizes an image to the given width and height.

    Args:
        image (list): The image matrix.
        new_width (int): The desired width.
        new_height (int): The desired height.

    Returns:
        list: The resized image matrix.

    """
    old_height = len(image)
    old_width = len(image[0])
    width_ratio = old_width / new_width
    height_ratio = old_height / new_height
    image_with_resized = make_matrix(new_height, new_width)
    for row in range(new_height):
        for column in range(new_width):
            old_row = int(row * height_ratio)
            old_column = int(column * width_ratio)
            image_with_resized[row][column] = image[old_row][old_column]
    return image_with_resized


def rotate(image: list) -> list:
    """Rotates an image 90 degrees.

    Args:
        image (list): The image matrix.

    Returns:
        list: The rotated image matrix.

    """
    rotated_image = make_square_matrix(len(image[0]))
    for row in range(len(image[0])):
        for column in range(len(image)):
            rotated_image[row][column] = image[column][len(image[0]) - row - 1]
    return rotated_image


def flip(image: list) -> list:
    """Flips an image horizontally.

    Args:
        image (list): The image matrix.

    Returns:
        list: The flipped image matrix.

    """
    flipped_image = copy.deepcopy(image)
    for row in range(len(flipped_image)):
        flipped_image[row] = flipped_image[row][::-1]
    return flipped_image


def main():
    # Example usage
    image_path = Path("example_image.png")
    image = ex5_helper.load_image(image_path)
    separated_channels = separate_channels(image)
    combined_channels = combine_channels(separated_channels)
    grayscale_image = RGB2grayscale(image)
    blurred_image = blur(image)
    resized_image = resize(image, 200, 200)
    rotated_image = rotate(image)
    flipped_image = flip(image)

    # Saving the processed images
    ex5_helper.save_image(separated_channels, "separated_channels.png")
    ex5_helper.save_image(combined_channels, "combined_channels.png")
    ex5_helper.save_image(grayscale_image, "grayscale_image.png")
    ex5_helper.save_image(blurred_image, "blurred_image.png")
    ex5_helper.save_image(resized_image, "resized_image.png")
    ex5_helper.save_image(rotated_image, "rotated_image.png")
    ex5_helper.save_image(flipped_image, "flipped_image.png")


if __name__ == "__main__":
    main()
