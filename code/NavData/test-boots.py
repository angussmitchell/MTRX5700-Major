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
while CDC == drone.ConfigDataCount:     time.sleep(0.001)           # Wait until configuration has been set (after resync is done)
for i in drone.ConfigData:
    if i[0] == "control:altitude_max":	print "   "+str(i)+"   Count: "+str(drone.ConfigDataCount)+"   Timestamp: "+str(drone.ConfigDataTimeStamp)


## set up vision detection
# Shell-Tag=1, Roundel=2, Black Roundel=4, Stripe=8, Cap=16, Shell-Tag V2=32, Tower Side=64, Oriented Roundel=128
drone.setConfig("detect:detect_type","5")
#drone.setMConfig("detect:detections_select_h", "128")           # oriented roundel front camera
drone.setConfig("detect:detections_select_v", "128")   # oriented roundel with ground camera
CDC = drone.ConfigDataCount
while CDC == drone.ConfigDataCount:    time.sleep(0.01)        # Wait until configuration has been set

time.sleep(1.0)         # Give it some time to awake fully

drone.trim()                # Recalibrate sensors
drone.getSelfRotation(5)    # Auto-alteration-value of gyroscope-sensor
print "Auto-alternation: " + str(drone.selfRotation) + "deg/sec"

## check to see if vision is actually enabled
if drone.State[1] == 1:
    print "Video: enabled"
else:
    print "Video: disabled"

if drone.State[2] == 1:
    print "Vision: enabled"
else:
    print "Vision: disabled"

if drone.State[7] == 1:
    print "Camera: ready"
else:
    print "Camera: not ready"

## main program


