#
# ─── CLASS FOR THE GAME SCORER ─────────────────────────────────────────────────
#

import tkinter as tk
from tkinter import *
import time


class ScoreBoard(tk.Frame):
    def __init__(self, parent, dimension, difficulty):
        tk.Frame.__init__(self, parent)
        self.config(bg='#F19C79')
        self.parent = parent
        self.sec = 0
        self.timing = True
        self.dimension = dimension
        self.difficulty = difficulty
        self.score = 0

        #
        # ─── CREATE COMPONENTS ───────────────────────────────────────────
        self.time = Label(self, bg='#F19C79', font=('Times', 20))
        self.time.pack()
        self.tick()
        

    def tick(self, calc_score=True):
        if self.timing:
            self.sec += 1
            minutes = self.sec // 60
            seconds = self.sec % 60

            if calc_score:
                self.calculate_score()

            format_str = "Time: {min}:{sec} Score: {score}"
            time_string = format_str.format(min=minutes, sec=seconds, score=self.score)
            self.time['text'] = time_string
            self.time.after(1000, self.tick)
    
    def stop_timer(self, calc_score=True):
        self.score = 0
        self.tick(calc_score=calc_score)
        self.timing = False
        
    
    def calculate_score(self):
        base_score = 2000
        deductions = self.sec * (100 - (self.dimension * (self.difficulty * self.difficulty)))
        deductions *= 0.24
        self.score = base_score - deductions
        if self.score <= 0:
            self.score = 0
        self.score = round(self.score, ndigits=2)
    
    def get_score(self):
        return self.score
    


    #     #
    #     # ─── CREATE COMPONENTS ───────────────────────────────────────────
    #     self.now = tk.StringVar()
    #     self.time = tk.Label(self, font=('Helvetica', 24))
        
    #     #
    #     # ─── PACK AND PLACE COMPONENTS ───────────────────────────────────
    #     self.time.pack(side="top")
    #     self.time["textvariable"] = self.now

    
    # def start_timer(self):
    #     pass

    # def stop_timer(self):
    #     pass
    
    