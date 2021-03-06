from PIL import Image
from Script.mode import SortMode
from copy import copy
import multiprocessing as mp
from functools import partial


# Range Modes:
#   brighter:
#       Sort pixels brighter than the set black point.
#           Each range of non black pixels sorted separately.
#   darker:
#       Sort pixels darker than the set white point.
#           Each range of non white pixels sorted separately.
#
# Sort Modes:
#   sort:
#       The pixels in each range are sorted by the given parameter (HSL).
#   average:
#       The pixels in each range are averaged, then all pixels in the range are set to this value.
#       Luminance values are increased by the luminance bias parameter value.
#
# Noise ignore parameter:
#   Sets the minimum length of each range; minimizes impact of image noise on range selection.


def main():
    # parameters: row/col, hsl mode, range selection mode, sort mode, direction,
    #             noise parameter, black point, white point, average mode luminance bias
    mode = SortMode('row', 'l', 'brighter', 'sort', -1, 250, 20, 150, 40)
    try:
        im = Image.open("./Example Images/Mixed Signals.jpg").convert("HSV")
        print(im.format, im.size, im.mode)
        sort(im, mode)
        im = im.convert("RGB")
        im.save('Mixed Signals-edited.png')

    # if file is not found:
    except IOError:
        print("File not found")


def sort(im, mode):
    # distributes rows/columns between worker processes

    pool = mp.Pool(processes=4)  # setting up worker pool (set equal to number of CPU cores)
    pixels = im.load()  # loading pixel map of image

    # sorting rows
    if mode.row:
        if mode.range_mode == 0 or mode.range_mode == 1:  # extraneous if statement to cover future expansion
            srt = partial(rowHandler, im, mode)  # using partial for easier use of pool.map
            workers = pool.map(srt, range(im.size[1]))
            for q in range(len(workers)):
                rowInsert(pixels, workers[q][0], workers[q][1], mode, q)  # calls row insert function, then frees worker

    # sorting columns
    else:
        if mode.range_mode == 0 or mode.range_mode == 1:  # extraneous if statement to cover future expansion
            srt = partial(colHandler, im, mode)  # using partial for easier use of pool.map
            workers = pool.map(srt, range(im.size[0]))
            for q in range(len(workers)):
                colInsert(pixels, workers[q][0], workers[q][1], mode, q)  # calls col insert function, then frees worker


def colHandler(source, mode, i):
    # function to handle column sorting
    pixels = source.load()  # loading pixel map of image
    sort_range = [0]
    temp_range = []

    if mode.range_mode == 0:  # "brighter" selection mode
        for j in range(source.size[1]):
            if mode.black < pixels[i, j][2]:
                temp_range.append(j)  # building temporary sort range list
            else:
                if sort_range[-1] != -1:
                    sort_range.append(-1)  # signifies break in sort range (edge)
                if len(temp_range) > mode.ignore_noise:  # if temp sort range is longer than noise parameter:
                    sort_range += temp_range  # append temp range to sort range list
                temp_range = []  # reset temp range
        else:
            sort_range += temp_range  # appending last temp range if it reaches the end of the image
        col = [(0, 0, 0)]
        cols = [[(0, 0, 0), ], ]

        # breaking up sort range list into 2D list
        for j in sort_range:
            if j != -1:
                col.append(pixels[i, j])
            else:
                cols[-1] = copy(col)
                cols += [[(0, 0, 0)]]
                col = [(0, 0, 0)]
        cols[-1] = col

        if mode.sort_mode == 0:  # if mode is "sort"
            for subset in cols:
                radixSort(subset, 255, mode.hsl)  # sort ranges using radix base-16 sort
            return [cols, sort_range]  # return parameters to col insert function

        elif mode.sort_mode == 1:  # if mode is "average"
            for subset in cols:
                averageRange(subset, mode)  # average pixel values in each range
            return [cols, sort_range]  # return parameters to col insert function

    elif mode.range_mode == 1:  # "darker" selection mode
        for j in range(source.size[1]):
            if pixels[i, j][2] < mode.white:
                temp_range.append(j)  # building temporary sort range list
            else:
                if sort_range[-1] != -1:
                    sort_range.append(-1)  # signifies break in sort range (edge)
                if len(temp_range) > mode.ignore_noise:  # if temp sort range is longer than noise parameter:
                    sort_range += temp_range  # append temp range to sort range list
                temp_range = []  # reset temp range
        else:
            sort_range += temp_range  # appending last temp range if it reaches the end of the image
        col = [(0, 0, 0)]
        cols = [[(0, 0, 0), ], ]

        # breaking up sort range list into 2D list
        for j in sort_range:
            if j != -1:
                col.append(pixels[i, j])
            else:
                cols[-1] = copy(col)
                cols += [[(0, 0, 0)]]
                col = [(0, 0, 0)]
        else:
            cols[-1] = col

        if mode.sort_mode == 0:  # if mode is "sort"
            for subset in cols:
                radixSort(subset, 255, mode.hsl)  # sort ranges using radix base-16 sort
            return [cols, sort_range]  # return parameters to col insert function

        elif mode.sort_mode == 1:  # if mode is "average"
            for subset in cols:
                averageRange(subset, mode)  # average pixel values in each range
            return [cols, sort_range]  # return parameters to col insert function


def rowHandler(source, mode, i):
    # the same structure as colHandler, but for rows
    pixels = source.load()
    sort_range = [0]
    temp_range = []
    if mode.range_mode == 0:
        for j in range(source.size[0]):
            if mode.black < pixels[j, i][2]:
                temp_range.append(j)
            else:
                if sort_range[-1] != -1:
                    sort_range.append(-1)
                if len(temp_range) > mode.ignore_noise:
                    sort_range += temp_range
                temp_range = []
        else:
            sort_range += temp_range
        row = [(0, 0, 0)]
        rows = [[(0, 0, 0), ], ]
        for j in sort_range:
            if j != -1:
                row.append(pixels[j, i])
            else:
                rows[-1] = (copy(row))
                rows += [[(0, 0, 0)]]
                row = [(0, 0, 0)]
        rows[-1] = row

        if mode.sort_mode == 0:
            for subset in rows:
                radixSort(subset, 255, mode.hsl)
            return [rows, sort_range]

        elif mode.sort_mode == 1:
            for subset in rows:
                averageRange(subset, mode)
            return [rows, sort_range]

    elif mode.range_mode == 1:
        for j in range(source.size[0]):
            if pixels[j, i][2] < mode.white:
                temp_range.append(j)
            else:
                if sort_range[-1] != -1:
                    sort_range.append(-1)
                if len(temp_range) > mode.ignore_noise:
                    sort_range += temp_range
                temp_range = []
        else:
            sort_range += temp_range
        row = [(0, 0, 0)]
        rows = [[(0, 0, 0), ], ]
        for j in sort_range:
            if j != -1:
                row[len(row) - 1] = pixels[j, i]
                row += [(0, 0, 0)]
            else:
                rows[-1] = copy(row)
                rows += [[(0, 0, 0)]]
                row = [(0, 0, 0)]
        rows[-1] = row

        if mode.sort_mode == 0:
            for subset in rows:
                radixSort(subset, 255, mode.hsl)
            return [rows, sort_range]

        elif mode.sort_mode == 1:
            for subset in rows:
                averageRange(subset, mode)
            return [rows, sort_range]


def colInsert(pixels, cols, sort_range, mode, col):  # replaces sorted columns of original image
    index = curr = 0
    for j in sort_range:
        if not (j == -1):
            pixels[col, j] = cols[curr][mode.direction * index]
            index += 1
        else:
            curr += 1
            index = 0


def rowInsert(pixels, rows, sort_range, mode, row):
    # replaces sorted rows of original image
    index = curr = 0
    for j in sort_range:
        if not (j == -1):
            pixels[j, row] = rows[curr][mode.direction * index]
            index += 1
        else:
            curr += 1
            index = 0


def averageRange(source, mode):
    # averages the pixel values in each range
    average = [0, 0, 0]
    for pixel in source:
        for i in range(3):
            average[i] += pixel[i]
    for i in range(3):
        average[i] //= len(source)
    newPixel = (average[0], average[1], average[2] + mode.lum_bias)  # adds luminance bias parameter (brightens ranges)
    for i in range(len(source)):
        source[i] = newPixel


def radixSort(source, key, hsl):
    # radix base-16 sort (using bitwise operators)
    # note that pixel[hsl] accesses the hue, saturation, or luminance as specified in original parameters
    pval = 0
    while key >> pval > 0:
        countingSort(source, pval, hsl)
        pval += 4


def countingSort(source, pval, hsl):
    # subroutine for radix sort
    elementCount = [0] * 16  # digit count list
    ordered = [(0, 0, 0)] * len(source)
    for pixel in source:
        if pixel[2] >= 0:  # handling edge case of 0 brightness pixels
            elementCount[(pixel[hsl] >> pval) & 0xF] += 1  # selecting base 16 digit with bitwise operators
        else:
            elementCount[0] += 1
    for i in range(1, 16):
        elementCount[i] += elementCount[i - 1]
    for pixel in reversed(source):
        val = (pixel[hsl] >> pval) & 0xF
        ordered[elementCount[val] - 1] = pixel
        elementCount[val] -= 1
    for i in range(len(source)):
        source[i] = ordered[i]


if __name__ == '__main__':
    main()
