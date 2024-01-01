import keyboard
import moteur_graphique as mg
from lib_math import *
import time

cam = mg.Camera(vec3(0,0,0),0.0,-2.0)
light = mg.LightSource(vec3(0,20,0))

cube = mg.loadObj("cube.obj")

def inputs():
    if keyboard.is_pressed("down arrow"):
        if cam.pitch>-1.57:
            cam.pitch-=0.01*dt
    if keyboard.is_pressed("up arrow"):
        if cam.pitch<1.57:
            cam.pitch+=0.01*dt
    if keyboard.is_pressed("left arrow"):
        cam.yaw+=0.01*dt
    if keyboard.is_pressed("right arrow"):
        cam.yaw-=0.01*dt
    if keyboard.is_pressed("z"):
        cam.position+=cam.getForwardDirection()*0.01*dt
    if keyboard.is_pressed("s"):
        cam.position+=-1*cam.getForwardDirection()*0.01*dt
    if keyboard.is_pressed("d"):
        cam.position+=cam.getRightDirection()*0.01*dt
    if keyboard.is_pressed("q"):
        cam.position+=-1*cam.getRightDirection()*0.01*dt
    if keyboard.is_pressed("space"):
        cam.position.y+=0.01*dt
    if keyboard.is_pressed("shift"):
        cam.position.y-=0.01*dt
    
last = time.time()

while True:
    current = time.time()
    dt = (current-last)*500
    last=current

    inputs()

    mg.clear(' ')
    
    mg.putMesh(cube,cam,light)

    mg.draw()