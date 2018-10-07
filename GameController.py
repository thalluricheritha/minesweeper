# coding=utf-8
#####   ---------------------------------------------------------------   #####
##                          Controller Class                                 ##
##               Entire Game Implementation for Minesweeper                  ##
#####   ---------------------------------------------------------------   #####

class GameController:
    def __init__(self, board):
        self.board = board
    
#
# ─── MUTATE BOARD STATE AFTER RECEIVING ACTION FROM VIEW ────────────────────────
#   
    def activate(self, i, j):
        print("[Controller] Passing", i, j,)
        self.board.toggle_button(i, j)

    def cover(self, i, j):
        print("[Controller] Covering", i, j)
        self.board.cover_button(i, j)

    
        

