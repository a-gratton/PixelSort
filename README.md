# PixelSort
A Python pixel sorting utility created using Pillow (a fork of the Python Image Library). Use it to create unique artistic effects with your favourite photos!



![Example Image](https://github.com/a-gratton/PixelSort/blob/master/Example%20Images/Mixed%20Signals-edited.png)

## Install
In order to use the script, first install Pillow:

```
pip install Pillow
```

Then edit the parameters at the beginning of the script to generate new images.

## Example

Using the parameters: 
```
 mode = SortMode('row', 'l', 'brighter', 'sort', -1, 250, 20, 150, 40)
```

And setting the file path:
```
im = Image.open("./Example Images/Mixed Signals.jpg").convert("HSV")
```
will generate the same example image from above!

## Usage
All script parameters are controlled by editing the first line of main. From left to right they are:
* Row/Column Specifier: 'row' for sorting rows, 'col' for sorting columns.
* HSL Selector: choose how you want to sort each pixel: by **H**ue (color), **S**aturation (intensity) or **L**uminance (brightness))
* Range Selection Mode: 'brighter' for selecting pixel ranges with a higher luminance than the set black point, 'darker' for selecting pixel ranges with a lower luminance than the set white point
* Sort Mode: 'sort' for sorting pixels by their HSL values, 'average' for replacing each selected range with the average pixel from that range (plus the luminance bias factor)
* Direction: 1 for left-to-right/top-to-bottom, -1 for right-to-left/bottom-to-top
* Noise Threshold: sets the minimum size in pixels a range must be in order to be sorted
* Black Point: sets the black point for 'brighter' range selection
* White Point: sets the white point for 'darker' range selection
* Luminance Bias: set the luminance increase for pixels when using the 'average' mode


Efficiency Improvements
--------------
Pixels are sorted using a bitwise base 16 implementation of the *Radix-LSD* sorting algorithm in order to improve run-times on large images.

Rows/Columns are processed on separate cores simultaneously through use of the Python multiprocessing library. In order to maximize performance, change the processes parameter on line 46
```
pool = mp.Pool(processes=4)
```
to equal the number of cores availible on your local machine.

