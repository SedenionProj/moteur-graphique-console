import os
from lib_math import *

width,height = os.get_terminal_size()
height -= 1
pixelBuffer = [' ']*(width*height)

class Camera:
    def __init__(self,position,pitch,yaw,focalLenth=1) -> None:
        self.position = position
        self.pitch = pitch
        self.yaw = yaw
        self.focalLenth = focalLenth

    def getLookAtDirection():
        pass

    def getForwardDirection(self):
        return vec3(-sin(self.yaw),0,cos(self.yaw))
    
    def getRightDirection(self):
        return vec3( cos(self.yaw),0,sin(self.yaw))


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

def putTriangle(tri,char):
    def eq(p, a, b):
        return (a.x-p.x)*(b.y-p.y)-(a.y-p.y)*(b.x-p.x)

    xmin = round(min(tri.v1.x, tri.v2.x, tri.v3.x))
    xmax = round(max(tri.v1.x, tri.v2.x, tri.v3.x))+1
    ymin = round(min(tri.v1.y, tri.v2.y, tri.v3.y))
    ymax = round(max(tri.v1.y, tri.v2.y, tri.v3.y))+1
    for y in range(ymin,ymax):
        if 0<=y<height:
            for x in range(xmin,xmax):
                if 0<=x<width:
                    pos = vec2(x,y)
                    w1 = eq(pos, tri.v3, tri.v1)
                    w2 = eq(pos, tri.v1, tri.v2)
                    w3 = eq(pos, tri.v2, tri.v3)
                    if (w1 >= 0 and w2 >= 0 and w3 >= 0) or (-w1 >= 0 and -w2 >= 0 and -w3 >= 0):
                        putPixel(pos,char)

def putMesh(mesh:list[Triangle3D],cam:Camera):
    for triangle in mesh:
        putTriangle(triangle.translate(-1*cam.position).rotationY(cam.yaw).rotationX(cam.pitch).projection(cam.focalLenth).toScreen(),'@')

