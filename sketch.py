# -*- coding: utf-8 -*-
# to run script, cmd-i : https://atom.io/packages/script
from drawBot import * # needed for using as python module

# CONSTANTS:
DISPLAYWIDTH, DISPLAYHEIGHT = 500, 500
EXCLUDECOLUMN = 1 # todo can we do this in the preprocessing?
FONTSIZE = 150
FONT = 'assets/RAG-Marom-GX.ttf'
TOTALFRAMES = 1
TOTALDURATION = 1 # in seconds
BACKGROUND_R, BACKGROUND_G, BACKGROUND_B = 238, 127, 171


# PRE PROCESSING
displayTextList = DISPLAYTEXT.split(' ')
lines = len(displayTextList) # The number of lines
charsInLine = len(displayTextList[0])

font(FONT)
fontMinWidth  = listFontVariations()['wdth']['minValue']
fontMaxWidth  = listFontVariations()['wdth']['maxValue']
fontMinHeight = listFontVariations()['hght']['minValue']
fontMaxHeight = listFontVariations()['hght']['maxValue']

minDivWidth = DISPLAYWIDTH * 0.1
maxDivWidth = DISPLAYWIDTH * 0.3
minDivHeight = DISPLAYHEIGHT/2 * 0.7
maxDivHeight = DISPLAYHEIGHT/2

frame_Duration = TOTALDURATION / TOTALFRAMES

# INITIALIZE VARIABLES
xOffset =  5
yOffset = DISPLAYHEIGHT - FONTSIZE
accumulatedWidth = 0
accumulatedheight = 0


def newLine():
    t = FormattedString()
    t.fill(255,255,255)
    t.font(FONT)
    t.fontSize(FONTSIZE)
    t.openTypeFeatures(ss01=True)
    return t

# MAIN
newDrawing() # needed for using as python module
for frame in range(TOTALFRAMES):
    # Draw the background rectangle
    newPage(DISPLAYWIDTH, DISPLAYHEIGHT)
    fill(BACKGROUND_R/255, BACKGROUND_G/255, BACKGROUND_B/255)
    rect(0,0,DISPLAYWIDTH, DISPLAYHEIGHT)
    frameDuration(frame_Duration)
    for line in range(lines):
        # Create a new empty text object and set its properties
        lineTxt = newLine()
        for char in range(charsInLine):
            txt.append(
                displayTextList[line][char]
                # , # the char
                # fontVariations = dict(hght = hght_value) # create dict to put inplace of original fontVariations dict
                # fontVariations(wght=varWght) ??
                )
        text(lineTxt, (xOffset, yOffset))
        yOffset -= FONTSIZE


# Save the animation as a gif
path = "letterGrid.gif"
saveImage(path)  # or ~/Desktop/...

endDrawing() # needed for using as python module
