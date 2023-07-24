# Image Editor

## Overview

Image Editor is a Python script that provides various image editing functionalities. It allows users to perform operations such as separating and combining color channels, converting an RGB image to grayscale, applying a blur effect, resizing, rotating, and flipping images.

## Functions

- `separate_channels`: Separates the channels of an image and rearranges them.
- `combine_channels`: Combines the channels of an image and rearranges them.
- `make_square_matrix`: Creates a square matrix of the given size.
- `make_matrix`: Creates a matrix with the given number of rows and columns.
- `average_color_to_black_white`: Calculates the average of three colors and converts it to black and white.
- `kernel_in_limit`: Checks if the sum of the kernel is within the limit (0-255).
- `RGB2grayscale`: Converts an RGB image to grayscale.
- `blur`: Applies a blur effect to an image.
- `resize`: Resizes an image to the given width and height.
- `rotate`: Rotates an image 90 degrees.
- `flip`: Flips an image horizontally.

## Usage

To use the Image Editor, run the script and pass the desired image path and processing options as function arguments.

```python
# Example usage
image_path = Path("example_image.png")
image = ex5_helper.load_image(image_path)
separated_channels = separate_channels(image)
# ... Add other functions and image processing operations here ...
