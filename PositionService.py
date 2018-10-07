class PositionService:
    def __init__(self, mode, tile_dimension):
        print("Got here?")
        print("PS MODE: ", mode)
        self.mode = mode
        self.tile_dimension = tile_dimension
        self.row_height = tile_dimension * 0.75
    
    def calculate_coordinates(self, x, y):  
        if self.mode == "SQUARE":
            return self.calculate_coordinates_square(x, y)
        elif self.mode == "HEX":
            return self.calculate_coordinates_hex(x, y)
    
    def calculate_coordinates_square(self, x, y):
        return (y // self.tile_dimension, x // self.tile_dimension)

    def calculate_coordinates_hex(self, x, y):
        row = int(y // (self.row_height))
        odd_row = row % 2 == 1
        if odd_row:
            column = int((x - self.tile_dimension / 2) / self.tile_dimension)
        else:
            column = int(x / self.tile_dimension)
        #
        # ─── DETERMINE RELATIVE POSITION ─────────────────────────────────
        rel_y = y - row * self.row_height
        if odd_row:
            rel_x = x - column * (self.tile_dimension) - self.tile_dimension / 2
        else:
            rel_x = x - column * self.tile_dimension
        
        #
        # ─── CALCULATE THE GRADIENT OF THE TOP EDGES ─────────────────────
        #
        c = self.tile_dimension * 0.25
        gradient = c / (self.tile_dimension / 2)
        

        #
        # ─── DETERMINE IF POINT IS ABOVE HEXAGONS TOP EDGES ──────────────
        if rel_y < (-gradient * rel_x + c):
            row -= 1
            if not odd_row:
                column -= 1
        elif rel_y < (gradient * rel_x - c):
            row -= 1
            if odd_row:
                column += 1
        
        return [row, column]


            
            
