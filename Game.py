import sys

from direct.interval.IntervalGlobal import *
from direct.particles.ParticleEffect import ParticleEffect
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage

from ColObjBase import *
import SpaceJamClasses as sjc
import mathPaths as mp

class SpaceJam(ShowBase):
    showInstructions = True

    def __init__(self):
        ShowBase.__init__(self)

        self.accept('escape', self.quit)
        self.setScene()
        self.setCamera()
        self.setInstruction()

        self.setParticels()
        self.cntExplode = 0
        self.xplodeIntervals = {}

        self.pusher.addCollider(self.khanShip.cNode, self.khanShip.modelNode)
        self.traverser.addCollider(self.khanShip.cNode, self.pusher)

    def setScene(self):
        self.traverser = CollisionTraverser()
        base.cTrav = self.traverser
        self.traverser.traverse(render)
        self.pusher = CollisionHandlerPusher()

        self.handler = CollisionHandlerEvent()
        self.handler.addInPattern("into")
        self.accept("into", self.handleInto)
                
        self.universe = sjc.Universe('./Universe/Universe.x', render, 'Big Bang', './Universe/starfield-in-blue.jpg', Vec3(0, 0, 0), 10000)

        self.sunPlanet = sjc.Planet('./Planets/protoPlanet.x', render, 'Sol', './Planets/sun.jpg', Vec3(-2000,9000,0), 800)
        self.redPlanet = sjc.Planet('./Planets/protoPlanet.x', render, 'Mars', './Planets/redPlanet.jpg', Vec3(-2500,8000,-2000), 300)
        self.bluePlanet = sjc.Planet('./Planets/protoPlanet.x', render,'BigBlue', './Planets/BigBlue.jpg', Vec3(500,1500,-200), 150)
        self.earthPlanet = sjc.Planet('./Planets/protoPlanet.x', render,'Earth', './Planets/earthLike.jpg', Vec3(0,3000,0), 100)
        self.earthMoon = sjc.Planet('./Planets/protoPlanet.x', render,'Moon', './Planets/moonLike.jpg', Vec3(200,2750,-25), 25)

        self.drone = sjc.spaceStation('./Ships/DroneDefender/DroneDefender', render, 'Drone Defender', Vec3(50,-50,50), 2 )
        self.morlockShip = sjc.spaceStation('./Ships/MorlockShip/theMorlocks', render, 'Morlock Fighter', Vec3(20,-20,20), 2 )
        self.tridentShip = sjc.spaceStation('./Ships/Trident/trident', render, 'Trident Fighter', Vec3(0,-100,0), 10 )
        self.spaceStation = sjc.spaceStation('./Ships/SpaceStation1B/spaceStation', render, 'SpaceStation1B', Vec3(-200,500,-10), 2 )

        self.khanShip = sjc.SpaceShip('./Ships/KhanShip/Khan', render, 'Khan Fighter', Vec3(0,0,0), 0.25, self.traverser, self.handler)


        self.sentinal = sjc.Orbiter("./Ships/Dumbledore/Dumbledore", render, "Drone-Travler", 125, 6.0, \
            "./Ships/DroneDefender/octotoad1_auv.png", self.spaceStation, 230, "MLB")
######Defense Drones######
        radian = 0
        fullCycle = 60
        for j in range(fullCycle):
            sjc.Drone.droneCnt += 1
            nickName = "drone-" + str(sjc.Drone.droneCnt)

            unitVec = mp.CircleXY(j, fullCycle)
            
            unitVec.normalize()
            position = unitVec * 300 + self.spaceStation.modelNode.getPos()
            self.drone = sjc.Drone("./Ships/Dumbledore/Dumbledore", render, nickName, position, 4)

    def setCamera(self):
        self.disableMouse()
        self.camera.reparentTo(self.khanShip.modelNode)
        #Third party
        self.camera.setFluidPos(0,-200,50)
        self.camera.setHpr(0,-8,0)
    
    def setInstruction(self):
        self.hud = OnscreenImage(image = "./Hud/_hud/krunkerRedDot.png", pos=(0, 0, 0), scale=0.10)
        self.hud.setTransparency(TransparencyAttrib.MAlpha)

#####Camera/ Instructions#####
    def addInstruction(self, pos, msg):
        return OnscreenText(text=msg, style=1, fg=(1,1,1,1), pos=(0.5,pos), align=TextNode.ABoxedLeft, scale=0)

    def setParticels(self):
        base.enableParticles()
        self.splodeEffect = ParticleEffect()
        self.splodeEffect.setScale(40)
        self.explodeNode = render.attachNewNode('xpl-efx')

    def handleInto(self, entry):
        print("XXXXXX")
        print(str(entry))
        fromNode = entry.getFromNodePath().getName()
        intoNode = entry.getIntoNodePath().getName()
        intoPos =  Vec3(entry.getSurfacePoint(render))
        print(str(intoNode) +" : "+ str(intoPos))
        
        tempVar = fromNode.split("_")
        shooter = tempVar[0]
        tempVar = intoNode.split("-")
        target = tempVar[0]
        tempVar = intoNode.split("_")
        victim = tempVar[0]

        print("missile Hit")
        print(shooter)
        print(fromNode + " into " + intoNode)
        print(victim)

        if target == "drone":
            sjc.Missile.Intervals[shooter].finish()
            self.droneDestroy(victim, intoPos)
        else:
            sjc.Missile.Intervals[shooter].finish()
    
    def droneDestroy(self, hitID, hitPos):
        nodeID = self.render.find(hitID)
        nodeID.detachNode()
        print(hitID + " destroyed")

        self.explode(hitID, hitPos)

        self.explodeNode.setPos(hitPos)


    def explode(self, hitID, impactPt):
        start = Vec3(0,0,0) + Vec3(impactPt)

        self.cntExplode += 1
        tag = 'particles-' + str(self.cntExplode)
        print('\n' + str(self.explodeNode.getPos()) + "explosion location")
        self.xplodeIntervals[tag] = LerpFunc(self.explodeLight, fromData=0, \
            toData=1, duration=2.0, extraArgs=[impactPt])
        self.xplodeIntervals[tag].start()
    
    def explodeLight(self, t, explPosition):
        if t == 1.0 and self.splodeEffect:
            self.splodeEffect.disable()
        elif t == 0:
            self.splodeEffect.start(self.explodeNode)
    
    def quit():
        sys.exit()

loadPrcFileData('','win-size 720, 500')

app = SpaceJam()
app.run()
