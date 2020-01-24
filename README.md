# PixelSort
A Python pixel sorting utility created using Pillow (a fork of Python Image Library).
See the Example Images folder for some before/after samples!

Supplied images are first converted into the **HSV** color mode, and then the pixels in each row or column are sorted by their respective **H**ue (color), **S**aturation (intensity) or **V**alue (luminance).

The ranges of pixels to sort in a given row or column are selected according to the chosen mode. Currently PixelSort supports two manipulation modes:
* Brighter, which sorts only pixels with a luminance above a certain threshold.
* Darker, which sorts only pixels with a luminance below a certain threshold.

Efficiency Considerations
--------------
Pixels are sorted using a bitwise base 16 implementation of the *Radix-LSD* sorting algorithm in order to improve run-times on large images.

Rows/Columns are processed on separate cores simultaneously through use of the Python multiprocessing library.

