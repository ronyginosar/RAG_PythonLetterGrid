# -*- coding: utf-8 -*-
# to run script, cmd-i : https://atom.io/packages/script
from drawBot import * # needed for using as python module

# TODO's:
# animate transitions
# NTH - make input text
# NTH - interactive with mouse

# DISTRIBUTION LOGIC
# rand #cols num
# sum them - s1
# width - w
# scale all by w/s1
# sum of all will be w
# why? the probability is the diff
# in the original logic the numbers are monotonic decreasing, the expectance is also decreasing
# in this idea, the expected is k/2

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
SPACEING = 10

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
FRAME_DURATION = TOTALDURATION / TOTALFRAMES

# HELPER FUNCTIONS
colunmwidths = []
accumulatedHeight = [0]*CHARS_IN_LINE ## TODO in rowheights
rowheights = []
shade = 0

def colDistribution():
    global colunmwidths
    widths = randomDistribution(FONT_MIN_WIDTH, FONT_MAX_WIDTH,
                                 CHARS_IN_LINE, DISPLAYWIDTH)
    colunmwidths = widths
    return

def rowDistribution():
    heights = randomDistribution(FONT_MIN_HEIGHT, FONT_MAX_HEIGHT,
                                 LINES, DISPLAYHEIGHT)
    rowheights.append(heights)
    return

def randomDistribution(minValue, maxValue, rangeValue, displaysizeparam):
    randomList = [0]*rangeValue
    s = 0
    # random numbers
    for i in range(rangeValue):
        r = randint(minValue, maxValue)
        # if excluded column:
        if (rangeValue==CHARS_IN_LINE and i==EXCLUDECOLUMN):
            r = minValue
        s += r
        randomList[i] = r
    # scale
    d = displaysizeparam
    scale = d/s
    for i in range(rangeValue):
        randomList[i] *= scale
        randomList[i] = int(randomList[i])
    # fix last
    remainder = d - sum(randomList)
    randomList[0] += remainder
    return randomList

def drawLetter(char, xLocation, yLocation, boxWidth, boxHeight):
    # get lettershape as bezier
    B = BezierPath()
    B.text(char, (0, 0), fontSize=FONTSIZE, font=FONT, align="right")
    # get lettershape bounding box
    left, bottom, right, top = B.bounds()
    # calculate lettershape width & height
    letterWidth  = right - left
    letterHeight = top - bottom
    # calculate scaling factors
    factorHeight = (boxHeight - SPACEING) / letterHeight
    factorWidth  = (boxWidth - SPACEING)  / letterWidth
    ## draw box
    ## fill(1, 1, 0)
    ## rect(xLocation, yLocation, boxWidth, boxHeight)
    # apply scaling factors
    B.scale(factorWidth, factorHeight)
    # shift shape to origin position
    B.translate(xLocation, yLocation)
    # draw scaled lettershape
    stroke(None)
    fill(1, 1, 1)
    drawPath(B)

# MAIN FUNCTION
newDrawing() # needed for using as python module
for frame in range(TOTALFRAMES):
    yOffset = MARGINS
    accumulatedHeight = [0]*CHARS_IN_LINE

    # Draw the background rectangle
    newPage(SCREENWIDTH, SCREENHEIGHT)
    fill(BACKGROUND_R/255, BACKGROUND_G/255, BACKGROUND_B/255)
    rect(0,0,SCREENWIDTH, SCREENHEIGHT)
    frameDuration(FRAME_DURATION)

    # # test min and max size of letters
    # fill(0)
    # rect(0,0, minLetterWidth,  minLetterHeight)
    # rect(100,0, maxLetterWidth, maxLetterHeight)
    stroke(0)
    fill(None)

    # run once the cols, *chars the rows
    colDistribution()
    for c in range(CHARS_IN_LINE):
        rowDistribution()

    for l in range(LINES): # rows
        xOffset = SCREENWIDTH - MARGINS
        # xOffset = SCREENWIDTH - MARGINS
        for c in range(CHARS_IN_LINE): # cols
            boxHeight = rowheights[c][l]
            boxWidth = colunmwidths[c]
            char = DISPLAYTEXTLIST[l][c]
            drawLetter(char,
                       xOffset, yOffset+accumulatedHeight[c],
                       boxWidth, boxHeight)
            # rect(xOffset, yOffset+accumulatedHeight[c], width, height)
            xOffset -= boxWidth
            accumulatedHeight[c] += boxHeight

# Save the animation as a gif
path = "letterGrid.gif"
saveImage(path)  # or ~/Desktop/...

endDrawing() # needed for using as python module
