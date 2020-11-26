from drawBot import *
# get lettershape as bezier
B = BezierPath()
B.text('x', (0, 0), fontSize=100, font='Georgia', align="right")

# get lettershape bounding box
left, bottom, right, top = B.bounds()
print(left, bottom, right, top)

# calculate lettershape width & height
letterWidth  = right - left
letterHeight = top - bottom

# define box width & height
boxWidth, boxHeight = 800, 400

# calculate scaling factors
factorHeight = boxHeight / letterHeight
factorWidth  = boxWidth  / letterWidth

# draw box
fill(1, 1, 0)
rect(10, 10, boxWidth, boxHeight)

# apply scaling factors
B.scale(factorWidth, factorHeight)

# shift shape to origin position
B.translate(boxWidth+10,10)

# draw scaled lettershape
fill(1, 0, 0)
drawPath(B)

path = "viewbox.gif"
saveImage(path)  # or ~/Desktop/...
