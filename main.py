from direct.showbase.ShowBaseGlobal import globalClock
from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import loadPrcFile
from direct.actor.Actor import Actor
from panda3d.core import Vec4, Vec3
from direct.showbase.ShowBase import ShowBase
from panda3d.core import CollisionTraverser
from panda3d.core import CollisionHandlerPusher
from panda3d.core import CollisionTraverser, CollisionHandlerPusher, CollisionSphere, CollisionTube, CollisionNode


loadPrcFile ( 'conf.prc' )


class MyGame ( ShowBase ) :
    def updateKeyMap(self, controlName, controlState):
        self.keyMap[controlName] = controlState
        self.updateTask = taskMgr.add(self.update, "update")
        print(controlName, "set to", controlState)



# class Mapmanager():
#     def __init__(self):
#         self.model = 'block'
#         self.texture = 'block.png'
#         self.colors = [
#             ( 0.2,0.2,0.35,1 ),
#             ( 0.2, 0.5, 0.2, 1 ),
#             ( 0.7, 0.2, 0.2, 1 ),
#             ( 0.5, 0.3, 0.0, 1 )
#         ]
#         self.startNew()
#     def startNew(self):
#         self.land = render.attacNewNode('Land')
#     def getColor(self, z):
#         if z < len(self.colors):
#                 return self.colors[z]
#         else:
#             return self.colors[len(self.colors)-1]
#     def addBlock(self,position):
#         self.block = loader.loadModel(self.model)
#         self.block.setTexture(loader.loadTexture(self.texture))
#         self.block.setPos(position)
#         self.color = self.getColor(int(position[2]))
#         self.block.setColor(self.color)
#         self.block.reparentTo(self.land)
#     def clear(self):
#         self.land.removeNode()
#         self.startNew()
#
#     def loadLand(self, filename) :
#         with open ( 'OLEG.txt' ) as file :
#             y=0
#             for line in file:
#                 x=0
#                 line=line.split ( '' )
#                 for z in line :
#                     for z0 in range ( int ( z ) + 1 ):
#                         block=self.adBlock ( (x, y, z0) )
#                     x+=1
#                     y+=1
    def update(self, task):
        dt = globalClock.getDt()
        if self.keyMap["up"]:
            self.tempActor.setPos(self.tempActor.getPos() + Vec3( 0 * dt, 0.001, 0))
        if self.keyMap["down"]:
            self.tempActor.setPos(self.tempActor.getPos() + Vec3( 0 * dt, -0.001, 0))
        if self.keyMap["left"]:
            self.tempActor.setPos(self.tempActor.getPos() + Vec3(-1.0 * dt, 0, 0))
        if self.keyMap["right"]:
            self.tempActor.setPos(self.tempActor.getPos() + Vec3(1.0 * dt, 0, 0))
        if self.keyMap["shoot"]:
            print("Zap!")

        return task.cont

    def __init__(self) :
        ShowBase.__init__(self)
        # self.land = Mapmanager()
        # self.land.loadLand('OLEG.txt')
        # base.camLens.detFov(90)
        # super ( ).__init__ ()
        self.accept("w", self.updateKeyMap, ["up", True])
        self.accept("w-up", self.updateKeyMap, ["up", False])
        self.accept("s", self.updateKeyMap, ["down", True])
        self.accept("s-up", self.updateKeyMap, ["down", False])
        self.accept("a", self.updateKeyMap, ["left", True])
        self.accept("a-up", self.updateKeyMap, ["left", False])
        self.accept("d", self.updateKeyMap, ["right", True])
        self.accept("d-up", self.updateKeyMap, ["right", False])
        self.tempActor=Actor ( "panda", {"walk" : "panda-walk"} )
        self.tempActor.setPos ( 0, 190, 0 )
        self.tempActor.setScale ( 0.1, 0.1, 0 )
        self.tempActor.getChild ( 0 ).setH ( 180 )
        self.environment=loader.loadModel ( "Environment/environment" )
        self.environment.reparentTo ( render )
        self.environment.setPos ( 0, 190, 0 )
        #self.tempActor.setP ( 90 )
        self.pusher = CollisionHandlerPusher()
        self.cTrav = CollisionTraverser()

        self.pusher.setHorizontal(True)

        colliderNode = CollisionNode("player")
        colliderNode.addSolid(CollisionSphere(0, 0, 0, 0.3))
        collider = self.tempActor.attachNewNode(colliderNode)

        base.pusher.addCollider(collider, self.tempActor)
        base.cTrav.addCollider(collider, self.pusher)

        wallSolid=CollisionTube ( 0, 930, 0, 930, 930, 0, 8.2 )
        wallNode=CollisionNode ( "wall" )
        wallNode.addSolid ( wallSolid )
        wall=render.attachNewNode ( wallNode )
        wall.setY ( 8.0 )

        wallSolid=CollisionTube ( 0, 94, 0, 930, 94, 0, 8.2 )
        wallNode=CollisionNode ( "wall" )
        wallNode.addSolid ( wallSolid )
        wall=render.attachNewNode ( wallNode )
        wall.setY ( -8.0 )

        wallSolid=CollisionTube ( 94, 0, 0, 94, 930, 0, 8.2 )
        wallNode=CollisionNode ( "wall" )
        wallNode.addSolid ( wallSolid )
        wall=render.attachNewNode ( wallNode )
        wall.setX ( 8.0 )

        wallSolid=CollisionTube ( 930, 0, 0, 930, 930, 0, 8.2 )
        wallNode=CollisionNode ( "wall" )
        wallNode.addSolid ( wallSolid )
        wall=render.attachNewNode ( wallNode )
        wall.setX ( -8.0 )
        self.updateTask = taskMgr.add(self.update, "update")
        self.tempActor.loop ( "walk" )

        self.cam.setPos ( 0, 185, 30 )
        self.cam.setP ( -80 )

        self.keyMap={
            "up" : False,
            "down" : False,
            "left" : False,
            "right" : False,
            "shoot" : False
        }

        self.tempActor.reparentTo ( render )


game=MyGame ( )
game.run ( )
