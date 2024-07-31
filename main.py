from curses import initscr,endwin
from signal import signal,SIGWINCH
from time import sleep

import random
import time

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
            Tab.append(Line.split())
        # read file line by line

        return Tab
        # return table of line

    except:
        return -1

####################################################################

def settingParsing(Board):
    pass

####################################################################

def generateBord():

    Rows,Cols=stdscr.getmaxyx()
    for _ in range(Rows-2):
        Board.append([" " for _ in range(Cols-2)])
    # Generate matrix of dead cell with specific size

    for _ in range(Rows-2):
        NewBoard.append([" " for _ in range(Cols-2)])

####################################################################

def generateStartConf(Rows,Cols,Number):
    for Iter in range(Number):
        y=random.randrange(Rows-2)
        x=random.randrange(Cols-2)
        # Generate radom position of living cell

        Board[y][x]="O"

####################################################################

def drawBoard(Cols):
    Iter=1
    for Line in Board:
        String="".join(Line)
        stdscr.addnstr(Iter,1,String,Cols-1)
        Iter+=1 

####################################################################

def drawStdScreen():
    Rows,Cols=stdscr.getmaxyx()
    # Calculate size of window

    stdscr.clear()

    stdscr.border()
    stdscr.addnstr(0,1," Game of Life ",Cols-1)
    # Draw border with name of program

    drawBoard(Cols)

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

def calculateTransformation(Rows,Cols):
    IterY=0
    while IterY<(Rows-2):
        IterX=0
        while IterX<(Cols-2):
            Sum=sumOfNeighbors(IterY,IterX)

            if Sum==3:
                NewBoard[IterY][IterX]="O"

            if not(Sum in [2,3]):
                NewBoard[IterY][IterX]=" "

            IterX+=1
        IterY+=1

####################################################################

def copyArray():
    Iter=0
    for Item in NewBoard:
        Board[Iter]=Item
        Iter+=1

####################################################################

signal(SIGWINCH,resizeHandler)

####################################################################    

def main():

    initscr()

    Rows,Cols=stdscr.getmaxyx()
    generateBord()
    generateStartConf(Rows,Cols,400)

    try:
        drawStdScreen()
        Iter=1
        while True:
            time.sleep(0.1)

            calculateTransformation(Rows,Cols)

            copyArray()

            drawBoard(Cols)

            stdscr.addnstr(Rows-1,1," Step: "+str(Iter),Cols-1)
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