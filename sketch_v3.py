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
# DISPLAYTEXT = "hello"
# DISPLAYTEXT = "מטבחים מערכות מבטחים"
DISPLAYTEXT = "מטבחים מטבחים מבטחים"
EXCLUDECOLUMN = 4 # todo can we do this in the preprocessing?
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
# print("init", minLetterWidth,maxLetterWidth,minLetterHeight,maxLetterHeight)

FRAME_DURATION = TOTALDURATION / TOTALFRAMES

# INITIALIZE VARIABLES
xOffset = SCREENWIDTH - MARGINS # since we align right for hebrew
yOffset = MARGINS
accumulatedHeight = [yOffset] * CHARS_IN_LINE # acc height per column
widthcontainer = [0] * CHARS_IN_LINE # tracking the 1st row widths to use

# MORNING:
# create shape "grid" that sums to 1.
# each iter re-distribute
# then draw letters.


# idea!
# rand 6 num.
# sum them - s1
# width - w
# scale all by w/s1
# sum of all will be w

# the probability is the diff
# in the current logic the numbers are monotonic decreasing, the expectance is decreasing
# in this idea, the expected is k/2



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
def getVariableSettings(row, col): #, accumulatedWidth):
    global accumulatedHeight
    global widthcontainer
    accumulatedWidth = sum(widthcontainer)
    # print("acc", accumulatedWidth)
    variableWdth = minLetterWidth # init local
    variableHght = minLetterHeight # init local
    if (row==0):
        # 1st row in charge of width definition for column
        if (col==EXCLUDECOLUMN):
            # currentwidth = minLetterWidth
            variableWdth = minLetterWidth
            # variableWdth = FONT_MIN_WIDTH
        else :
            # variableWdth regards letters before
            # currentmaxwidth = max((DISPLAYWIDTH - accumulatedWidth)*0.5, minLetterWidth*(CHARS_IN_LINE-col)) # min* how many letters left
            currentmaxwidth = max(DISPLAYWIDTH - accumulatedWidth - (minLetterWidth*(CHARS_IN_LINE-col))*0.5, 0)
            currentwidth = randint(minLetterWidth, int(currentmaxwidth))
            variableWdth = currentwidth # RECT
            print (accumulatedWidth, currentwidth, (DISPLAYWIDTH - accumulatedWidth)*0.5, minLetterWidth*(CHARS_IN_LINE-col), CHARS_IN_LINE-col)

            # variableWdth = mapWidthToFont(currentwidth)
            # streach last letter width
            if (col==CHARS_IN_LINE-1):
                # TODO, max with minLetterWidth
                currentwidth = max(DISPLAYWIDTH - accumulatedWidth, minLetterWidth)
                variableWdth = currentwidth # RECT
                # variableWdth = mapWidthToFont(currentwidth)
                # print (accumulatedWidth, currentwidth, variableWdth, accumulatedWidth+currentwidth)
        # hold on to 1st row width values
        widthcontainer[col] = variableWdth
    else:
        # other rows use the same width
        variableWdth = widthcontainer[col]

    # all rows need height settings
    currentmaxheight = max((DISPLAYHEIGHT - accumulatedHeight[col]), minLetterHeight*(LINES-row))
    currentheight = randint(minLetterHeight, int(currentmaxheight))
    variableHght = currentheight # RECT
    # variableHght = mapHeightToFont(currentheight)
    # print(currentmaxheight, currentheight, variableHght, accumulatedHeight[col])


    # streach last row height
    if (row==LINES-1):
        # TODO, max with minLetterHeight
        currentheight = max(DISPLAYHEIGHT - accumulatedHeight[col],minLetterHeight)
        variableHght = currentheight # RECT
        # variableHght = mapHeightToFont(currentheight)

    # print(variableWdth, variableHght)
    return variableWdth, variableHght


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
            print(xOffset, yOffset, w, h)

            # xOffset -= w
            accumulatedHeight[char] += h
# print(accumulatedHeight)


# Save the animation as a gif
path = "letterGrid.gif"
saveImage(path)  # or ~/Desktop/...

endDrawing() # needed for using as python module
