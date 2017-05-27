#########
# firstTry.py
# This program is part of the online PS-Drone-API-tutorial on www.playsheep.de/drone.
# It shows how to do basic movements with a Parrot AR.Drone 2.0 using the PS-Drone-API.
# Dependencies: a POSIX OS, PS-Drone-API 2.0 beta or higher.
# (w) J. Philipp de Graaff, www.playsheep.de, 2014
##########
# LICENCE:
#   Artistic License 2.0 as seen on http://opensource.org/licenses/artistic-license-2.0 (retrieved December 2014)
#   Visit www.playsheep.de/drone or see the PS-Drone-API-documentation for an abstract from the Artistic License 2.0.
###########
import time
import ps_drone                # Imports the PS-Drone-API
import sys

drone = ps_drone.Drone()       # Initializes the PS-Drone-API
drone.startup()                # Connects to the drone and starts subprocesses
drone.reset()

#Sets drones LEDs to green when red
while (drone.getBattery()[0]==-1): time.sleep(0.1) #Reset completed ?
print "battery:" + str(drone.getBattery()[0]) + "% " + str(drone.getBattery()[1])
if drone.getBattery()[1]=="empty": sys.exit()

drone.useDemoMode(True)
drone.getNDpackage(["demo"])
time.sleep(0.5)

drone.trim()
drone.getSelfRotation(5)


#15 basic datasets per second (default)
#Packets, which shall be decoded
#Give it some time to fully awake
drone.takeoff()

time.sleep(7.5)                # Gives the drone time to start
drone.mtrim()

# start = time.time()
# for i in range(20):
#     drone.moveUp(1)
#     time.sleep(0.3)
#     drone.moveDown(1)
#     time.sleep(0.3)
# stop = time.time()

start = time.time()
drone.moveUp(1)
time.sleep(0.3)
stop = time.time()

dt = stop - start

print "time = " + str(dt)
#drone.doggyHop()
#drone.doggyNod()


#time.sleep()                # Gives the drone time to start
#drone.moveForward()            # Drone flies forward...
#time.sleep(2)                  # ... for two seconds
#drone.stop()                   # Drone stops...
#time.sleep(2)                  # ... needs, like a car, time to stop
#
#drone.moveBackward(0.25)       # Drone flies backward with a quarter speed...
#time.sleep(1.5)                # ... for one and a half seconds
#drone.stop()                   # Drone stops
#time.sleep(2)
#
#drone.setSpeed(1.0)            # Sets default moving speed to 1.0 (=100%)
#print drone.setSpeed()         # Shows the default moving speed
#
#drone.turnLeft()               # Drone moves full speed to the left...
#time.sleep(2)                  # ... for two seconds
#drone.stop()                   # Drone stops
#time.sleep(2)

drone.land()                   # Drone lands

