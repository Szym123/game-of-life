from curses import initscr,endwin
from signal import signal,SIGWINCH

import random
import time

####################################################################

stdscr=initscr()
Board=[]
NewBoard=[]

####################################################################

def openFile(Name):
    Tab=[]

    try:
        File=open(Name,"r")
        # open a file in read mode

        while True:
            Line=File.readline()
            if not Line:
                break
            Tab.append(Line)
        # read file line by line

        return Tab
        # return table of line

    except:
        print("There is problem with config.txt")
        exit()

####################################################################

def parsConfig(Tab):
    NewTab=[]
    for Item in Tab:
        if "#"==Item[0]:
            continue
        # Not read line started with "#"
        NewTab.append(Item.split("="))

    Dictionary={}
    for Item in NewTab:
        Dictionary[Item[0]]=Item[1].rstrip()

    return Dictionary

####################################################################

def generateBoard(Size):
    for _ in range(Size):
        Board.append([" " for _ in range(Size)])
    # Generate matrix of dead cell with specific size

    for _ in range(Size):
        NewBoard.append([" " for _ in range(Size)])

####################################################################

def parsSeed(Tab):
    for IterY in range(len(Tab)):
        for IterX in range(len(Tab[IterY])):
            if Tab[IterY][IterX]=="O":
                Board[IterY][IterX]="O"

####################################################################

def modifiedGauss(Range):
    while True:
        Result=int(random.gauss(Range/2,8.0))

        if 0<=Result<=Range:
            return Result

####################################################################

def generateStartConf(Rows,Cols,Number,Range,Option):
    for Iter in range(Number):
        if Option=="fixed":
            y=random.randrange(Rows-2)
            x=random.randrange(Cols-2)
        # Generate with fixed distribution

        elif Option=="triang":
            y=int(Range*random.triangular(0,1))
            x=int(Range*random.triangular(0,1))
        # Generate with triangular distribution

        elif Option=="gauss":
            y=modifiedGauss(50)
            x=modifiedGauss(50)
        # Generate with Gauss distribution

        Board[y][x]="O"
        # Generate radom position of living cell

####################################################################

def drawBoard(Rows,Cols):
    for PosY in range(Rows-2):
        String=""
        for PosX in range(Cols-2):
            String+=Board[PosY][PosX]

        stdscr.addnstr(PosY+1,1,String,Cols-1)

####################################################################

def drawStdScreen():
    Rows,Cols=stdscr.getmaxyx()
    # Calculate size of window

    stdscr.clear()

    stdscr.border()
    stdscr.addnstr(0,1," Game of Life ",Cols-1)
    # Draw border with name of program

    drawBoard(Rows,Cols)

    stdscr.addnstr(Rows-1,1," Step: 1 ",Cols-1)

    stdscr.refresh()

####################################################################

def resizeHandler(Signum,Frame):
    endwin()
    # This could lead to crashes according to below comment
    stdscr.refresh()
    drawStdScreen()

####################################################################

def sumOfNeighbors(PosY,PosX):
    Sum=0

    IterY=PosY-1
    while IterY<=(PosY+1):
        IterX=PosX-1
        while IterX<=(PosX+1):
            try:
                if (IterX!=PosX or IterY!=PosY) and Board[IterY][IterX]=="O":
                    Sum+=1
            except:
                pass
            IterX+=1
        IterY+=1

    return Sum

####################################################################

def calculateTransformation(Size):
    IterY=0
    while IterY<(Size):
        IterX=0
        while IterX<(Size):
            Sum=sumOfNeighbors(IterY,IterX)

            if Board[IterY][IterX]==" " and Sum==3:
                NewBoard[IterY][IterX]="O"
            # When dead cell have 3 neighbors, he start be alive

            if Board[IterY][IterX]=="O" and Sum in [2,3]:
                NewBoard[IterY][IterX]="O"
            # When alive cell have 2 or 3 neighbors, he stay alive

            if not(Sum in [2,3]):
                NewBoard[IterY][IterX]=" "
            # When cell have other number of neighbors, than 2 or 3, 
            # he start or stay dead

            IterX+=1
        IterY+=1

####################################################################

def copyArray(Size):
    for Iter in range(len(NewBoard)):
        Board[Iter]=NewBoard[Iter]
        NewBoard[Iter]=[" " for _ in range(Size)]
    # This update all cells in same time

####################################################################

signal(SIGWINCH,resizeHandler)

####################################################################    

def main():
    Tab=openFile("config.txt")
    Dictionary=parsConfig(Tab)
    # Dowload and pars configuration data

    initscr()

    Rows,Cols=stdscr.getmaxyx()
    generateBoard(int(Dictionary["board_size"]))
    #generateStartConf(Rows,Cols,int(Dictionary["numbers_of_cell"]),80,Dictionary["random_distribution"])
    # Generate board with start configuration

    Seed=openFile("seed.txt")
    parsSeed(Seed)

    try:
        drawStdScreen()
        # Draw all TUI

        Iter=1
        while True:
            time.sleep(float(Dictionary["sleep_time"]))

            calculateTransformation(int(Dictionary["board_size"]))
            copyArray(int(Dictionary["board_size"]))
            # Calculate new position of cells and 
            # update them in same time

            drawBoard(Rows,Cols)
            # Redraw board

            stdscr.addnstr(Rows-1,1," Step: "+str(Iter)+" ",Cols-1)
            # Redraw number of step

            Iter+=1

            stdscr.refresh()

    except (KeyboardInterrupt, SystemExit):
        pass
    except Exception as e:
        pass

    endwin()

####################################################################

if __name__=="__main__":
	main()