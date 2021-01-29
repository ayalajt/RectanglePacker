from tkinter import Tk, Canvas
import rpack
import sys
import random

class CustomCanvas:
    
    # CustomCanvas takes in two explicit arguments, and then a rectangle list
    # if rectangles are to be drawn onto the canvas
    def __init__(self, height, width):
        
        # Create canvas using the passed height and width
        self.height = height
        self.width = width
        self.window = Tk() 
        self.canvas = Canvas(self.window, height = self.height, width = self.width) 
        
class Rectangle:
    def __init__(self, height, width, x = 0, y = 0):
        self.height = height
        self.width = width
        self.x = x
        self.y = y

def pack(allRect, canvasSize):

    # in pack, first create a new list that only contains tuples of every rectangle's
    # width and height
    rectSizes = []
    for rect in allRect:
        rectSizes.append((int(rect.width), int(rect.height)))
    
    # then sort the rectangle sizes's in order of greatest height, from the biggest
    # rectangle to the smallest (This is for best results using the module rpack)
    rectSizes.sort(key=lambda x: x[1], reverse=True)

    # Then call rpack.pack, which finds the coordinates for every rectangle with no overlap
    # and with the smallest area possible
    positions = rpack.pack(rectSizes)
    
    # Then create a new rectangle object list, which grabs the respective coordinates
    # of every rectangle and creates a new rectangle object with those coordinates and also
    # uses the width and height from the sorted rectangle list
    counter = 0
    newRectList = []
    for rect in rectSizes:
        coords = positions[counter]
        newRectList.append(Rectangle(rect[1], rect[0], coords[0], coords[1]))
        counter = counter + 1

    # enclosing_size is then called to grab the grid size in which the rectangles
    # were placed in
    gridSize = rpack.enclosing_size(rectSizes, positions)

    # if the grid size made with rpack is bigger than the canvas size, then shuffle the
    # sizes list until it finds valid points that fit inside the canvas
    # (Note: this works fine with 75PercentFill but with 95PercentFill it cannot seem to
    # find a valid point list, so I would advise not running 95PercentFill since its going to fail)
    while (int(gridSize[0]) > int(canvasSize[0]) or int(gridSize[1]) > int(canvasSize[1])):
        counter = 0
        newRectList = []
        random.shuffle(rectSizes)
        positions = rpack.pack(rectSizes)
        for rect in rectSizes:
            coords = positions[counter]
            newRectList.append(Rectangle(rect[1], rect[0], coords[0], coords[1]))
            counter = counter + 1
        gridSize = rpack.enclosing_size(rectSizes, positions)
            
    return newRectList
    
def main():
    try:
        rectList = []

        # while the text file has values
        with open(sys.argv[1], "r") as filestream: 

            # the first line is going to be the canvas dimensions, so split it
            # with the comma and then store the height and with as a tuple
            firstLine = filestream.readline()
            firstLine = firstLine.split(",")
            canvasDimensions = (firstLine[0], firstLine[1])

            # the rest of the lines will consist of the rectangle sizes
            for line in filestream:
                currentLine = line.split(",")
                rectList.append(Rectangle(currentLine[0],currentLine[1]))

        # call pack with the list of rectangle objects and the canvas size
        aList = pack(rectList, canvasDimensions)
        newCanvas = CustomCanvas(canvasDimensions[0], canvasDimensions[1])

        # create the rectangles using the x, y, height, and width coordinates and draw it on the canvas
        for rect in aList:
            originX = rect.x
            originY = rect.y
            bottomX = rect.x + int(rect.width)
            bottomY = rect.y + int(rect.height)
            newCanvas.canvas.create_rectangle(originX, originY, bottomX, bottomY, fill='red')
        newCanvas.canvas.pack()
        newCanvas.window.mainloop()
    except:
        
        # If no valid file is found, print out error
        print("Error: No File Found")

if __name__ == '__main__':
    main()
