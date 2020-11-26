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

colunmwidths = [0]*CHARS_IN_LINE
# rowheights = []*LINES
shade = 0

def rowDistribution():
# rand 6 num
# sum them - s1
# width - w
# scale all by w/s1
# sum of all will be w
# why?
# the probability is the diff
# in the original logic the numbers are monotonic decreasing, the expectance is also decreasing
# in this idea, the expected is k/2
    s = 0
    for i in range(CHARS_IN_LINE):
        r = randint(FONT_MIN_WIDTH, FONT_MAX_WIDTH)
        # r = randint(minLetterWidth, maxLetterWidth)
        s += r
        colunmwidths[i] = r
    w = DISPLAYWIDTH
    scale = w/s
    for i in range(CHARS_IN_LINE):
        # temp = colunmwidths[i]*scale
        colunmwidths[i] *= scale
        colunmwidths[i] = int(colunmwidths[i])
    # fix last
    remainder = w - sum(colunmwidths)
    colunmwidths[0] += remainder
    return

# MAIN FUNCTION
newDrawing() # needed for using as python module
for frame in range(TOTALFRAMES):
    # Draw the background rectangle
    newPage(SCREENWIDTH, SCREENHEIGHT)
    fill(BACKGROUND_R/255, BACKGROUND_G/255, BACKGROUND_B/255)
    rect(0,0,SCREENWIDTH, SCREENHEIGHT)
    frameDuration(FRAME_DURATION)

    # # test min and max size of letters
    # fill(0)
    # rect(0,0, minLetterWidth,  minLetterHeight)
    # rect(100,0, maxLetterWidth, maxLetterHeight)

    for l in range(LINES):
        rowDistribution()
        xOffset = SCREENWIDTH - MARGINS

        stroke(0)
        fill(None)
        # print(colunmwidths)
        for i in range(CHARS_IN_LINE):
            width = colunmwidths[i]
            height = 100
            xOffset -= width
            rect(xOffset, yOffset, width, height)
        yOffset +=100


    # for line in range(LINES):
    #     xOffset = SCREENWIDTH - MARGINS # init for each line
    #     for char in range(CHARS_IN_LINE):
    #         w, h = getVariableSettings(line, char)
    #         fill(None)
    #         stroke(0)
    #         rect(xOffset, yOffset, w, h)


# Save the animation as a gif
path = "letterGrid.gif"
saveImage(path)  # or ~/Desktop/...

endDrawing() # needed for using as python module
