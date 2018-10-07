# coding=utf-8
#####   ---------------------------------------------------------------   #####
##                               Board Class                                 ##
##                Contains Model Representation of a Game Board              ##
#####   ---------------------------------------------------------------   #####
import random as rand


class Board:
    def __init__(self, board_type, difficulty, dimension):
        self.type = board_type
        self.dimension = dimension
        
        self.graph = self.create_graph(type, dimension, dimension)

        self.cell_count = dimension * dimension
        self.mine_count = difficulty * self.cell_count
        self.mines = self.add_mines(dimension, dimension, self.mine_count)
        self.button_numbers = self.calc_mines(self.graph, self.mines, dimension, dimension)
        
        self.toggles = [[False] * dimension for _ in range(dimension)]
        self.covers = [[False] * dimension for _ in range(dimension)]
        self.game_over = False
        self.game_win = False

        # for i in range(self.dimension):
        #     for j in range(self.dimension):
        #         if self.button_numbers[i][j] == -1:
        #             print(j,i, "Neighbors:", self.graph[j,i] )


#
# ─── SETUP FUNCTIONS ────────────────────────────────────────────────────────────
#
    def create_graph(self, type, w, h):
        """ Function to create the graph for a board of n * n size """
        graph = {}
        for j in range(h):
            for i in range(w):
                neighbors = []
                # Top left
                if i % 2 == 0 or self.type == "SQUARE":
                    if i - 1 >= 0 and j - 1 >= 0:
                        neighbors.append((i - 1, j - 1))
                # Top
                if i - 1 >= 0:
                    neighbors.append((i - 1, j))
                # Top Right
                if i % 2 == 1 or self.type == "SQUARE":
                    if i - 1 >= 0 and j + 1 < w:
                        neighbors.append((i - 1, j + 1))
                # Right
                if j + 1 < w:
                    neighbors.append((i, j + 1))
                # Bottom Right
                if i % 2 == 1 or self.type == "SQUARE":
                    if i + 1 < h and j + 1 < w:
                        neighbors.append((i + 1, j + 1))
                # Bottom
                if i + 1 < h:
                    neighbors.append((i + 1, j))
                # Bottom Left
                if i % 2 == 0 or self.type == "SQUARE":
                    if i + 1 < h and j - 1 >= 0:
                        neighbors.append((i + 1, j - 1))
                # Left
                if j - 1 >= 0:
                    neighbors.append((i, j - 1))
                graph[(i,j)] = neighbors
        return graph


    def add_mines(self, w, h, mineCount):
        mines = [[0 for col in range(w)] for row in range(h)]
        count = mineCount
        done = False
        while not done:
            for j in range(h):
                for i in range(w):
                    if mines[i][j] != 1 and rand.random() > 0.91:
                        if count <= 0:
                            done = True
                            break
                        mines[i][j] = 1
                        count = count - 1
        return mines


    def increment_surrounds(self, graph, button_numbers, i, j):
        for neighbor in graph[i,j]:
            if button_numbers[neighbor[0]][neighbor[1]] == -1:
                continue
            else:
                button_numbers[neighbor[0]][neighbor[1]] += 1


    def calc_mines(self, graph, mines, w, h):
        button_numbers = [[0 for col in range(h)] for row in range(w)]
        for j in range (h):
            for i in range(w):
                # add -1 if the button is over a bomb
                if mines[i][j] == 1:
                    button_numbers[i][j] = -1
                    self.increment_surrounds(graph, button_numbers, i, j)
                
        return button_numbers
    
    
#
# ─── STATE MODIFICATION FUNCTIONS ───────────────────────────────────────────────
#
    def recursive_reveal(self, i, j):
        neighbors = self.graph[i,j]
        grow_list = []
        for neighbor in neighbors:
            n_i = neighbor[0]
            n_j = neighbor[1]
            if self.covers[n_i][n_j]:
                continue
            if self.button_numbers[n_i][n_j] == 0:
                # Toggle the button
                self.toggles[n_i][n_j] = True
                # Add the button to the grow list
                grow_list.append([n_i,n_j])
                # Set to English 'zero' to prevent endless recursion
                self.button_numbers[n_i][n_j] = 'zero'
            elif self.button_numbers[n_i][n_j] == 1 or 2:
                # Toggle the 'button'
                self.toggles[n_i][n_j] = True
        if grow_list:
            for neighbor in grow_list:
                self.recursive_reveal(neighbor[0], neighbor[1])

    def toggle_button(self, i, j):
        if self.toggles[i][j]:
            return
        if self.covers[i][j]:
            self.covers[i][j] = False
            return
        self.toggles[i][j] = True
        button_value = self.button_numbers[i][j]
        if button_value == 0:
            self.recursive_reveal(i,j)
        elif button_value == -1:
            self.game_over = True

    def cover_button(self, i, j):
        if self.toggles[i][j]:
            return
        if self.covers[i][j]:
            self.covers[i][j] = False
        else:
            self.covers[i][j] = True
    
    def cover_match(self):
        difference = 0
        for i in range(self.dimension):
            for j in range(self.dimension):
                if self.covers[i][j] == True and self.button_numbers[i][j] != -1:
                    difference += 1
                elif self.covers[i][j] == False and self.button_numbers[i][j] == -1:
                    difference += 1
        if difference == 0:
            self.game_win = True

#
# ─── GETTERS ────────────────────────────────────────────────────────────────────
#
    def get_state_toggles(self):
        return self.toggles

    def get_state_button_numbers(self):
        return self.button_numbers

    def get_state_board_type(self):
        return self.board_type

    def get_state_loss(self):
        return self.game_over

    def get_state_mines(self):
        return self.mines

    def get_state_covers(self):
        return self.covers

    def get_state_win(self):
        self.cover_match()
        return self.game_win
