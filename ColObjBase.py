from direct.showbase.ShowBase import ShowBase
from panda3d.core import *

class PlaceObj(ShowBase):
    def __init__(self, modelPath, parentNode, nodeName):
        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setName(nodeName)
        
class CollideableObj(PlaceObj):
    def __init__(self, modelPath, parentNode, nodeName):
        super(CollideableObj, self).__init__(modelPath, parentNode, nodeName)
        self.cNode = self.modelNode.attachNewNode(CollisionNode(nodeName + "_Cnode"))

class TubeCollideObj(CollideableObj):
    def __init__(self, modelPath, parentNode, nodeName, ax, ay, az, bx, by, bz, r):  
        super(TubeCollideObj, self).__init__(modelPath, parentNode, nodeName)      
        self.cNode.node().addSolid(CollisionTube(ax, ay, az, bx, by, bz, r))

class InvCollideObj(CollideableObj):
    def __init__(self, modelPath, parentNode, nodeName, x, y, z, r):
        super(InvCollideObj, self).__init__(modelPath, parentNode, nodeName)
        self.cNode.node().addSolid(CollisionInvSphere(x, y, z, r))

class SphereCollideObj(CollideableObj):
    def __init__(self, modelPath, parentNode, nodeName, x, y, z, r):
        super(SphereCollideObj, self).__init__(modelPath, parentNode, nodeName)
        self.cNode.node().addSolid(CollisionSphere(x, y, z, r))
