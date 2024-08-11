#!/usr/bin/env python3
# -*- coding: utf8 -*-

from curses import initscr,endwin
from signal import signal,SIGWINCH

import random
import time
import sys
import getopt

####################################################################

stdscr=initscr()
Board=[]
NewBoard=[]

####################################################################

def handlingError(Text):
    endwin()
    print(Text)
    exit()

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
        handlingError("There is problem with "+str(Name))
        # return file error

####################################################################

def parsConfig(Tab):
    try:
        NewTab=[]
        for Item in Tab:
            if "#"==Item[0]:
                continue
            # Not read line started with "#"
            if "\n"==Item:
                continue
            # Not read blank line
            NewTab.append(Item.split("="))
            # Add new item ass list to NewTab

        Dictionary={}
        for Item in NewTab:
            Dictionary[Item[0]]=Item[1].rstrip()
        # Add item from NewTab as new entry to dictionary

        return Dictionary
    except:
        handlingError("There is problem with config file")

####################################################################

def generateBoard(Size):
    for _ in range(Size):
        Board.append([" " for _ in range(Size)])
    # Generate matrix of dead cell with specific size

    for _ in range(Size):
        NewBoard.append([" " for _ in range(Size)])
    # Generate matrix of dead cell with specific size

####################################################################

def parsSeed(Seed):
    for IterY in range(len(Seed)):
        for IterX in range(len(Seed[IterY])):
            if Seed[IterY][IterX]=="O":
                Board[IterY][IterX]="O"
            # when in a particular position in seed is living cell
            # copy them to board

####################################################################

def modifiedGauss(Range):
    while True:
        Result=int(random.gauss(Range/2,8.0))
        # Generate random variable from Gauss distribution

        if 0<=Result<=Range:
            return Result
        # Return varieble only when is between 0 and range

####################################################################

def generateStartConf(Number,Range,Option):
    for _ in range(Number):
        if Option=="fixed":
            y=random.randrange(Range)
            x=random.randrange(Range)
        # Generate from fixed distribution

        elif Option=="triang":
            y=int(Range*random.triangular(0,1))
            x=int(Range*random.triangular(0,1))
        # Generate from triangular distribution

        elif Option=="gauss":
            y=modifiedGauss(Range)
            x=modifiedGauss(Range)
        # Generate with Gauss distribution

        Board[y][x]="O"
        # Generate radom position of living cell

####################################################################

def drawBoard(Rows,Cols):
    for PosY in range(Rows-2):
        String=""
        for PosX in range(Cols-2):
            try:
                String+=Board[PosY][PosX]
            except:
                String+=" "
        # Sum cell from line in board into string

        stdscr.addnstr(PosY+1,1,String,Cols-1)
        # Draw line of board

####################################################################

def drawStdScreen():
    Rows,Cols=stdscr.getmaxyx()
    # Calculate size of window

    stdscr.clear()

    stdscr.border()
    stdscr.addnstr(0,1," Game of Life ",Cols-1)
    # Draw border with name of program

    drawBoard(Rows,Cols)
    # Draw board with cell

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

def getHelp():
    endwin()
    
    print("Usage: ./main.py [OPTION]...")
    print("implementation of the Game of Life,")
    print("generates a board filled with cells and allows you to observe their development")
    print("")
    print(" -c / --config=FILE   reads the settings from the specified FILE, the default is config.txt")
    print(" -s / --seed=FILE     reads the initial state from the specified FILE")
    print(" -l / --len           display size of your window (how many characters will fit)")
    print(" -h / --help          display this help and exit")
    print("")

    exit()

####################################################################

def printLen():
    Rows,Cols=stdscr.getmaxyx()
    endwin()

    print("Size of window:")
    print("x: "+str(Cols))
    print("y: "+str(Rows))
    print("")

    exit()

####################################################################

def parsFlag():
    Dictionary={'config':'config.txt'}

    try:
        Opts,Args=getopt.getopt(sys.argv[1:],"s:c:hl",["seed=","config=","help","len"])
        #Reading command line option
        for O,B in Opts:
            if O in("-s","--seed"):
                Dictionary["seed"]=B
            elif O in("-c","--config"):
                Dictionary["config"]=B
            elif O in("-h","--help"):
                Dictionary["help"]="help"
            elif O in ("-l","--len"):
                Dictionary["len"]="len"
        # Pars command line option

        return Dictionary
    except:
        handlingError("Incorrect flags or values")
        # Return flag error

####################################################################

def findConfigError(Dictionary):
    for Item in ["board_size","numbers_of_cell"]:
        if Item in Dictionary:
            try:
                Dictionary[Item]=int(Dictionary[Item])
            except:
                handlingError("There is problem with ",Item)
        else:
            handlingError(Item+" does not exits")
    # Finding error in:
    # - board_size -> int
    # - numbers_of_cell - > int

    if "sleep_time" in Dictionary:
        try:
            Dictionary["sleep_time"]=float(Dictionary["sleep_time"])
        except:
            handlingError("There is problem with sleep_time")
    else:
        handlingError("sleep_time does not exits")
    # Finding error in sleep_time -> float

    if "random_distribution" in Dictionary:
        try:
            Dictionary["random_distribution"]=str(Dictionary["random_distribution"])
        except:
            handlingError("There is problem with random_distribution")
    else:
        handlingError("random_distribution does not exits")
    # Finding error in random_distribution -> str

    return Dictionary

####################################################################

def sumAllCell():
    Sum=0
    for Line in Board:
        for Cell in Line:
            if Cell=="O":
                Sum+=1

    return Sum

####################################################################

signal(SIGWINCH,resizeHandler)
# System interrupt

####################################################################    

def main():
    Flag=parsFlag()

    if "help" in Flag:
        getHelp()
    # print help and exit
    elif "len" in Flag:
        printLen()
    # print size of window

    Tab=openFile(Flag["config"])
    Dictionary=parsConfig(Tab)
    Dictionary=findConfigError(Dictionary)
    # Dowload and pars configuration data

    generateBoard(Dictionary["board_size"])
    # Generate board

    if "seed" in Flag:
        Seed=openFile(Flag["seed"])
        parsSeed(Seed)
        # Generate start cell configuration using seed
    else:   
        generateStartConf(Dictionary["numbers_of_cell"],Dictionary["board_size"],Dictionary["random_distribution"])
        # Generate random start cell configuretion

    initscr()

    try:
        drawStdScreen()
        # Draw all TUI

        Iter=1
        while True:
            Rows,Cols=stdscr.getmaxyx()

            stdscr.addnstr(Rows-1,1," Step: "+str(Iter),Cols-1)
            # Draw number of step

            stdscr.addnstr(Rows-1,14," Number of cell: "+str(sumAllCell()),Cols-1)
            # Draw sum of cell

            time.sleep(Dictionary["sleep_time"])

            calculateTransformation(Dictionary["board_size"])
            copyArray(Dictionary["board_size"])
            # Calculate new position of cells and 
            # update them in same time

            drawBoard(Rows,Cols)
            # Redraw board

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