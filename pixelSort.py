from PIL import Image
from mode import SortMode
from copy import copy


# Modes:
#  brighter: Sort pixels brighter than the set black point.
#            each range of non black pixels sorted separately
#   darker: Sort pixels darker than the set white point
#           each range of non white pixels sorted separately


def main():
    mode = SortMode('col', 'l', 'brighter', -1, 100, 256)
    try:
        im = Image.open("Mixed Signals.jpg").convert("HSV")
        print(im.format, im.size, im.mode)
        sort(im, mode)
        im.show()
    except IOError:
        print("File not found")


def sort(im, mode):
    if mode.row:
        sortRow(im, mode)
    else:
        sortCol(im, mode)


def sortCol(source, mode):
    pixels = source.load()
    if mode.mode == 0:
        for i in range(source.size[0]):
            sort_range = [0]
            for j in range(source.size[1]):
                if mode.black < pixels[i, j][2]:
                    sort_range[len(sort_range) - 1] = j
                    sort_range += [0]
                elif not (sort_range[len(sort_range) - 1] == -1):
                    sort_range += [-1]
            col = [(0, 0, 0)]
            cols = [[(0, 0, 0), ], ]
            for j in range(len(sort_range)):
                if not (sort_range[j] == -1):
                    col[len(col) - 1] = pixels[i, sort_range[j]]
                    col += [(0, 0, 0)]
                else:
                    cols[len(cols) - 1] = copy(col)
                    cols += [[(0, 0, 0)]]
                    col = [(0, 0, 0)]
            cols[len(cols) - 1] = col
            for subset in cols:
                radixSort(subset, 255, mode.hsl)
            colInsert(pixels, cols, sort_range, mode, i)

    elif mode.mode == 1:
        for i in range(source.size[0]):
            sort_range = [0]
            for j in range(source.size[1]):
                if pixels[i, j][2] < mode.white:
                    sort_range[len(sort_range) - 1] = j
                    sort_range += [0]
                elif not (sort_range[len(sort_range) - 1] == -1):
                    sort_range += [-1]
            col = [(0, 0, 0)]
            cols = [[(0, 0, 0), ], ]
            for j in range(len(sort_range)):
                if not (sort_range[j] == -1):
                    col[len(col) - 1] = pixels[i, sort_range[j]]
                    col += [(0, 0, 0)]
                else:
                    cols[len(cols) - 1] = copy(col)
                    cols += [[(0, 0, 0)]]
                    col = [(0, 0, 0)]
            cols[len(cols) - 1] = col
            for subset in cols:
                radixSort(subset, 255, mode.hsl)
            colInsert(pixels, cols, sort_range, mode, i)


def sortRow(source, mode):
    pixels = source.load()
    if mode.mode == 0:
        for i in range(source.size[1]):
            sort_range = [0]
            for j in range(source.size[0]):
                if mode.black < pixels[j, i][2]:
                    sort_range += [0]
                    sort_range[len(sort_range) - 1] = j

                elif not (sort_range[len(sort_range) - 1] == -1):
                    sort_range += [-1]
            row = [(0, 0, 0)]
            rows = [[(0, 0, 0), ], ]
            for j in range(len(sort_range)):
                if not (sort_range[j] == -1):
                    row[len(row) - 1] = pixels[sort_range[j], i]
                    row += [(0, 0, 0)]
                else:
                    rows[len(rows) - 1] = copy(row)
                    rows += [[(0, 0, 0)]]
                    row = [(0, 0, 0)]
            rows[len(rows) - 1] = row
            for subset in rows:
                radixSort(subset, 255, mode.hsl)
            rowInsert(pixels, rows, sort_range, mode, i)

    if mode.mode == 1:
        for i in range(source.size[1]):
            sort_range = [0]
            for j in range(source.size[0]):
                if pixels[j, i][2] < mode.white:
                    sort_range += [0]
                    sort_range[len(sort_range) - 1] = j
                elif not (sort_range[len(sort_range) - 1] == -1):
                    sort_range += [-1]
            row = [(0, 0, 0)]
            rows = [[(0, 0, 0), ], ]
            for j in range(len(sort_range)):
                if not (sort_range[j] == -1):
                    row[len(row) - 1] = pixels[sort_range[j], i]
                    row += [(0, 0, 0)]
                else:
                    rows[len(rows) - 1] = copy(row)
                    rows += [[(0, 0, 0)]]
                    row = [(0, 0, 0)]
            rows[len(rows) - 1] = row
            for subset in rows:
                radixSort(subset, 255, mode.hsl)
            rowInsert(pixels, rows, sort_range, mode, i)


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


main()
