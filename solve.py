import pygame
import sys
import math
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os

# initialize variable
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 900
block = 30


# screen
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# initialize


class place:
    def __init__(self, k, l):
        self.i = k
        self.j = l
        self.g = 0
        self.h = sys.maxsize  # maxsize
        self.neighbors = []
        self.previous = None
        self.obs = False
        self.closed = False
        self.val = 1

    def createRect(self, color, line):
        #if self.closed == False:
            rect = pygame.Rect(self.i * 30, self.j*30, 30, 30)
            pygame.draw.rect(screen, color, rect, line)
            pygame.display.update()

    def addneighbors(self, grid):
        i = self.i
        j = self.j
        if i < cols - 1 and grid[self.i + 1][j].obs == False:
            self.neighbors.append(grid[self.i + 1][j])
        if i > 0 and grid[self.i - 1][j].obs == False:
            self.neighbors.append(grid[self.i - 1][j])
        if j < rows - 1 and grid[self.i][j + 1].obs == False:
            self.neighbors.append(grid[self.i][j + 1])
        if j > 0 and grid[self.i][j - 1].obs == False:
            self.neighbors.append(grid[self.i][j - 1])

        if j > 0 and i < cols-1 and grid[self.i + 1][j-1].obs == False: #top right
            self.neighbors.append(grid[self.i + 1][j-1])
        if i > 0 and j > 0 and grid[self.i - 1][j-1].obs == False: #top left
            self.neighbors.append(grid[self.i - 1][j-1])
        if j < rows - 1 and i < cols-1 and grid[self.i + 1][j + 1].obs == False: #lower right
            self.neighbors.append(grid[self.i + 1][j + 1])
        if i > 0 and j < rows-1 and grid[self.i - 1][j + 1].obs == False: #lower left
            self.neighbors.append(grid[self.i - 1][j + 1])



cols = 30
rows = 30
grid = [0 for i in range(cols)]
openSet = []
visitedSet = []

# creating the grid
for m in range(cols):
    grid[m] = [0 for m in range(rows)]

# create place
for x in range(cols):
    for y in range(rows):
        grid[x][y] = place(x, y)

# Create rect
for x in range(cols):
    for y in range(rows):
        grid[x][y].createRect((255, 255, 255), 1)



start = grid[0][0]
final = grid[12][12]
grey = (220, 220, 220)


def onSubmit():
    global final
    ed = endBox.get().split(',')
    final = grid[int(ed[0])][int(ed[1])]
    window.quit()
    window.destroy()


# input button
window = Tk()
label = Label(window, text='Finish(x,y): ')

endBox = Entry(window)

submit = Button(window, text='Submit', command=onSubmit)

submit.grid(columnspan=2, row=3)
endBox.grid(row=1, column=1, pady=3)
label.grid(row=0, pady=3)



window.update()
mainloop()

pygame.init()
openSet.append(start)  # what???


def mousePress(x):
    t = x[0]
    w = x[1]
    g1 = t // (900 // 30)
    g2 = w //(900 // 30)
    acess = grid[g1][g2]
    if acess != start and acess != final:
        if acess.obs == False:
            acess.obs = True
            acess.createRect((205, 205, 255), 0)


start.createRect((255, 18, 127), 0)
final.createRect((255, 18, 127), 0)

loop = True
while loop:
    ev = pygame.event.get()

    for event in ev:
        if event.type == pygame.QUIT:
            pygame.quit()
        if pygame.mouse.get_pressed()[0]:
            try:
                pos = pygame.mouse.get_pos()
                mousePress(pos)
            except AttributeError:
                pass
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                loop = False
                break


for a in range(cols):
    for b in range(rows):
        grid[a][b].addneighbors(grid)



def main():
    final.createRect((255, 18, 127), 0)
    start.createRect((255, 18, 127), 0)
    curr = grid[0][0]

    start.h = 0
    lowestIndex = 0

    if len(openSet) > 0:
        temp = sys.maxsize
        for i in range(len(openSet)):
            if openSet[i].h < temp:
                temp = openSet[i].h
                lowestIndex = i

        curr = openSet[lowestIndex]

        if openSet[lowestIndex] == final:
            startFrom = curr
            innerLoop = True
            while innerLoop:
                if startFrom == start:
                    startFrom.createRect((0, 128, 0), 0)
                    innerLoop = False

                startFrom.createRect((0, 120, 0), 0)
                startFrom = startFrom.previous
                print("here")

            Tk().wm_withdraw()
            result = messagebox.askokcancel('Program Finished', (
                        'The program finished, the shortest distance \n to the path is ' + str(
                    temp) + ' blocks away, \n would you like to re run the program?'))
            if result == True:
                os.execl(sys.executable, sys.executable, *sys.argv)
            else:
                ag = True
                while ag:
                    ev = pygame.event.get()
                    for event in ev:
                        if event.type == pygame.KEYDOWN:
                            ag = False
                            break


            print('done', curr.h)
            pygame.quit()

        curr.createRect((255, 255, 102), 0)
        openSet[lowestIndex].closed = True
        openSet.pop(lowestIndex)
        visitedSet.append(curr)

        neigh = curr.neighbors

        for v in range(len(neigh)):
            if neigh[v] not in visitedSet:

                if neigh[v] in openSet and neigh[v].h > curr.h + neigh[v].val:
                    neigh[v].h = curr.h + neigh[v].val

                if neigh[v] not in openSet:
                    neigh[v].h = curr.h + neigh[v].val
                    openSet.append(neigh[v])

            if neigh[v].previous is None:
                neigh[v].previous = curr

        for i in range(len(openSet)):
            openSet[i].createRect((0, 18, 245), 0)

        # for j in range(len(visitedSet)):
        #     visitedSet[j].createRect((1, 0, 10), 0)

    curr.closed = True

# game loop
running = True
while running:
    ev = pygame.event.poll()
    if ev.type == pygame.QUIT:
        pygame.quit()
    pygame.display.update()
    main()
