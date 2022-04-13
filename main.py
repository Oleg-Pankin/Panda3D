from direct.showbase.ShowBaseGlobal import globalClock
from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import loadPrcFile
from direct.actor.Actor import Actor
from panda3d.core import AmbientLight
from panda3d.core import Vec4, Vec3

loadPrcFile ( 'conf.prc' )
from direct.showbase.ShowBase import ShowBase


class MyGame ( ShowBase ) :
    def updateKeyMap(self, controlName, controlState):
        self.keyMap[controlName] = controlState
        self.updateTask = taskMgr.add(self.update, "update")
        print(controlName, "set to", controlState)

    def update(self, task):
        dt = globalClock.getDt()
        if self.keyMap["up"]:
            self.tempActor.setPos(self.tempActor.getPos() + Vec3( 0 * dt, 0, 0.001))
        if self.keyMap["down"]:
            self.tempActor.setPos(self.tempActor.getPos() + Vec3( 0 * dt, 0, -0.001))
        if self.keyMap["left"]:
            self.tempActor.setPos(self.tempActor.getPos() + Vec3(-5.0 * dt, 0, 0))
        if self.keyMap["right"]:
            self.tempActor.setPos(self.tempActor.getPos() + Vec3(5.0 * dt, 0, 0))
        if self.keyMap["shoot"]:
            print("Zap!")

        return task.cont

    def __init__(self) :
        super ( ).__init__ ()
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
        self.tempActor.getChild ( 0 ).setH ( 180 )
        self.tempActor.setP ( 90 )
        self.tempActor.loop ( "walk" )

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
