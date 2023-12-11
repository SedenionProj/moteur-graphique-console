import keyboard
import moteur_graphique as mg
from lib_math import *
import time

carre = [Triangle(vec3(0,0,0),
                  vec3(1,0,0),
                  vec3(0,1,0)),
         Triangle(vec3(1,0,0),
                  vec3(1,1,0),
                  vec3(0,1,0))]

cam = mg.Camera(vec3(0,0,-3),0.0,0.0)

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
    

last = 0

while True:
    current = time.time()
    dt = (current-last)*100
    last=current

    mg.clear(' ')
    
    inputs()

    mg.putMesh(carre,cam)

    mg.draw()