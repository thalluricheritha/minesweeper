
# Import Modules
from tkinter import *

# Import Classes
from GameController import GameController
from Board import Board
from View import View
from MainMenu import MainMenu


class Minesweeper:
    def on_closing(self):
        self.root.destroy()
        exit()

    def __init__(self):
        #
        # ─── DECLARE GAME SETTINGS ───────────────────────────────────────
        #
        self.game_settings = {}
        self.game_settings['window_dimension'] = 720
        self.game_settings['tile_dimension'] = 46

        #
        # ─── CREATE ROOT WINDOW ──────────────────────────────────────────
        #
        
        self.root = Tk()
        self.root.title("Z-Sweeper")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        while(True):
            #
            # ─── DISPLAY MAIN MENU AND POPULATE GAME SETTINGS ────────────────
            #
            self.main_menu = MainMenu(self.root, self.game_settings)
            self.root.mainloop()


            #
            # ─── CREATE THE GAME BOARD ───────────────────────────────────────
            #
            self.game_board = Board(
                self.game_settings['game_mode'],
                self.game_settings['game_difficulty'],
                self.game_settings['game_size']
            );

            self.game_controller = GameController(self.game_board)

            self.view = View(self.game_board, self.game_controller, self.root, self.game_settings)
            self.root.mainloop()


        #
        # ─── CREATE GAME WITH SETTINGS ───────────────────────────────────
        #
        # mine_density = 0.15
        # dimension = 8
        # self.board = Board("square", mine_density, dimension)
        # self.game_controller = GameController(board)
        # self.view = View(board, game_controller)

Minesweeper()