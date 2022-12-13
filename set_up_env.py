#first try to setup an environment with robot and floor, robot arm moves a bit

import pybullet as pyb 
import time
import pybullet_data

physicsClient = pyb.connect(pyb.GUI) # ruft den graphischen Client auf
pyb.setAdditionalSearchPath(pybullet_data.getDataPath()) # notwendig für Boden ?
planeID = pyb.loadURDF("plane.urdf") # Boden wird generiert 
#wir generieren den roboter, usefixedbase hindert den roboter daran umzukippen
robot = pyb.loadURDF("/home/parallels/Desktop/RobotAndWorldGenerator/jeffrey.urdf")
pyb.setGravity(0,0,-9.81)
#optional eigentlich ist das sowieso auf 0 gesetzt, sodass eine simulation erst erfolgt wenn
# durch code angegeben 
pyb.setRealTimeSimulation(0)

#unklar was es macht
#pyb.setJointMotorControlArray(robot,range(7),p.POSITION_CONTROL,targetPositions=[1.5] * 7)

print("Start Simulation? Y/N")
b = input("Enter answer")

#forschleife die die schritte simuliert, nun bewegt sich auch der Roboter
#for _ in range (300): 
 #   pyb.stepSimulation()
  #  time.sleep(1./10.)



# Dieser code muss am ende kommen, da das Script sonst automatisch terminiert
print("Do you want to exit? Y/N")
a = input("Enter answer: ")
print("you chose", a)

#pyb.ste