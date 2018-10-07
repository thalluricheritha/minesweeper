# coding=utf-8
#####   ---------------------------------------------------------------   #####
##                                 View Class                                ##
##                                                                           ##
#####   ---------------------------------------------------------------   #####

#
# ─── IMPORTS ────────────────────────────────────────────────────────────────────
from tkinter import *
import tkinter.messagebox as tkMsg
from MenuBar import MenuBar
from PositionService import PositionService
from ScoreBoard import ScoreBoard

class View:
    #
    # ─── CALLBACK FOR LEFT CLICKING THE CANVAS ──────────────────────────────────────
    #
    def callback_toggle(self, event):
        #
        # ─── DISABLE THE BOARD ON LOSS ───────────────────────────────────
        if self.board.get_state_loss():
            return NONE
        if self.board.get_state_win():
            return NONE
        
        #
        # ─── MUTATE THE BOARD THROUGH THE CONTROLLER ─────────────────────
        coordinates = self.position_service.calculate_coordinates(event.x, event.y)
        self.controller.activate(coordinates[0], coordinates[1])

        #
        # ─── BEFORE REDRAW CHECK IF THE GAME IS OVER ─────────────────────
        if self.board.get_state_loss():
            self.draw_mines()
            self.score_board.stop_timer(False)
            tkMsg.showinfo("Game Over", "You Lost the Game!")
        else: 
            self.render_handler();
            
        if self.board.get_state_win():
            self.score_board.stop_timer()
            win_string = "Congratulations!\n You won the game with a final score of:{score}"
            display_string = win_string.format(score=self.score_board.get_score())
            tkMsg.showinfo("Game Win!", display_string)


    def callback_cover(self, event):
        if self.board.get_state_loss():
            return NONE
        if self.board.get_state_win():
            return NONE
        #
        # ─── MUTATE THE BOARD THROUGH THE CONTROLLER ─────────────────────
        coordinates = self.position_service.calculate_coordinates(event.x, event.y)
        self.controller.cover(coordinates[0], coordinates[1])
        
        self.render_handler()

        if self.board.get_state_win():
            self.score_board.stop_timer()
            win_string = "Congratulations!\n You won the game with a final score of:{score}"
            display_string = win_string.format(score=self.score_board.get_score())
            tkMsg.showinfo("Game Win!", display_string)


    def __init__(self, game_board, game_controller, master, settings):
        #
        # ─── ASSIGN REFERENCE VARIABLES ──────────────────────────────────
        self.board = game_board
        self.controller = game_controller

        #
        # ─── EXTRACT SETTINGS ────────────────────────────────────────────
        self.height = settings['window_dimension']
        self.width = settings['window_dimension']
        self.game_size = settings['game_size']
        self.tile_dimension = settings['tile_dimension']
        self.mode = settings['game_mode']
        self.difficulty = settings['game_difficulty']
        self.position_service = PositionService(self.mode, self.tile_dimension)

        #
        # ─── CALCULATE CANVAS DIMENSIONS ─────────────────────────────────
        canvas_dimension = self.tile_dimension * self.game_size
        canvas_width = canvas_dimension
        canvas_height = canvas_dimension
        if self.mode == "HEX":
            canvas_height = canvas_dimension * 0.75 + self.tile_dimension / 2
            canvas_width += self.tile_dimension / 2
            
        #
        # ─── DEFINE THE FRAME ────────────────────────────────────────────
        self.frame = Frame(master, background="#F19C79", borderwidth=23)
        self.frame.pack()

        #
        # ─── LOAD SQUARE TILE SET ─────────────────────────────────────────
        self.square_up    = PhotoImage(file="assets/square_up.png")
        self.square_down  = PhotoImage(file="assets/square_down.png")
        self.square_bomb  = PhotoImage(file="assets/square_bomb.png")
        self.square_cover = PhotoImage(file="assets/square_cover.png")

        #
        # ─── LOAD HEXAGONAL TILE SET ─────────────────────────────────────
        self.hex_up    = PhotoImage(file="assets/hex_up.png")
        self.hex_down  = PhotoImage(file="assets/hex_down.png")
        self.hex_bomb  = PhotoImage(file="assets/hex_bomb.png")
        self.hex_cover = PhotoImage(file="assets/hex_cover.png")

        #
        # ─── CREATE COMPONENTS ───────────────────────────────────────────
        self.canvas = Canvas(self.frame, width=canvas_width, height=canvas_height, background="#F19C79", bd=0, highlightthickness=0)
        self.canvas.bind("<Button-1>", self.callback_toggle)
        self.canvas.bind("<Button-3>", self.callback_cover)
        self.score_board = ScoreBoard(self.frame, self.width, self.difficulty)
        self.score_board.pack(side="top")
        self.canvas.pack()
        self.render_handler()
        self.menubar = MenuBar(self.frame, self)
        self.menubar.pack(side="bottom", pady=(40,0))


    #
    # ─── RENDER HANDLER BASED ON GAME TYPE ──────────────────────────────────────────
    def render_handler(self):
        if self.mode == "SQUARE":
            self.draw_squares()
        elif self.mode == "HEX":
            self.draw_hexagons()
            print("We printed the hexagons")
        

    def draw_squares(self):
        #
        # ─── GET CURRENT STATE OF THE MODEL ──────────────────────────────
        toggles = self.board.get_state_toggles()
        numbers = self.board.get_state_button_numbers()
        covers  = self.board.get_state_covers()

        # ─── REDRAW THE GAME BOARD ───────────────────────────────────────
        self.canvas.delete(ALL)
        for i in range(self.game_size):
            for j in range(self.game_size):
                if covers[i][j] == True:
                    self.place_tile_square(j, i, self.square_cover)
                elif not toggles[i][j]:
                    self.place_tile_square(j, i, self.square_up)
                elif numbers[i][j] == 0:
                    self.place_tile_square(j, i, self.square_down)
                else:
                    self.place_tile_square(j, i, self.square_down, numbers[i][j])
    
    def draw_hexagons(self):
        #
        # ─── GET CURRENT STATE OF THE MODEL ──────────────────────────────
        toggles = self.board.get_state_toggles()
        numbers = self.board.get_state_button_numbers()
        covers  = self.board.get_state_covers()

        # ─── REDRAW THE GAME BOARD ───────────────────────────────────────
        self.canvas.delete(ALL)
        for i in range(self.game_size):
            for j in range(self.game_size):
                if covers[i][j] == True:
                    self.place_tile_hex(j, i, self.hex_cover)
                elif not toggles[i][j]:
                    self.place_tile_hex(j, i, self.hex_up)
                elif numbers[i][j] == 0:
                    self.place_tile_hex(j, i, self.hex_down)
                else:
                    self.place_tile_hex(j, i, self.hex_down, numbers[i][j])
    
    #
    # ─── DETERMINE POSITION FOR SQUARE TILE ─────────────────────────────────────────
    def place_tile_square(self, i, j, image, text=0):
        img_dimension = 46
        pos_x = img_dimension * i
        pos_y = img_dimension * j
        self.draw_tile(pos_x, pos_y, image, text)

    #
    # ─── DETERMINE POSITION FOR HEXAGONAL TILE ──────────────────────────────────────
    def place_tile_hex(self, i, j, image, text=0):
        img_dimension = 46
        base_pos_y = j * (img_dimension * 0.75)
        if j % 2 == 1:
            base_pos_x = i * img_dimension + (img_dimension / 2)
        else:
            base_pos_x = i * img_dimension
        self.draw_tile(base_pos_x, base_pos_y, image, text)

        
    def draw_tile(self, pos_x, pos_y, image, text):
        self.canvas.create_image(pos_x, pos_y, anchor=NW, image=image, tags="tile");
        if text != 0:
            if text != "zero":    
                self.canvas.create_text(pos_x + 22.5, pos_y + 22.5, text=text)


    def draw_mines(self):
        numbers = self.board.get_state_button_numbers()
    
        for i in range(self.game_size):
            for j in range(self.game_size):
                if numbers[i][j] == -1:
                    if self.mode == "SQUARE":    
                        self.place_tile_square(j, i, self.square_bomb)
                    elif self.mode == "HEX":
                        self.place_tile_hex(j, i, self.hex_bomb)
                        
    #
    # ─── FUNCTION TO DESTROY ALL TKINTER COMPONENTS AND RETURN TO MENU ──────────────
    #
    def cleanup(self):
        self.canvas.destroy()
        self.menubar.destroy()
        self.frame.destroy()
        self.frame.quit()
        