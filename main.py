from direct.showbase.ShowBaseGlobal import globalClock
from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import loadPrcFile
from direct.actor.Actor import Actor
from panda3d.core import Vec4, Vec3
from direct.showbase.ShowBase import ShowBase
from panda3d.core import CollisionTraverser
from panda3d.core import CollisionHandlerPusher
from panda3d.core import CollisionTraverser, CollisionHandlerPusher, CollisionSphere, CollisionTube, CollisionNode
from GameObject import *


loadPrcFile ( 'conf.prc' )


class MyGame ( ShowBase ) :
    def updateKeyMap(self, controlName, controlState):
        self.keyMap[controlName] = controlState
        self.updateTask = taskMgr.add(self.update, "update")
        print(controlName, "set to", controlState)

    def update(self, task):
        dt = globalClock.getDt()

        self.player.update(self.keyMap, dt)

        self.tempEnemy.update(self.player, dt)


        return task.cont

    def __init__(self) :
        ShowBase.__init__(self)
        self.accept("w", self.updateKeyMap, ["up", True])
        self.accept("w-up", self.updateKeyMap, ["up", False])
        self.accept("s", self.updateKeyMap, ["down", True])
        self.accept("s-up", self.updateKeyMap, ["down", False])
        self.accept("a", self.updateKeyMap, ["left", True])
        self.accept("a-up", self.updateKeyMap, ["left", False])
        self.accept("d", self.updateKeyMap, ["right", True])
        self.accept("d-up", self.updateKeyMap, ["right", False])
        self.tempActor = Player
        self.environment=loader.loadModel ( "Environment/environment" )
        self.environment.reparentTo ( render )
        self.environment.setPos ( 0, 190, 0 )
        self.pusher = CollisionHandlerPusher()
        self.cTrav = CollisionTraverser()

        self.pusher.setHorizontal(True)

        colliderNode = CollisionNode("player")
        colliderNode.addSolid(CollisionSphere(0, 0, 0, 0.3))


        self.pusher.add_in_pattern("%fn-into-%in")
        self.accept("trapEnemy-into-wall", self.stopTrap)
        self.accept("trapEnemy-into-trapEnemy", self.stopTrap)
        self.accept("trapEnemy-into-player", self.trapHitsSomething)
        self.accept("trapEnemy-into-walkingEnemy", self.trapHitsSomething)

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


        self.cam.setPos ( 0, 185, 30 )
        self.cam.setP ( -80 )

        self.keyMap={
            "up" : False,
            "down" : False,
            "left" : False,
            "right" : False,
            "shoot" : False
        }

        def stopTrap(self, entry):
            collider = entry.getFromNodePath()
            if collider.hasPythonTag("owner"):
                trap = collider.getPythonTag("owner")
                trap.moveDirection = 0
                trap.ignorePlayer = False

        dt = globalClock.getDt()
        self.player = Player()
        class TrapEnemy(Enemy):
            def __init__(self, pos):
                Enemy.__init__(self, pos,
                               "trap",
                               {
                                   "stand": "trap-stand",
                                   "walk": "trap-walk",
                               },
                               100.0,
                               10.0,
                               "trapEnemy")

        self.tempTrap = TrapEnemy(Vec3(-2, 7, 0))
        self.tempTrap.update(self.player, dt)

        def stopTrap(self, entry):
            collider = entry.getFromNodePath()
            if collider.hasPythonTag("owner"):
                trap = collider.getPythonTag("owner")
                trap.moveDirection = 0
                trap.ignorePlayer = False

        def trapHitsSomething(self, entry):
            collider = entry.getFromNodePath()
            if collider.hasPythonTag("owner"):
                trap = collider.getPythonTag("owner")

                # We don't want stationary traps to do damage,             # so ignore the collision if the "moveDirection" is 0             if trap.moveDirection == 0:
                return

            collider = entry.getIntoNodePath()
            if collider.hasPythonTag("owner"):
                obj = collider.getPythonTag("owner")
                if isinstance(obj, Player):
                    if not trap.ignorePlayer:
                        obj.alterHealth(-1)
                        trap.ignorePlayer = True
                else:
                    obj.alterHealth(-10)

        self.player = Player()

        self.tempEnemy = WalkingEnemy(Vec3(0, 185, 0))



game=MyGame ( )
game.run ( )