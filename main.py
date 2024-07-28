from curses import initscr,endwin
from signal import signal,SIGWINCH
from time import sleep

import random

stdscr=initscr()

####################################################################

def generateBord():
    Board=[]

    Rows,Cols=stdscr.getmaxyx()
    for _ in range(Rows-2):
        Board.append([" " for _ in range(Cols-2)])

    return Board

####################################################################

def generateStartConf(Board,Rows,Cols,Number):
    for Iter in range(Number):
        y=random.randrange(Rows-2)
        x=random.randrange(Cols-2)

        Board[y][x]="O"

    return Board

####################################################################

def drawBoard(Board,Cols):
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
    stdscr.addnstr(0,1," GAME OF LIFE ",Cols-1)
    # Draw border with name of program

    Board=generateBord()

    Board=generateStartConf(Board,Rows,Cols,100)

    drawBoard(Board,Cols)

    stdscr.refresh()

####################################################################

def resizeHandler(Signum,Frame):
    endwin()
    # This could lead to crashes according to below comment
    stdscr.refresh()
    drawStdScreen()

####################################################################

signal(SIGWINCH,resizeHandler)

####################################################################    

def main():

    initscr()

    try:
        drawStdScreen()
        while 1:
            # print stuff with curses
            sleep(1)
    except (KeyboardInterrupt, SystemExit):
        pass
    except Exception as e:
        pass

    endwin()

####################################################################

