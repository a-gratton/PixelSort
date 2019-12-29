class SortMode:
    def __init__(self, row, hsl, mode, direc, black = 0, white = 255, lowT = 0, highT = 0):
        self.row = 1 if row == 'row' else 0
        self.hsl = 0 if hsl == 'h' else 1 if hsl == 's' else 2
        self.mode = 0 if mode == 'brighter' else 1 if mode == 'darker' else 2
        self.direction = 1 if direc >= 0 else -1
        self.black = black
        self.white = white
        self.low = lowT
        self.high = highT
