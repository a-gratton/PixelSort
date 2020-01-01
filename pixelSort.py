from PIL import Image
from mode import SortMode
from copy import copy
import multiprocessing as mp
from functools import partial


# Modes:
#  brighter: Sort pixels brighter than the set black point.
#            each range of non black pixels sorted separately
#   darker: Sort pixels darker than the set white point
#           each range of non white pixels sorted separately


def main():
    mode = SortMode('col', 'l', 'brighter', 'average', 1, 30, 256)
    try:
        im = Image.open("Writing On Stone Star Composite.jpg").convert("HSV")
        print(im.format, im.size, im.mode)
        sort(im, mode)
        im.show()
    except IOError:
        print("File not found")


def sort(im, mode):
    pool = mp.Pool(processes=8)
    pixels = im.load()
    if mode.row:
        if mode.range_mode == 0 or mode.range_mode == 1:
            srt = partial(sortRow, im, mode)
            workers = pool.map(srt, range(im.size[1]))
            for q in range(len(workers)):
                rowInsert(pixels, workers[q][0], workers[q][1], mode, q)
    else:
        if mode.range_mode == 0 or mode.range_mode == 1:
            srt = partial(sortCol, im, mode)
            workers = pool.map(srt, range(im.size[0]))
            for q in range(len(workers)):
                colInsert(pixels, workers[q][0], workers[q][1], mode, q)


def sortCol(source, mode, i):
    pixels = source.load()
    if mode.range_mode == 0:
        sort_range = [0]
        for j in range(source.size[1]):
            if mode.black < pixels[i, j][2]:
                sort_range.append(j)
            elif sort_range[-1] != -1:
                sort_range.append(-1)
        col = [(0, 0, 0)]
        cols = [[(0, 0, 0), ], ]
        for j in sort_range:
            if j != -1:
                col.append(pixels[i, j])
            else:
                cols[-1] = copy(col)
                cols += [[(0, 0, 0)]]
                col = [(0, 0, 0)]
        cols[-1] = col
        if mode.sort_mode == 0:
            for subset in cols:
                radixSort(subset, 255, mode.hsl)
            return [cols, sort_range]
        elif mode.sort_mode == 1:
            for subset in cols:
                averageRange(subset)
            return [cols, sort_range]

    elif mode.range_mode == 1:
        sort_range = [0]
        for j in range(source.size[1]):
            if pixels[i, j][2] < mode.white:
                sort_range.append(j)
            elif sort_range[-1] != -1:
                sort_range.append(-1)
        col = [(0, 0, 0)]
        cols = [[(0, 0, 0), ], ]
        for j in sort_range:
            if j != -1:
                col.append(pixels[i, j])
            else:
                cols[-1] = copy(col)
                cols += [[(0, 0, 0)]]
                col = [(0, 0, 0)]
        else:
            cols[-1] = col
        if mode.sort_mode == 0:
            for subset in cols:
                radixSort(subset, 255, mode.hsl)
            return [cols, sort_range]
        elif mode.sort_mode == 1:
            for subset in cols:
                averageRange(subset)
            return [cols, sort_range]


def sortRow(source, mode, i):
    pixels = source.load()
    if mode.range_mode == 0:
        sort_range = [0]
        for j in range(source.size[0]):
            if mode.black < pixels[j, i][2]:
                sort_range.append(j)
            elif sort_range[-1] != -1:
                sort_range.append(-1)
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
                averageRange(subset)
            return [rows, sort_range]

    elif mode.range_mode == 1:
        sort_range = [0]
        for j in range(source.size[0]):
            if pixels[j, i][2] < mode.white:
                sort_range.append(j)
            elif sort_range[-1] != -1:
                sort_range.append(-1)
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
                averageRange(subset)
            return [rows, sort_range]


def averageRange(source):
    average = [0, 0, 0]
    for pixel in source:
        for i in range(3):
            average[i] += pixel[i]
    for i in range(3):
        average[i] //= len(source)
    newPixel = (average[0], average[1], average[2])
    for i in range(len(source)):
        source[i] = newPixel


def colInsert(pixels, cols, sort_range, mode, col):
    index = curr = 0
    for j in sort_range:
        if not (j == -1):
            pixels[col, j] = cols[curr][mode.direction * index]
            index += 1
        else:
            curr += 1
            index = 0


def rowInsert(pixels, rows, sort_range, mode, row):
    index = curr = 0
    for j in sort_range:
        if not (j == -1):
            pixels[j, row] = rows[curr][mode.direction * index]
            index += 1
        else:
            curr += 1
            index = 0


def radixSort(source, key, hsl):
    pval = 0
    while key >> pval > 0:
        countingSort(source, pval, hsl)
        pval += 4


def countingSort(source, pval, hsl):
    elementCount = [0] * 16
    ordered = [(0, 0, 0)] * len(source)
    for pixel in source:
        if pixel[2] >= 0:
            elementCount[(pixel[hsl] >> pval) & 0xF] += 1
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
