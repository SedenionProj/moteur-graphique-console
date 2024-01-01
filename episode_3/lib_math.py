from math import cos, sin, sqrt
import moteur_graphique as mg

class vec2:
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y

    def __mul__(self,c):
        return vec2(self.x*c,self.y*c)
    
    def __truediv__(self,c):
        return vec2(self.x/c,self.y/c)
    
    def __add__(self,v):
        return vec2(self.x+v.x,self.y+v.y)
    
    def __sub__(self,v):
        return vec2(self.x-v.x,self.y-v.y)
    
    __radd__ = __add__
    __rmul__ = __mul__

    def toScreen(self):
        v = vec2(((29/13)*mg.height/mg.width*self.x+1)*mg.width  /2,
                 (-self.y+1)*mg.height /2)
        return v
    
class vec3:
    def __init__(self,x,y,z) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __mul__(self,c):
        return vec3(self.x*c,self.y*c,self.z*c)

    def __truediv__(self,c):
        return vec3(self.x/c,self.y/c,self.z/c)
    
    def __add__(self,v):
        return vec3(self.x+v.x,self.y+v.y,self.z+v.z)
    
    def __sub__(self,v):
        return vec3(self.x-v.x,self.y-v.y,self.z-v.z)
    
    __radd__ = __add__
    __rmul__ = __mul__

    def projection(self,focalLenth) -> vec2:
        return focalLenth*vec2(self.x, self.y)/self.z
    
    def rotationX(self,pitch):
        y1=cos(pitch)*self.y-sin(pitch)*self.z
        z1=sin(pitch)*self.y+cos(pitch)*self.z
        return vec3(self.x,y1,z1)

    def rotationY(self,yaw):
        x1= cos(yaw)*self.x+sin(yaw)*self.z
        z1=-sin(yaw)*self.x+cos(yaw)*self.z
        return vec3(x1,self.y,z1)
    
    def normalize(self):
        norm = sqrt(self.x*self.x+self.y*self.y+self.z*self.z)
        return vec3(self.x/norm, self.y/norm, self.z/norm)
        
    def length(self):
        return sqrt(self.x*self.x+self.y*self.y+self.z*self.z)
    
class Triangle2D:    
    def __init__(self,v1,v2,v3) -> None:
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3

    def toScreen(self):
        return Triangle2D(self.v1.toScreen(),self.v2.toScreen(),self.v3.toScreen())

class Triangle3D:    
    def __init__(self,v1,v2,v3) -> None:
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3

    def projection(self,focalLenth):
        return Triangle2D(self.v1.projection(focalLenth),self.v2.projection(focalLenth),self.v3.projection(focalLenth))

    def translate(self, v:vec3):
        return Triangle3D(self.v1 + v,self.v2 + v,self.v3 + v)

    def rotationX(self,pitch):
        return Triangle3D(self.v1.rotationX(pitch),self.v2.rotationX(pitch),self.v3.rotationX(pitch))
    
    def rotationY(self,yaw):
        return Triangle3D(self.v1.rotationY(yaw),self.v2.rotationY(yaw),self.v3.rotationY(yaw))

def LinePlaneCollision(planeNormal, planePoint, v1, v2):
    u=v2-v1
    dotp = dot(planeNormal,u)
    if abs(dotp) < 1e-5:
        return (0,0,0) # pas de collision
    w = (v1-planePoint)
    si = -dot(planeNormal,w)/dotp
    u = si*u
    return (v1+u)

def dot(v1:vec3, v2: vec3):
    return v1.x*v2.x + v1.y*v2.y + v1.z*v2.z

def crossProd(v1:vec3, v2: vec3):
    return vec3(v1.y*v2.z-v1.z*v2.y,
                v1.z*v2.x-v1.x*v2.z, 
                v1.x*v2.y-v1.y*v2.x)