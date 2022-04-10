from panda3d.core import loadPrcFile
from direct.actor.Actor import Actor
from panda3d.core import AmbientLight
from panda3d.core import Vec4

loadPrcFile ( 'conf.prc' )
from direct.showbase.ShowBase import ShowBase


class MyGame ( ShowBase ) :
    def __init__(self) :
        super ( ).__init__ ( )
        self.environment = loader.loadModel ( "models\misc\camera" )
        self.environment.setPos ( 0, 25, 0 )
        self.environment.setP ( 90 )
        self.environment.reparentTo ( render )
        self.tempActor=Actor ( "panda", {"walk" : "panda-walk"} )
        self.tempActor.setPos ( 0, 25, 0 )
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
