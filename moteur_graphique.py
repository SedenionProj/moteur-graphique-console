import os

width,height = os.get_terminal_size()
height -= 1
pixelBuffer = ['*']*(width*height)

def draw():
    print(''.join(pixelBuffer),end='')

def clear(char):
    for i in range(width*height):
        pixelBuffer[i] = char

def putPixel(x, y, char):
    px = round(x)
    py = round(y)
    if 0 <=px<width and 0<=y<height:
        pixelBuffer[py * width + px] = char

putPixel(10, 10, " ")
draw()

input()