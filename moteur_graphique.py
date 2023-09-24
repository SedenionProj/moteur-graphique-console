import os
from lib_math import *

width,height = os.get_terminal_size()
height -= 1
pixelBuffer = ['*']*(width*height)

def draw():
    print(''.join(pixelBuffer),end='')

def clear(char):
    for i in range(width*height):
        pixelBuffer[i] = char

def putPixel(v, char):
    px = round(v.x)
    py = round(v.y)
    if 0 <=px<width and 0<=py<height:
        pixelBuffer[py * width + px] = char

putPixel(vec2(10,10), " ")
draw()

input()
