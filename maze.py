import tkinter as gui
from time import sleep
from random import choice, randint
# import os
# import math
# import keyboard
# import turtle
# import sys
# from cryptography.fernet import Fernet
# import string

class Maze:
    def __init__(self, grids_x = 10, grids_y = 10, solve = True) -> None:
        self.root = gui.Tk()
        self.root.configure(bg='#2a2b2e')

        #grid = [left wall, bottem wall, right wall, top wall]
        self.grids = []
        self.grid_box = []
        self.checked_walls = []
        self.checked_grids = []
        self.grids_ = []
        self.path = [[0, 0]]
        self.end = [0, 0]

        self.grids_x = grids_x
        self.grids_y = grids_y
        self.screen_size_x = self.root.winfo_screenwidth()
        self.screen_size_y = self.root.winfo_screenheight()
        self.window_size_x = 750
        self.window_size_y = 750
        self.canvas_size_x = 750
        self.canvas_size_y = 750
        self.grid_size_x = self.canvas_size_x//grids_x
        self.grid_size_y = self.canvas_size_y//grids_y

        self.rand_nums = [randint(0, 3) for i in range(2)]

        self.root.geometry(f'{self.window_size_x}x{self.window_size_y}+{(self.screen_size_x - self.window_size_x)//2}+{(self.screen_size_y - self.window_size_y)//2}')

        self.canvas = gui.Canvas(bg='black', highlightbackground='red', highlightthickness=5, height=self.canvas_size_x, width=self.canvas_size_y)
        self.canvas.pack(expand=1)

        def fun():
            self.draw_grid()
            self.generate_maze()
            # self.current_pos = [randint(0, self.grids_x - 1), randint(0, self.grids_y - 1)]
            self.end = [randint(0, self.grids_x - 1), randint(0, self.grids_y - 1)]
            self.canvas.itemconfigure(self.grid_box[self.end[0]][self.end[1]], fill='red')
            self.canvas.itemconfigure(self.grid_box[self.path[0][0]][self.path[0][1]], fill='white')
            self.canvas.update()
            
            self.root.bind('w', lambda event: self.button_clicked('top'))
            self.root.bind('a', lambda event: self.button_clicked('left'))
            self.root.bind('s', lambda event: self.button_clicked('bot'))
            self.root.bind('d', lambda event: self.button_clicked('right'))

        self.root.after(0, fun)
        self.root.mainloop()

    def draw_grid(self):
        for j in range(self.grids_y):
            self.grids.append([])
            self.grid_box.append([])
            for i in range(self.grids_x):
                self.grids[j].append([None, None, None, None])
                self.grid_box[j].append([])

        for j in range(1, self.grids_y):
            for i in range(self.grids_x):
                self.grids[j][i][3] = self.canvas.create_line(5+i*self.grid_size_x, 5+j*self.grid_size_y, 5+(i+1)*self.grid_size_x, 5+j*self.grid_size_y, fill='red', width=5)
                if j > 0:
                    self.grids[j - 1][i][1] = self.grids[j][i][3]

        for j in range(1, self.grids_x):
            for i in range(self.grids_y):
                self.grids[i][j][0] = self.canvas.create_line(5+j*self.grid_size_x, 5+i*self.grid_size_y, 5+j*self.grid_size_x, 5+(i+1)*self.grid_size_y, fill='red', width=5)
                if j > 0:
                    self.grids[i][j - 1][2] = self.grids[i][j][0]

        for i in range(self.grids_x):
            for j in range(self.grids_y):
                self.grid_box[j][i] = self.canvas.create_oval(i*self.grid_size_x + 5 + 10, j*self.grid_size_y + 5 + 10, (i + 1)*self.grid_size_x + 5 - 10, (j + 1)*self.grid_size_y + 5 - 10, fill='green')

        self.root.update()

    def generate_maze(self):

        def get_moves(grid):
            moves = self.grids[grid[0]][grid[1]].copy()
            index = 0
            while True:
                if index == len(moves):
                    break
                wall = moves[index]
                if not wall:
                    moves.pop(index)
                    continue
                row, col = grid[0], grid[1]
                i = self.grids[row][col].index(wall)
                if i == 0:
                    col-=1
                elif i == 1:
                    row+=1
                elif i == 2:
                    col+=1
                elif i == 3:
                    row-=1
                if [row, col] in self.checked_grids:
                    moves.pop(index)
                    continue
                index += 1
            return moves
        
        self.checked_grids.append([0, 0])
        self.grids_.append([0, 0])
        
        while True:
            if len(self.checked_grids) == self.grids_x*self.grids_y:
                break
            moves = get_moves(self.grids_[-1])
            row = self.grids_[-1][0]
            col = self.grids_[-1][1]

            # for i in self.grid_box:
            #     for j in i:
            #         self.canvas.itemconfigure(j, fill='black')
            # self.canvas.itemconfigure(self.grid_box[row][col], fill='white')
            # self.root.update()
            # sleep(0.05)

            if moves:
                # tries = 0
                # while True:
                #     tries += 1
                num = randint(0, len(moves) - 1)
                    # if num not in self.rand_nums or tries >= 5:
                    #     self.rand_nums.pop(0)
                    #     self.rand_nums.append(num)
                    #     break
                wall = moves[num]
                self.checked_walls.append(wall)
                index = self.grids[self.grids_[-1][0]][self.grids_[-1][1]].index(wall)
                moves.remove(wall)
                
                # sleep(0.01)
                # for i in moves:
                #     self.canvas.itemconfigure(i, fill='red')
                # self.root.update()

                self.canvas.delete(wall)
                if index == 0:
                    col-=1
                elif index == 1:
                    row+=1
                elif index == 2:
                    col+=1
                elif index == 3:
                    row-=1
                self.checked_grids.append([row, col])
                self.grids_.append([row, col])
            else:
                self.grids_.pop(-1)

        for i in self.grid_box:
            for j in i:
                self.canvas.itemconfigure(j, fill='black')

    def solve_maze(self):
        pass

    def button_clicked(self, direction = None):
        def get_moves():
            walls = self.grids[self.path[-1][0]][self.path[-1][1]]
            directions = []
            for i in walls:
                if i and i in self.checked_walls:
                    if walls.index(i) == 0:
                        directions.append('left')
                    if walls.index(i) == 1:
                        directions.append('bot')
                    if walls.index(i) == 2:
                        directions.append('right')
                    if walls.index(i) == 3:
                        directions.append('top')
            return directions
        
        self.canvas.itemconfigure(self.grid_box[self.path[-1][0]][self.path[-1][1]], fill=('white', 'black')[0 if [self.path[-1][0], self.path[-1][1]] in self.path else 1])
        row, col = self.path[-1]
        moves = get_moves()
        if not direction or direction == -1:
            if len(moves) <= 2 and (len(self.path) >= 2):
                _row, _col = self.path[-2]
                if col - _col == 1:
                    _from = 'left'
                if col - _col == -1:
                    _from = 'right'
                if row - _row == 1:
                    _from = 'top'
                if row - _row == -1:
                    _from = 'bot'
                if _from in moves:
                    moves.remove(_from)
                if moves:
                    if direction == -1:
                        direction = _from
                    else:
                        direction = moves[0]
                else:
                    return
                moves = get_moves()
            else:
                return
            
        if direction in moves:
            if direction == 'left':
                if col != 0:
                    col -= 1
            elif direction == 'bot':
                if row != self.grids_x - 1:
                    row += 1
            elif direction == 'right':
                if col != self.grids_y - 1:
                    col += 1
            elif direction == 'top':
                if row != 0:
                    row -= 1
            if [row, col] in self.path:
                self.canvas.itemconfigure(self.grid_box[self.path[-1][0]][self.path[-1][1]], fill=('white', 'black')[1])
                self.path.pop(-1)
                self.canvas.update()
                sleep(0.05)
                self.button_clicked(direction=-1)
            else:
                self.path.append([row, col])
                self.canvas.update()
                sleep(0.05)
                self.button_clicked()

Maze(50, 50)