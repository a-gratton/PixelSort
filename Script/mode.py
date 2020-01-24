class SortMode:
    def __init__(self, row, hsl, range_mode, sort, direc=1, noise=0, black=0, white=255, lum_bias=0):
        self.row = 1 if row == 'row' else 0
        self.hsl = 0 if hsl == 'h' else 1 if hsl == 's' else 2
        self.range_mode = 0 if range_mode == 'brighter' else 1 if range_mode == 'darker' else 2
        self.ignore_noise = noise
        self.sort_mode = 0 if sort == 'sort' else 1 if sort == 'average' else 2
        self.direction = 1 if direc >= 0 else -1
        self.black = black
        self.white = white
        self.lum_bias = lum_bias
