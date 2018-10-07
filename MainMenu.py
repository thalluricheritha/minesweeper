# coding=utf-8
#
# ─── MAINMENU CLASS ─────────────────────────────────────────────────────────────
#
from tkinter import *
# from Configuration import Configuration

class MainMenu:
    def __init__(self, master, settings):
        self.config = {}
        self.config['bg_colour'] = "#F19C79"
        self.settings = settings
        self.state = 0
        
        #
        # ─── DEFINE THE FRAME ────────────────────────────────────────────
        #
        self.frame = Frame(master, background="#F19C79", borderwidth=10, height=720, width=720)
        self.frame.pack()

        #
        # ─── DEFINE THE IMAGES ───────────────────────────────────────────
        #
        # Choose Mode Btn
        self.square_btn_img = PhotoImage(file="assets/stdBtn.png")
        self.hex_btn_img    = PhotoImage(file="assets/hexBtn.png")

        # Choose Size Btn
        self.small_btn_img  = PhotoImage(file="assets/small_btn.png")
        self.medium_btn_img = PhotoImage(file="assets/medium_btn.png")
        self.large_btn_img  = PhotoImage(file="assets/large_btn.png")

        self.normal_btn_img  = PhotoImage(file="assets/normal_btn.png")
        self.hard_btn_img    = PhotoImage(file="assets/hard_btn.png")
        self.extreme_btn_img = PhotoImage(file="assets/extreme_btn.png")
        
        # Labels
        self.title_img             = PhotoImage(file="assets/title.png")
        self.select_size_img       = PhotoImage(file="assets/select_size.png")
        self.select_difficulty_img = PhotoImage(file="assets/select_difficulty.png")

        #highscore_btn_img = PhotoImage(file="assets/highscoreBtn.png")


        #
        # ─── CREATE COMMON COMPONENTS ────────────────────────────────────
        #
        self.title_label = Label(
                                image=self.title_img,
                                bg=self.config['bg_colour']
                                )
            
        #
        # ─── CREATE SELECT MODE COMPONENTS ───────────────────────────────
        #
        self.square_button = self.create_button(self.square_btn_img, "game_mode", "SQUARE")
        self.hex_button = self.create_button(self.hex_btn_img, "game_mode", "HEX")
        
        #
        # ─── CREATE SELECT SIZE COMPONENTS ───────────────────────────────
        #
        self.select_size_label = Label(
                                image=self.select_size_img,
                                bg=self.config['bg_colour']
                                )
        self.small_button  = self.create_button(self.small_btn_img, "game_size", 8)
        self.medium_button = self.create_button(self.medium_btn_img, "game_size", 12)
        self.large_button  = self.create_button(self.large_btn_img, "game_size", 16)
        #
        # ─── CREATE SELECT DIFFICULTY COMPONENTS ─────────────────────────
        #
        self.select_difficulty_label = Label(
                                image=self.select_difficulty_img,
                                bg=self.config['bg_colour']
                                )

        self.normal_button  = self.create_button(self.normal_btn_img, "game_difficulty", 0.05)
        self.hard_button    = self.create_button(self.hard_btn_img, "game_difficulty", 0.2)
        self.extreme_button = self.create_button(self.extreme_btn_img, "game_difficulty", 0.3)
            
        #
        # ─── PACK AND PLACE COMPONENTS ───────────────────────────────────
        #
        self.square_button.pack()
        self.hex_button.pack()
        self.title_label.pack()
        self.square_button.place(bordermode=OUTSIDE, x=280, y=300)
        self.hex_button.place(bordermode=OUTSIDE, x=280, y=400)
        self.title_label.place(bordermode=OUTSIDE, x=60, y=80)


    #
    # ─── FUNCTION TO CREATE A BUTTON OBJECT ─────────────────────────────────────────
    #
    def create_button(self, display_image, spec_key, spec_value):
        return Button(
                self.frame,
                image=display_image,
                command=lambda key=spec_key, value=spec_value: self.save_setting(key, value),
                width=149,
                height=47,
                bg=self.config['bg_colour'],
                relief=FLAT,
                borderwidth=0,
                highlightthickness=0,
                bd=0
             )


    #
    # ─── FUNCTION FOR STATE SWITCHING ───────────────────────────────────────────────
    #
    def switch_state(self):
        self.state += 1
        if self.state == 1:
            self.clean_components("MODE")
            self.display("SIZE");
        elif self.state == 2:
            self.clean_components("SIZE")
            self.display("DIFFICULTY")
        else:
            self.clean_components("DIFFICULTY")
            self.stop_menu()
            

    #
    # ─── DISPLAY GROUPS OF COMPONENTS ───────────────────────────────────────────────
    #
    def display(self, group):
        if group == "SIZE":
            # ─── PACK AND PLACE SIZE SELECTION COMPONENTS ────────────────────
            self.select_size_label.pack()
            self.small_button.pack()
            self.medium_button.pack()
            self.large_button.pack()

            self.small_button.place(bordermode=OUTSIDE, x=280, y=350)
            self.medium_button.place(bordermode=OUTSIDE, x=280, y=450)
            self.large_button.place(bordermode=OUTSIDE, x=280, y=550)
            self.select_size_label.place(bordermode=OUTSIDE, x=165, y=250)
        elif group == "DIFFICULTY":
            # ─── PACK AND PLACE DIFFICULTY SELECTION COMPONENTS ──────────────
            self.select_difficulty_label.pack()
            self.normal_button.pack()
            self.hard_button.pack()
            self.extreme_button.pack()

            self.normal_button.place(bordermode=OUTSIDE, x=280, y=350)
            self.hard_button.place(bordermode=OUTSIDE, x=280, y=450)
            self.extreme_button.place(bordermode=OUTSIDE, x=280, y=550)
            self.select_difficulty_label.place(bordermode=OUTSIDE, x=165, y=250)


    #
    # ─── FUNCTION TO SAVE A SETTING ─────────────────────────────────────────────────
    #
    def save_setting(self, setting_key, setting_value, quit=False):
        self.settings[setting_key] = setting_value
        print("Setting Key:", setting_key, "Setting Value:", setting_value)
        self.switch_state();


    #
    # ─── FUNCTION TO EXIT THE MAIN MENU ─────────────────────────────────────────────
    #
    def stop_menu(self):
        self.frame.destroy()
        self.frame.quit()
    

    #
    # ─── FUNCTION TO DESTROY ALL COMPONENTS [CLEAN UP] ──────────────────────────
    #
    def clean_components(self, group):
        if group == "MODE":
            self.square_button.destroy()
            self.hex_button.destroy()
        elif group == "SIZE":
            self.small_button.destroy()
            self.medium_button.destroy()
            self.large_button.destroy()
            self.select_size_label.destroy()
        elif group == "DIFFICULTY":
            self.title_label.destroy()
            self.normal_button.destroy()
            self.hard_button.destroy()
            self.extreme_button.destroy()
            self.select_difficulty_label.destroy()
        