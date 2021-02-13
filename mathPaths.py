import math, random
from panda3d.core import *

def CircleXZ(time, numSeams, radius=1):
    theta = time / numSeams * 2 * math.pi
    return Vec3(math.sin(theta), 0 , math.cos(theta)) * radius

def CircleXY(time, numSeams, radius=1):
    theta = time / numSeams * 2 * math.pi
    return Vec3(math.sin(theta), 0 , math.cos(theta)) * radius

def CircleYZ(time, numSeams, radius=1):
    theta = time / numSeams * 2 * math.pi
    return Vec3(math.sin(theta), 0 , math.cos(theta)) * radius

def Cloud(radius=1):
    unitVec = Vec3(2.0 * random.random() -1, 2.0 * random.random() -1.0,\
         2.0 * random.random() -1.0 )
    unitVec.normalize()
    return unitVec * radius

def BaseballSeams(time, numSeams,fudgeFactor=0.1,radius=1):
    time = float(time)
    numSeams =float(numSeams)
    alpha = (time + numSeams/4)/numSeams * 2 * math.pi
    theta = (time/numSeams) * 2 * math.pi

    x = (radius * (1 - fudgeFactor) * math.cos(theta) * \
            math.sin(2 * theta)) + fudgeFactor * radius * \
                math.sin(theta)

    y = (radius * (1 - fudgeFactor) * math.cos(alpha) * \
            math.sin(2 * alpha)) + fudgeFactor * radius * \
                math.sin(alpha)

    z = radius * math.cos(theta * 2)

    return Vec3(x, y, z)