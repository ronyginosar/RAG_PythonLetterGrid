# -*- coding: utf-8 -*-
# to run script, cmd-i : https://atom.io/packages/script
from drawBot import * # needed for using as python module

# CONSTANTS:
DISPLAYTEXT = "מטבחים"
# DISPLAYTEXT = "hello"
# DISPLAYTEXT = "מטבחים מערכות מבטחים"
EXCLUDECOLUMN = 4 # todo can we do this in the preprocessing?
FONTSIZE = 150
FONT = 'assets/RAG-Marom-GX.ttf'
TOTALFRAMES = 1
TOTALDURATION = 1 # in seconds
BACKGROUND_R, BACKGROUND_G, BACKGROUND_B = 238, 127, 171
MARGINS = 10

# PRE PROCESSING - TEXT
displayTextList = DISPLAYTEXT.split(' ')
lines = len(displayTextList) # The number of lines
charsInLine = len(displayTextList[0])
# PRE PROCESSING - FONT
font(FONT)
fontMinWidth = listFontVariations()['wdth']['minValue']
fontMaxWidth = listFontVariations()['wdth']['maxValue']
fontMinHeight = listFontVariations()['hght']['minValue']
fontMaxHeight = listFontVariations()['hght']['maxValue']
# PRE PROCESSING - DISPLAY
DISPLAYWIDTH, DISPLAYHEIGHT = 500, FONTSIZE*lines
SCREENWIDTH = DISPLAYWIDTH + MARGINS*2
SCREENHEIGHT = DISPLAYHEIGHT + MARGINS*2
minLetterWidth = int(DISPLAYWIDTH * 0.1)
maxLetterWidth = int(DISPLAYWIDTH * 0.5)
minLetterHeight = int(DISPLAYHEIGHT/2 * 0.7)
maxLetterHeight = int(DISPLAYHEIGHT/2)

frame_Duration = TOTALDURATION / TOTALFRAMES

# not sure:
# for i,line in enumerate(displayTextList):
#     displayTextList[i] = list(line)
# for line in displayTextList:
#     line.reverse()

print(displayTextList)

# INITIALIZE VARIABLES
xOffset = 0
yOffset = MARGINS
# accumulatedWidth = 0
accumulatedHeight = [0] * charsInLine # acc height per column

def newLine():
    t = FormattedString()
    t.fill(255,255,255)
    t.font(FONT)
    t.fontSize(FONTSIZE)
    t.openTypeFeatures(ss01=True)
    return t

# print(minLetterWidth, maxLetterWidth, minLetterHeight, maxLetterHeight) # TEST
def getVariableSettings(row, col, accumulatedWidth):
    # global accumulatedWidth, accumulatedHeight
    if (row==0):
        if (col==EXCLUDECOLUMN):
            currentwidth = minLetterWidth
            variableWdth = fontMinWidth
        else :
            # variableWdth regards letters before
            currentmaxwidth = max((DISPLAYWIDTH - accumulatedWidth)*0.5, minLetterWidth)
            currentwidth = randint(minLetterWidth, int(currentmaxwidth))
            variableWdth = mapWidthToFont(currentwidth)
            if (col==charsInLine-1):
                currentwidth = DISPLAYWIDTH - accumulatedWidth
                variableWdth = mapWidthToFont(currentwidth)
                # print (accumulatedWidth, currentwidth, currentwidth+currentlinewidth)

    # TODO
    variableHght = 100
    # variableHght = randint(fontMinHeight, fontMaxHeight)
    # accumulatedHeight[col] += variableHght

    # print ("current range", int(currentmaxwidth), minLetterWidth,
    #         "currentwidth", currentwidth,
    #         "variableWdth", variableWdth)
    return variableWdth, variableHght

def mapWidthToFont(currentwidth):
    return int(mapValue(currentwidth,
                    minLetterWidth, maxLetterWidth,
                    fontMinWidth, fontMaxWidth))

def mapValue(value, oldmin, oldmax, newmin, newmax):
    return (value - oldmin) / (oldmax - oldmin) * (newmax - newmin) + newmin

# MAIN
newDrawing() # needed for using as python module
for frame in range(TOTALFRAMES):
    # Draw the background rectangle
    newPage(SCREENWIDTH, SCREENHEIGHT)
    fill(BACKGROUND_R/255, BACKGROUND_G/255, BACKGROUND_B/255)
    rect(0,0,SCREENWIDTH, SCREENHEIGHT)
    fill(None)
    stroke(0)
    rect(MARGINS, MARGINS, DISPLAYWIDTH, DISPLAYHEIGHT)


    frameDuration(frame_Duration)
    for line in range(lines):
        # Create a new empty text object and set its properties
        lineTxt = newLine()
        for char in range(charsInLine):
            currentlinewidth = int(textSize(lineTxt)[0])
            # TEST:
            # fill(None)
            # stroke(50,0,0)
            # rect(0, 0 ,SCREENWIDTH - currentlinewidth, SCREENHEIGHT)
            # rect(0, 0 ,currentlinewidth, SCREENHEIGHT)

            variableWdth, variableHght = getVariableSettings(line, char, currentlinewidth)
            lineTxt.append(
                displayTextList[line][char],
                # create dict to replace original fontVariations - so instead of fontVariations(x)
                fontVariations = dict(wdth = variableWdth, hght = variableHght)
                )
            print(currentlinewidth)
        text(lineTxt, (xOffset, yOffset))
        # yOffset -= FONTSIZE # TODO


# Save the animation as a gif
path = "letterGrid.gif"
saveImage(path)  # or ~/Desktop/...

endDrawing() # needed for using as python module
