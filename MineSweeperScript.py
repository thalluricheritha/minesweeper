# This is the python implementation of minesweeper
import random as rand
from tkinter import *
from functools import partial


def create_graph(w, h):
    """ Function to create the graph for a board of n * n size """
    graph = {}
    for i in range(h):
        for j in range(w):
            neighbors = []
            # Top left
            if i - 1 >= 0 and j - 1 >= 0:
                neighbors.append((i - 1, j - 1))
            # Top
            if i - 1 >= 0:
                neighbors.append((i - 1, j))
            # Top Right
            if i - 1 >= 0 and j + 1 < w:
                neighbors.append((i - 1, j + 1))
            # Right
            if j + 1 < w:
                neighbors.append((i, j + 1))
            # Bottom Right
            if i + 1 < h and j + 1 < w:
                neighbors.append((i + 1, j + 1))
            # Bottom
            if i + 1 < h:
                neighbors.append((i + 1, j))
            # Bottom Left
            if i + 1 < h and j - 1 >= 0:
                neighbors.append((i + 1, j - 1))
            # Left
            if j - 1 >= 0:
                neighbors.append((i, j - 1))
            graph[(i, j)] = neighbors
    return graph


def add_mines(w, h, mineCount):
    mines = [[0 for col in range(w)] for row in range(h)]
    count = mineCount
    done = False
    while not done:
        for i in range(h):
            for j in range(w):
                if mines[i][j] != 1 and rand.random() > 0.91:
                    if count < 0:
                        done = True
                        break
                    mines[i][j] = 1
                    count = count - 1
    return mines


def count_surrounds(graph, i, j, mines):
    count = 0
    for neighbor in graph[i, j]:
        if mines[neighbor[0]][neighbor[1]] == 1:
            count += 1
    return count


def calc_mines(graph, mines, w, h):
    button_numbers = [[0 for col in range(w)] for row in range(h)]
    for i in range(h):
        for j in range(w):
            # add -1 if the button is over a bomb
            if mines[i][j] == 1:
                button_numbers[i][j] = -1
            # Else calculate the buttons value
            else:
                button_numbers[i][j] = count_surrounds(graph, i, j, mines)
    return button_numbers


def reveal_mines(buttons):
    for i in range(height):
        for j in range(width):
            if mines[i][j] == 1:
                buttons[i][j].configure(
                    text="", relief=SUNKEN, image=bombImage)
            buttons[i][j].configure(command='')


def recursive_reveal(buttons, i, j):
    neighbors = graph[i, j]
    grow_list = []
    for neighbor in neighbors:
        if button_numbers[neighbor[0]][neighbor[1]] == 0:
            buttons[neighbor[0]][neighbor[1]].configure(
                relief=SUNKEN, text='0', image=downImg)
            grow_list.append([neighbor[0], neighbor[1]])
            button_numbers[neighbor[0]][neighbor[1]] = 'd'
        elif button_numbers[neighbor[0]][neighbor[1]] == 1:
            buttons[neighbor[0]][neighbor[1]].configure(
                relief=SUNKEN, text='1', image=downImg)
    if len(grow_list) > 0:
        for neighbor in grow_list:
           recursive_reveal(buttons, neighbor[0], neighbor[1])


def grid_callback(i, j, buttons, btn_value):
    print(i,j);
    buttons[i][j].configure(relief=SUNKEN, text=btn_value, image=downImg)

    # Handle the game loss
    if btn_value == -1:
        reveal_mines(buttons)
    # If 0 Recursive Reveal
    if btn_value == 0:
        recursive_reveal(buttons, i, j)
    # Else
    # if btn_value == 1:
    #     buttons[i][j].configure(bg='blue')
    # elif btn_value == 2:
    #     buttons[i][j].configure(bg='green')
    # elif btn_value == 3:
    #     buttons[i][j].configure(bg='orange')
    # elif btn_value == 4:
    #     buttons[i][j].configure(bg='purple')
    # elif btn_value == -1:
    #     buttons[i][j].configure(bg='red')
    print(i, j)


# Main Method
height = 8
width = 8

# Create the graph
graph = create_graph(width, height)

total_cells = height * width
ez_density = 0.1
mine_number = total_cells * ez_density

print(total_cells, mine_number)

mines = add_mines(width, height, mine_number)

button_numbers = calc_mines(graph, mines, width, height)

print(graph[1, 1])

print("Mines")
for i in range(height):
    for j in range(width):
        print(mines[i][j], end='\t')
    print()

print("Button Numbers")

for i in range(height):
    for j in range(width):
        print(button_numbers[i][j], end='\t')
    print()


###                        ###
# : All the GUI Stuff here : #
###                        ###

root = Tk()
Grid.rowconfigure(root, 0, weight=1)
Grid.columnconfigure(root, 0, weight=1)


#Create & Configure frame
frame = Frame(root)
frame.grid(row=0, column=0)
frame.pack(side=TOP)

img = PhotoImage(file="assets/square_up.png")
downImg = PhotoImage(file="assets/square_down.png")
bombImage = PhotoImage(file="assets/square_bomb.png")
buttons = []

for row_index in range(height):
    buttons.append([])
    Grid.rowconfigure(frame, row_index, weight=1)
    for col_index in range(width):
        btn_value = button_numbers[row_index][col_index]
        Grid.columnconfigure(frame, col_index, weight=1)

        # Create button and add an anonymous function to call callback with it's coordinates
        btn = Button(frame, image=img, height=45, width=45,
                     compound=CENTER, state=None, bd=0)
        # Configure the buttons call back to call with position and it's value
        btn.configure(command=lambda i=row_index, j=col_index,
                      value=btn_value: grid_callback(i, j, buttons, value))

        btn.grid(row=row_index, column=col_index)
        buttons[row_index].append(btn)

# Add bottom frame with action buttons
menu_frame = Frame(root, bg="#F19C79")
menu_frame.pack(side=BOTTOM)
restart_button = Button(menu_frame, text="Restart")
restart_button.grid(row=0)

menu_button = Button(menu_frame, text="Main Menu")
menu_button.grid(row=0, column=1)

quit_button = Button(menu_frame, text="Quit", command=lambda x=1: quit(x))
quit_button.grid(row=0, column=2)

# Add Top Frame with


root.mainloop()
