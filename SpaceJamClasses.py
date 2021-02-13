from ColObjBase import *
import mathPaths as mp
from direct.task import Task
from pandac.PandaModules import WindowProperties
props = WindowProperties()
props.setTitle('SpaceJam')

class Universe(InvCollideObj):

    def __init__(self, modelPath, parentNode, nodeName, texPath, posVec, scaleVec):
        base.win.requestProperties(props)
        mySound = base.loader.loadSfx("bgm.mp3")
        mySound.play()
        super(Universe, self).__init__(modelPath, parentNode, nodeName, 0, 0, 0, 0.9)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)
        
class Planet(SphereCollideObj):
    def __init__(self, modelPath, parentNode, nodeName, texPath, posVec, scaleVec):
        super(Planet, self).__init__(modelPath, parentNode, nodeName, 0, 0, 0, 1)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

class spaceStation(TubeCollideObj):
    def __init__(self, modelPath, parentNode, nodeName, posVec, scaleVec):
        super(spaceStation, self).__init__(modelPath, parentNode, nodeName, 0, 0, 10, 0, 0, -10, 3)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

class Drone(SphereCollideObj):
    droneCnt = 0
    def __init__(self, modelPath, parentNode, nodeName, posVec, scaleVec):
        super(Drone, self).__init__(modelPath, parentNode, nodeName, 0, 0, 0, 1)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

class Missile(SphereCollideObj):
    missileCnt = 0
    Intervals =  {}
    FireModels = {}
    cNodes = {}
    CSP = {}

    def __init__(self, modelPath, parentNode, nodeName, posVec, scaleVec = 1.0):
        super(Missile, self).__init__(modelPath, parentNode, nodeName, 0, 0 ,0 , 1.3)
        self.modelNode.setPos(posVec)

        Missile.FireModels[nodeName] = self.modelNode
        Missile.cNodes[nodeName] = self.cNode
        Missile.CSP[nodeName] = self.cNode.node().getSolid(0)

        print("burn # =" + str(Missile.missileCnt))

class SpaceShip(SphereCollideObj):
    def __init__(self, modelPath, parentNode, nodeName, posVec, scaleVec, traverser, missileHandler):
        super(SpaceShip, self).__init__(modelPath, parentNode, nodeName, 0, 0, 0, 1)
        
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
     
        self.traverser = traverser
        self.mHandler = missileHandler

        self.setKeyBindings()

        self.missileTank = 1
        taskMgr.add(self.checkIntervals, 'checkMissileBay', 34)

    def setKeyBindings(self):
        self.accept("space", self.thrust, [1])
        self.accept("space-up", self.thrust, [0])
        self.accept("arrow_left", self.leftTurn, [1])
        self.accept("arrow_left-up", self.leftTurn, [0])
        self.accept("arrow_right", self.rightTurn, [1])
        self.accept("arrow_right-up", self.rightTurn, [0])
        self.accept("arrow_up", self.pitchBack, [1])
        self.accept("arrow_up-up", self.pitchBack, [0])
        self.accept("arrow_down", self.pitchForward, [1])
        self.accept("arrow_down-up", self.pitchForward, [0])
        self.accept("a", self.rollLeft, [1])
        self.accept("a-up", self.rollLeft, [0])
        self.accept("d", self.rollRight, [1])
        self.accept("d-up", self.rollRight, [0])
        self.accept("f", self.fire)

######Thrust Control#####
    def thrust(self, keyDown):
        if keyDown:
            taskMgr.add(self.applyThrust, "forward-thrust")
        else:
            taskMgr.remove("forward-thrust")
            self.acceptOnce("space", self.thrust, [1])
            self.acceptOnce("space-up", self.thrust, [0])

    def applyThrust(self, keyDown):
        rate = 3
        trajectory = render.getRelativeVector(self.modelNode, Vec3.forward())
        trajectory.normalize()
        self.modelNode.setFluidPos(self.modelNode.getPos() + trajectory * rate)
        return Task.cont
 #####Yaw Controls#####
    def leftTurn(self, keyDown):
        if keyDown:
            taskMgr.add(self.applyLeftTurn, "left-turn")
        else:
            taskMgr.remove("left-turn")
            self.acceptOnce("arrow_left", self.leftTurn, [1])
            self.acceptOnce("arrow_left-up", self.leftTurn, [0])

    def applyLeftTurn(self, keyDown):
        rate = 0.5
        self.modelNode.setH(self.modelNode.getH() + rate)
        return Task.cont

    def rightTurn(self, keyDown):
        if keyDown:
            taskMgr.add(self.applyRightTurn, "right-turn")
        else:
            taskMgr.remove("right-turn")
            self.acceptOnce("arrow_right", self.rightTurn, [1])
            self.acceptOnce("arrow_right-up", self.rightTurn, [0])

    def applyRightTurn(self,keyDown):
        rate = -0.5
        self.modelNode.setH(self.modelNode.getH() + rate)
        return Task.cont
#####Pitch Control#####
    def pitchBack(self, keyDown):
        if keyDown:
            taskMgr.add(self.applyPitchBack, "pitch-back")
        else:
            taskMgr.remove("pitch-back")
            self.acceptOnce("arrow_up", self.pitchBack, [1])
            self.acceptOnce("arrow_up-up", self.pitchBack, [0])

    def applyPitchBack(self,keyDown):
        rate = 0.5
        self.modelNode.setP(self.modelNode.getP() + rate)
        return Task.cont
    
    def pitchForward(self, keyDown):
        if keyDown:
            taskMgr.add(self.applyPitchForward, "pitch-forward")
        else:
            taskMgr.remove("pitch-forward")
            self.acceptOnce("arrow_down", self.pitchForward, [1])
            self.acceptOnce("arrow_down-up", self.pitchForward, [0])

    def applyPitchForward(self,keyDown):
        rate = -0.5
        self.modelNode.setP(self.modelNode.getP() + rate)
        return Task.cont
#####Roll Control#####
    def rollLeft(self, keyDown):
        if keyDown:
            taskMgr.add(self.applyRollLeft, "roll-left")
        else:
            taskMgr.remove("roll-left")
            self.acceptOnce("a", self.rollLeft, [1])
            self.acceptOnce("a-up", self.rollLeft, [0])

    def applyRollLeft(self,keyDown):
        rate = -0.5
        self.modelNode.setR(self.modelNode.getR() + rate)
        return Task.cont
    
    def rollRight(self, keyDown):
        if keyDown:
            taskMgr.add(self.applyRollRight, "roll-right")
        else:
            taskMgr.remove("roll-right")
            self.acceptOnce("d", self.rollRight, [1])
            self.acceptOnce("d-up", self.rollRight, [0])

    def applyRollRight(self,keyDown):
        rate = 0.5
        self.modelNode.setR(self.modelNode.getR() + rate)
        return Task.cont
#####Missile Controls#####
    def fire(self):
        if self.missileTank:
            travRate = 2000
            aim = render.getRelativeVector(self.modelNode, Vec3.forward())
            aim.normalize()
            print(str(aim))
            fireSolution = aim * travRate
            inFront = aim * 20
            travVec = fireSolution + self.modelNode.getPos()
            Missile.missileCnt += 1
            self.missileTank -= 1
            tag = 'missile-' + str(Missile.missileCnt)
            mPosVec = self.modelNode.getPos() + inFront
            missile = Missile("./Ships/Phaser/phaser", render, tag , mPosVec)


            self.traverser.addCollider(missile.cNode, self.mHandler)

            Missile.Intervals[tag] = missile.modelNode.posInterval(2, travVec, \
                startPos=mPosVec, fluid=1)
            Missile.Intervals[tag].start()
        else:
            if not taskMgr.hasTaskNamed('reload'):
                print('Initalize reload ...')
                taskMgr.doMethodLater(0, self.reload, 'reload')
                return Task.cont
    def reload(self, task): 
        if self.missileTank == 1:
            return Task.done
        else:
            if task.time < 2.0:
                return Task.cont
            
            self.missileTank += 1
            if self.missileTank > 1:
                self.missileTank = 1

            print('Reload Complete')
            return Task.again
    def checkIntervals(self, task):
        for i in Missile.Intervals:
            if not Missile.Intervals[i].isPlaying():
                Missile.cNodes[i].detachNode()
                Missile.FireModels[i].detachNode()
                del Missile.Intervals[i]
                del Missile.FireModels[i]
                del Missile.cNodes[i]
                del Missile.CSP[i]
                print(i + "Has reached the end of it's trajectory.")
                break
        return Task.cont

class Orbiter(SphereCollideObj):
    numObiters = 0

    def __init__(self, modelPath, parentNode, modelName, numSeams, scaleVec, texturePath, \
        attachedObject, orbitRadius, orbitType):

        super(Orbiter, self).__init__(modelPath, parentNode, modelName, 0, 0, 0, 3.2)

        self.numSeams = numSeams
        self.orbitType = orbitType
        self.modelNode.setScale(scaleVec)
        tex = loader.loadTexture(texturePath)
        self.modelNode.setTexture(tex, 1)
        self.orbitObject = attachedObject
        self.orbitRadius = orbitRadius
        Orbiter.numObiters += 1

        self.taskFlag = "Travler-" + str(Orbiter.numObiters)
        taskMgr.add(self.orbit, self.taskFlag)

    def orbit(self, task):

        if self.orbitType == 'MLB':
            positionVec = mp.BaseballSeams(task.time, self.numSeams, 0.2)
        elif self.orbitType == 'XY':
            positrionVec = mp.CircleXY(task.time,self.numSeams)
        elif self.orbitType == 'YZ':
            positrionVec = mp.CircleXY(task.time,self.numSeams)
        elif self.orbitType == 'XZ':
            positrionVec = mp.CircleXY(task.time,self.numSeams)
        else:
            print("not now")
            sys.exit

        self.modelNode.setPos(positionVec * self.orbitRadius + self.orbitObject.modelNode.getPos())

        return Task.cont




