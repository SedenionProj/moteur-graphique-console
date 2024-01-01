from math import floor
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

    def getLookAtDirection(self):
        return vec3(-sin(self.yaw)*cos(self.pitch),sin(self.pitch),cos(self.yaw)*cos(self.pitch))

    def getForwardDirection(self):
        return vec3(-sin(self.yaw),0,cos(self.yaw))
    
    def getRightDirection(self):
        return vec3( cos(self.yaw),0,sin(self.yaw))

class LightSource:
    def __init__(self,position) -> None:
        self.position = position

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



def clip(triangle,camPos,planeNormal):
    def inZ(planeNormal, planePoint,tri):
        out = [] 
        in_ = []
        vert1 = dot(planePoint-tri.v1,planeNormal)
        vert2 = dot(planePoint-tri.v2,planeNormal)
        vert3 = dot(planePoint-tri.v3,planeNormal)

        out.append(tri.v1) if vert1 > 0 else in_.append(tri.v1)
        out.append(tri.v2) if vert2 > 0 else in_.append(tri.v2)
        out.append(tri.v3) if vert3 > 0 else in_.append(tri.v3)

        return out,in_, vert1*vert3>0

    zNear = camPos+0.1*planeNormal
    out, in_, isInverted = inZ(planeNormal,zNear,triangle)
    
    if len(out) == 0:
        return [triangle]
    elif len(out) == 3:
        return []
    elif len(out) == 1:
        collision0 = LinePlaneCollision(planeNormal,zNear,out[0],in_[0])
        collision1 = LinePlaneCollision(planeNormal,zNear,out[0],in_[1])
        if isInverted:
            return [
                Triangle3D(collision1,in_[1],collision0),
                Triangle3D(collision0,in_[1],in_[0])
                ]
        else:
            return [
                Triangle3D(collision0,in_[0],collision1),
                Triangle3D(collision1,in_[0],in_[1])
                ]
    elif len(out) == 2:
        if isInverted: 
            return [
                Triangle3D(LinePlaneCollision(planeNormal,zNear,out[0],in_[0]),
                           in_[0],
                           LinePlaneCollision(planeNormal,zNear,out[1],in_[0])) 
                ]
        else:
            
            return [
                Triangle3D(LinePlaneCollision(planeNormal,zNear,out[0],in_[0]),
                           LinePlaneCollision(planeNormal,zNear,out[1],in_[0]),
                           in_[0])
                ]
            
def loadObj(filePath):
    with open(filePath, "r") as  file:
        lines = [line.rstrip('\n').split(' ') for line in file.readlines() if line.rstrip('\n')]
        
        vertices = []
        faces  = []
        for line in lines:
            if line[0] == 'v':
                vertex = list(map(float,line[1:]))
                vertices.append(vec3(vertex[0], vertex[1], vertex[2]))
            if line[0] == 'f':
                faces.append(list(map(int,line[1:])))
                        
        triangles = []
        for f in faces:
            if len(f) == 3:
                triangles.append(Triangle3D(vertices[f[0]-1], vertices[f[1]-1], vertices[f[2]-1]))
            if len(f) == 4:
                triangles.append(Triangle3D(vertices[f[0]-1], vertices[f[1]-1], vertices[f[2]-1]))
                triangles.append(Triangle3D(vertices[f[2]-1], vertices[f[3]-1], vertices[f[0]-1]))
        return triangles
            
lightGradient = ".,;la#@"

def diffuseLight(light:LightSource, normal, vertex) -> str:
    lightDir = light.position-vertex
    intensity = dot(lightDir.normalize(),normal.normalize())
    return lightGradient[round(intensity*(len(lightGradient)-1))] if intensity>=0 else "."



def putMesh(mesh:list[Triangle3D],cam:Camera, light:LightSource):
    def distanceTriangle(triangle):
        position = (1/3)*(triangle.v1+triangle.v2+triangle.v3)-cam.position
        return position.length()
    
    mesh.sort(key=distanceTriangle, reverse=True )

    lookAt = cam.getLookAtDirection()

    for triangle in mesh:
        clippedTriangleList = clip(triangle,cam.position,lookAt)

        for clippedTriangle in clippedTriangleList:
            line1 = clippedTriangle.v2-clippedTriangle.v1
            line2 = clippedTriangle.v3-clippedTriangle.v1
            surfaceNorm = crossProd(line1,line2)

            if dot(surfaceNorm,clippedTriangle.v1-cam.position) < 0:
                lightStr = diffuseLight(light, surfaceNorm, clippedTriangle.v1)
                putTriangle(clippedTriangle
                            .translate(-1*cam.position)
                            .rotationY(cam.yaw)
                            .rotationX(cam.pitch)
                            .projection(cam.focalLenth)
                            .toScreen(),lightStr)

