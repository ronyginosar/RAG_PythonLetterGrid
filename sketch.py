# -*- coding: utf-8 -*-
# to run script, cmd-i : https://atom.io/packages/script
from drawBot import * # needed for using as python module

# TODO's:
# fill line width, mapping problem
# animate transitions
# NTH - make input text
# NTH - interactive with mouse


# CONSTANTS:
# DISPLAYTEXT = "מטבחים"
DISPLAYTEXT = "מטבחים מטבחים מבטחים"
EXCLUDECOLUMN = 4
FONTSIZE = 150
FONT = 'assets/RAG-Marom-GX.ttf'
TOTALFRAMES = 1
TOTALDURATION = 1 # in seconds
BACKGROUND_R, BACKGROUND_G, BACKGROUND_B = 238, 127, 171
MARGINS = 10

# PRE PROCESSING - TEXT
DISPLAYTEXTLIST = DISPLAYTEXT.split(' ')
LINES = len(DISPLAYTEXTLIST) # rows
CHARS_IN_LINE = len(DISPLAYTEXTLIST[0]) # cols
# PRE PROCESSING - FONT
font(FONT)
FONT_MIN_WIDTH = listFontVariations()['wdth']['minValue']
FONT_MAX_WIDTH = listFontVariations()['wdth']['maxValue']
FONT_MIN_HEIGHT = listFontVariations()['hght']['minValue']
FONT_MAX_HEIGHT = listFontVariations()['hght']['maxValue']
# PRE PROCESSING - DISPLAY
LINEHEIGHT = FONTSIZE*0.7
DISPLAYWIDTH, DISPLAYHEIGHT = 500, LINEHEIGHT*LINES
SCREENWIDTH = DISPLAYWIDTH + MARGINS*2
SCREENHEIGHT = DISPLAYHEIGHT + MARGINS*2
minLetterWidth = int(DISPLAYWIDTH * 0.1)
maxLetterWidth = int(DISPLAYWIDTH * 0.4)
minLetterHeight = int(DISPLAYHEIGHT* 0.1)
maxLetterHeight = int(DISPLAYHEIGHT*0.8)

FRAME_DURATION = TOTALDURATION / TOTALFRAMES

# INITIALIZE VARIABLES
xOffset = SCREENWIDTH - MARGINS # since we align right for hebrew
yOffset = MARGINS
accumulatedHeight = [yOffset] * CHARS_IN_LINE # acc height per column
widthcontainer = [0] * CHARS_IN_LINE # tracking the 1st row widths to use

# HELPER FUNCTIONS
def newTxt():
    t = FormattedString()
    t.fill(255,255,255)
    t.font(FONT)
    t.fontSize(FONTSIZE)
    t.openTypeFeatures(ss01=True)
    t.align('right')
    t.lineHeight(LINEHEIGHT)
    t.tracking(0)
    return t

def mapWidthToFont(currentwidth):
    return int(mapValue(currentwidth,
                    minLetterWidth, maxLetterWidth,
                    FONT_MIN_WIDTH, FONT_MAX_WIDTH))

def mapHeightToFont(currentheight):
    return int(mapValue(currentheight,
                    minLetterHeight, maxLetterHeight,
                    FONT_MIN_HEIGHT, FONT_MAX_HEIGHT))

def mapValue(value, oldmin, oldmax, newmin, newmax):
    return (value - oldmin) / (oldmax - oldmin) * (newmax - newmin) + newmin

# LOGIC CORE FUNCTION
def getVariableSettings(row, col):
    global accumulatedHeight
    global widthcontainer
    accumulatedWidth = sum(widthcontainer) # LOCAL ????
    variableWdth = minLetterWidth # init local
    variableHght = minLetterHeight # init local
    if (row==0):
        # 1st row in charge of width definition for column
        if (col==EXCLUDECOLUMN):
            variableWdth = minLetterWidth
        elif(col==CHARS_IN_LINE-1): # streach last letter width
            variableWdth = max(DISPLAYWIDTH - accumulatedWidth, minLetterWidth)
            print ("width",accumulatedWidth, variableWdth, (DISPLAYWIDTH - accumulatedWidth))
        else :
            currentminwidth = minLetterWidth*(CHARS_IN_LINE-col-1)
            currentmaxwidth = max((DISPLAYWIDTH - accumulatedWidth - currentminwidth), currentminwidth) # min* how many letters left
            variableWdth = randint(minLetterWidth, int(currentmaxwidth))
            print ("width",accumulatedWidth, currentmaxwidth, variableWdth, (DISPLAYWIDTH - accumulatedWidth- currentminwidth), currentminwidth)

        # hold on to 1st row width values
        widthcontainer[col] = variableWdth
    else:
        # other rows use the same width
        variableWdth = widthcontainer[col]

    # all rows need height settings
    currentmaxheight = max((DISPLAYHEIGHT - accumulatedHeight[col]), minLetterHeight*(LINES-row))
    variableHght = randint(minLetterHeight, int(currentmaxheight))
    # print("height", currentmaxheight, variableHght, accumulatedHeight[col])

    # streach last row height
    if (row==LINES-1):
        # TODO, max with minLetterHeight
        currentheight = max(DISPLAYHEIGHT - accumulatedHeight[col],minLetterHeight)
        variableHght = currentheight # RECT
        # variableHght = mapHeightToFont(currentheight)

    # print(variableWdth, variableHght)
    return int(variableWdth), int(variableHght)


# MAIN FUNCTION
newDrawing() # needed for using as python module
for frame in range(TOTALFRAMES):
    # Draw the background rectangle
    newPage(SCREENWIDTH, SCREENHEIGHT)
    fill(BACKGROUND_R/255, BACKGROUND_G/255, BACKGROUND_B/255)
    rect(0,0,SCREENWIDTH, SCREENHEIGHT)
    # fill(None) # TEST
    # stroke(0)  # TEST
    # rect(MARGINS, MARGINS, DISPLAYWIDTH, DISPLAYHEIGHT)  # TEST
    frameDuration(FRAME_DURATION)
    for line in range(LINES):
        xOffset = SCREENWIDTH - MARGINS # init for each line
        for char in range(CHARS_IN_LINE):
            w, h = getVariableSettings(line, char)
            # yOffset = 10
            yOffset = accumulatedHeight[char]
            fill(None)
            stroke(0)
            xOffset -= w
            # TODO max x and max y
            rect(xOffset, yOffset, w, h)
            # print("box", xOffset, yOffset, w, h)

            # xOffset -= w
            accumulatedHeight[char] += h
# print(accumulatedHeight)


# Save the animation as a gif
path = "letterGrid.gif"
saveImage(path)  # or ~/Desktop/...

endDrawing() # needed for using as python module
