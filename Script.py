#Drop Jump Simulator
#make sure run steamvr.py before run this script
#some data: walk time: 1s, dropping time: 0.9s 
import viz
import vizact
import vizfx
import timeit
import time
import vizconnect
import steamvr
from vizconnect.util import view_collision


viz.setMultiSample(4)
viz.fov(60)
vizconnect.go('vizconnect_config_htcvive.py')  #run htc vive config script
viz.go()
viz.phys.enable()


#set lab environment and light
viz.clearcolor(0.7,0.7,0.8)
viz.MainView.setPosition([9,3,15])
viz.MainView.setEuler(180, 0, 0)
lab = viz.addChild('lab.osgb')
lab.setPosition([0,0,0])
vizfx.addDirectionalLight(euler=(0,45,0))

env = viz.add(viz.ENVIRONMENT_MAP,'sky.jpg')
dome = viz.add('skydome.dlc')
dome.texture(env)

#set up collider and avatar
ground = lab.getChild('ground')  # get ground 
ground.collidePlane(bounce = 0, friction = 0.01)   # Make collideable plane 

#get table for experiment
table = viz.addChild( 'table.wrl' )
table.setPosition([9,0.5,15])
table.collideBox( node='Leg1', bounce = 0, friction = 1 )
table.collideBox( node='Leg2', bounce = 0, friction = 1 )
table.collideBox( node='Leg3', bounce = 0, friction = 1 )
table.collideBox( node='Leg4', bounce = 0, friction = 1 )
table.collideBox( node='Top', bounce = 0, friction = 0 )
viz.phys.enable()

#set up UI

import vizinfo
info = vizinfo.InfoPanel('R: ready, Space: start, A: reset',title='setting') 
title = viz.addText3D('Drop  Jump  Simulator',pos=[12.4,3.4,18], euler=[90,0,0])
title.scale([0.58,0.58,0.58])
title.font('Comic Sans MS')
startmenu = viz.addText3D('Please keep surrounding clear.\n\n  Make sure you are standing\n near the center of the platform.\n\n Press R when get ready!',pos=[12.4,2.5,18], euler=[90,0,0])
startmenu.scale([0.4,0.4,0.4])
startmenu.font('Comic Sans MS')
text3D = viz.addText(' Ready',pos=[13.8,1.4,16], euler=[90,0,0])
text3D.font('Calibri')

#set up the Avatar
experimenter = viz.addAvatar('vcc_female.cfg')
head = experimenter.getBone('Bip01 Head')
cameraPoint = experimenter.getBone('Bip01 Spine1')
neck = experimenter.getBone('Bip01 Neck')
global calfR, calfL
calfR = experimenter.getBone('Bip01 R Calf')
calfL = experimenter.getBone('Bip01 L Calf')
footL = experimenter.getBone('Bip01 L Foot')
neck.lock()
head.lock()
experimenter.setPosition([9.3,1.5,15])
experimenter.setEuler([90,0,0])
experimenter.collideBox(bounce = 0)
 
#set up VR headset
headTracker = vizconnect.getTracker('head_tracker').getNode3d()
cameralink = viz.link(head, headTracker, mask = viz.LINK_POS | viz.LINK_SCALE, offset = [0.2,0,0]) #offset avoid collision 

def ready():
   computer = lab.getChild('ID419')
   computer.setScale([0.005,0.005,0.005])
   title.setScale([0.005,0.005,0.005])
   startmenu.setScale([0.005,0.005,0.005])
def start():
   print('start!')
   print(time.time())
   text3D.message(' Start!')
   drop = vizact.walkTo([10,1.2,15])
   start = experimenter.addAction(drop)
   neck.lock()
   head.lock()
   
def reset():
   text3D.message(' Ready!')
   table.setPosition([9,0.5,15])
   experimenter.setPosition([9.3,1.5,15])
   experimenter.setEuler([90,0,0])


#helper function for simulating
def onground():
   if(experimenter.getPosition()[1] < 0.2):
      return 1
   else:
      return 0
      
def ontable():
   if(experimenter.getPosition()[1] > 1.15):
      return 1
   else:
      return 0

#simulate landing
def landing():
   if(ontable() == 0 and onground() == 0): #when dropping
      if(calfR.getEuler()[2] > -9):
         calfR.lock()
         calfL.lock()
         text3D.message('Dropping')
         print('drop!')
         print(time.time())
      if(calfR.getEuler()[2]> -30):
         calfR.setEuler(0, 0, calfR.getEuler()[2]-10)
         calfL.setEuler(0, 0, calfL.getEuler()[2]-10)
   if(ontable() == 0 and onground() == 1):    #after landing
      if(calfR.getEuler()[2] < -28):
         text3D.message('Finished')
         print('hit the ground!')
         print(time.time())
      if(calfR.getEuler()[2] < -10):
         calfR.setEuler(0, 0, calfR.getEuler()[2]+10)
         calfL.setEuler(0, 0, calfL.getEuler()[2]+10)


#press space to start the simulation
vizact.ontimer(0, landing)
vizact.onkeydown(' ', start)
vizact.onkeydown('a', reset)
vizact.onkeydown('r', ready)

