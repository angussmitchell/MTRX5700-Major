## MTRX5700
# Xue Yin Zhang
#
# Get some navigation while starting up and calibrating and doing a move

## clean startup sequence
import time, sys
import ps_drone         # Import PS-Drone-API
import pickle           # python library to save and restore variables
import boots

## clean start up
drone = ps_drone.Drone()                                                      # Start using drone
drone.startup()                                                               # Connects to drone and starts subprocesses
drone.reset()                                                                 # Sets drone's status to good (LEDs turn green when red)
while (drone.getBattery()[0] == -1):  time.sleep(0.1)                         # Wait until the drone has done its reset

## make sure drone has enough battery
if drone.getBattery()[0] < 30:
    print "battery too low"
    drone.land()        # land for safety (even though it's not in the air atm)
    quit()              # end program

## print out battery status
print "Battery: "+str(drone.getBattery()[0])+"%  "+str(drone.getBattery()[1]) # Gives a battery-status

## set mode of data packages
drone.useDemoMode(False)
drone.getNDpackage(["demo", "time", "altitude", "magneto", "vision_detect"])         # Packets, which shall be decoded
time.sleep(1.0)

## set maximum altitude
CDC = drone.ConfigDataCount
drone.setConfig("control:altitude_max","3500")                      # Request change of an option
drone.setConfig("control:control_yaw","6.11")
while CDC == drone.ConfigDataCount:     time.sleep(0.001)           # Wait until configuration has been set (after resync is done)
for i in drone.ConfigData:
    if i[0] == "control:altitude_max":	print "   "+str(i)+"   Count: "+str(drone.ConfigDataCount)+"   Timestamp: "+str(drone.ConfigDataTimeStamp)
for i in drone.ConfigData:
    if i[0] == "control:control_yaw":	print "   "+str(i)+"   Count: "+str(drone.ConfigDataCount)+"   Timestamp: "+str(drone.ConfigDataTimeStamp)
