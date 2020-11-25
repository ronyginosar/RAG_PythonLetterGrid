# -*- coding: utf-8 -*-
# to run script, cmd-i : https://atom.io/packages/script
from drawBot import * # needed for using as python module

# TODO's:
# fill line width, mapping problem


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
LINES = len(DISPLAYTEXTLIST) # The number of lines
CHARS_IN_LINE = len(DISPLAYTEXTLIST[0])
# PRE PROCESSING - FONT
font(FONT)
FONT_MIN_WIDTH = listFontVariations()['wdth']['minValue']
FONT_MAX_WIDTH = listFontVariations()['wdth']['maxValue']
FONT_MIN_HEIGHT = listFontVariations()['hght']['minValue']
FONT_MAX_HEIGHT = listFontVariations()['hght']['maxValue']
# PRE PROCESSING - DISPLAY
LINEHEIGHT = FONTSIZE*0.7
DISPLAYWIDTH, DISPLAYHEIGHT = 500, LINEHEIGHT*LINES
# DISPLAYWIDTH, DISPLAYHEIGHT = 500, 125
SCREENWIDTH = DISPLAYWIDTH + MARGINS*2
SCREENHEIGHT = DISPLAYHEIGHT + MARGINS*2
minLetterWidth = int(DISPLAYWIDTH * 0.1)
maxLetterWidth = int(DISPLAYWIDTH * 0.5)
minLetterHeight = int(DISPLAYHEIGHT* 0.1)
maxLetterHeight = int(DISPLAYHEIGHT*0.8)

FRAME_DURATION = TOTALDURATION / TOTALFRAMES

# not sure:
# for i,line in enumerate(DISPLAYTEXTLIST):
#     DISPLAYTEXTLIST[i] = list(line)
# for line in DISPLAYTEXTLIST:
#     line.reverse()

# print(DISPLAYTEXTLIST)

# INITIALIZE VARIABLES
xOffset = SCREENWIDTH - MARGINS # since we align right for hebrew
yOffset = MARGINS
accumulatedHeight = [0] * CHARS_IN_LINE # acc height per column
widthcontainer = [0] * CHARS_IN_LINE # tracking the 1st row widths to use

# HELPER FUNCTIONS
def newLine():
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
# print(minLetterWidth, maxLetterWidth, minLetterHeight, maxLetterHeight) # TEST
def getVariableSettings(row, col, accumulatedWidth):
    global accumulatedHeight
    global widthcontainer
    variableWdth = minLetterWidth
    variableHght = minLetterHeight

    if (row==0):
        # 1st row in charge of width definition for column
        if (col==EXCLUDECOLUMN):
            currentwidth = minLetterWidth
            variableWdth = FONT_MIN_WIDTH
        else :
            # variableWdth regards letters before
            currentmaxwidth = max((DISPLAYWIDTH - accumulatedWidth)*0.5, minLetterWidth)
            currentwidth = randint(minLetterWidth, int(currentmaxwidth))
            variableWdth = mapWidthToFont(currentwidth)
            if (col==CHARS_IN_LINE-1):
                currentwidth = DISPLAYWIDTH - accumulatedWidth
                variableWdth = mapWidthToFont(currentwidth)
                # print (accumulatedWidth, currentwidth, variableWdth, accumulatedWidth+currentwidth)
        # hold on to 1st row width values
        widthcontainer[col] = variableWdth
    else:
        # other rows use the same width
        variableWdth = widthcontainer[col]

    # all rows need height settings
    currentmaxheight = max((DISPLAYHEIGHT - accumulatedHeight[col])*0.7, minLetterHeight)
    # currentmaxheight = max((DISPLAYHEIGHT)*0.5, minLetterHeight)
    currentheight = randint(minLetterHeight, int(currentmaxheight))
    variableHght = mapHeightToFont(currentheight)
    accumulatedHeight[col] += currentheight # TODO find right value
    print(currentmaxheight, currentheight, variableHght, accumulatedHeight[col])

    # if (row==LINES-1):
    #     currentheight = DISPLAYHEIGHT - accumulatedHeight[col]
    #     variableHght = mapHeightToFont(currentheight)


    # print ("current range", int(currentmaxwidth), minLetterWidth,
    #         "currentwidth", currentwidth,
    #         "variableWdth", variableWdth)
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
        # Create a new empty text object and set its properties
        lineTxt = newLine()
        for char in range(CHARS_IN_LINE):
            currentlinewidth = int(textSize(lineTxt)[0])

            # TEST:
            # fill(None)
            # stroke(50,0,0)
            # rect(MARGINS, yOffset ,xOffset - MARGINS - currentlinewidth, lineTxt.fontLineHeight())

            variableWdth, variableHght = getVariableSettings(line, char, currentlinewidth)
            lineTxt.append(
                DISPLAYTEXTLIST[line][char],
                # create dict to replace original fontVariations - so instead of fontVariations(x)
                fontVariations = dict(wdth = variableWdth, hght = variableHght)
                )
            # if (char == CHARS_IN_LINE-1):
            #     print("wanted", DISPLAYWIDTH - currentlinewidth, "got", int(textSize(lineTxt)[0])-currentlinewidth) #TEST
            # print(currentlinewidth)Y
        text(lineTxt, (xOffset, yOffset))#, align="right")

        # TODO according to accumulatedHeight
        yOffset += lineTxt.fontLineHeight() # TODO


# Save the animation as a gif
path = "letterGrid.gif"
saveImage(path)  # or ~/Desktop/...

endDrawing() # needed for using as python module
