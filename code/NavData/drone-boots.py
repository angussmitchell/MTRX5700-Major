## MTRX5700
# Xue Yin Zhang
#
# Get some navigation while starting up and calibrating and doing a move

## clean startup sequence
import time, sys
import ps_drone         # Import PS-Drone-API
import pickle           # python library to save and restore variables
import boots

## drone variables
multi_config = True
demo_mode = True
front_cam = False

## clean start up
drone = ps_drone.Drone()                                                      # Start using drone
drone.startup()                                                               # Connects to drone and starts subprocesses
drone.reset()                                                                 # Sets drone's status to good (LEDs turn green when red)
while (drone.getBattery()[0] == -1):  time.sleep(0.1)                         # Wait until the drone has done its reset

### make sure drone has enough battery
#if drone.getBattery()[0] < 30:
#    print "battery too low"
#    drone.land()        # land for safety (even though it's not in the air atm)
#    quit()              # end program

## print out battery status
print "Battery: "+str(drone.getBattery()[0])+"%  "+str(drone.getBattery()[1]) # Gives a battery-status

## set mode of data packages
drone.useDemoMode(demo_mode)
if demo_mode == False:
#        drone.getNDpackage(["demo", "time", "pwm", "altitude", "magneto", "vision_detect", "chksum"])   # Packets, which shall be decoded
    drone.getNDpackage(["all"])         # Packets, which shall be decoded
    print "Demo mode: off"
else:
    drone.getNDpackage(["demo", "vision_detect"])
    print "Demo mode: on"

time.sleep(0.5)

## configure the drone
if multi_config == True:
    print "using multi-configuration mode to enable camera"
    drone.setConfigAllID()              # use multi-configuration mode to enable camera
    CDC = drone.ConfigDataCount
    while CDC == drone.ConfigDataCount:    time.sleep(0.0001)    # Wait until configuration has been set (after resync is done)
    for i in drone.ConfigData:
        if i[0].count("custom:")==1 and i[0].count("_id")==1:    print str(i)

#    drone.useMDemoMode(demo_mode)
#
#    ## set mode of data packages
#    if demo_mode == False:
##        drone.getNDpackage(["demo", "time", "pwm", "altitude", "magneto", "vision_detect", "chksum"])   # Packets, which shall be decoded
#        drone.getNDpackage(["all"])         # Packets, which shall be decoded
#        print "Demo mode: off"
#    else:
#        drone.getNDpackage(["demo", "vision_detect"])
#        print "Demo mode: on"
#
#    time.sleep(0.5)
#
#    if drone.State[10] != demo_mode:
#        print "drone.useMDemoMode() does not work!"

    ## set up vision detection
    # Shell-Tag=1, Roundel=2, Black Roundel=4, Stripe=8, Cap=16, Shell-Tag V2=32, Tower Side=64, Oriented Roundel=128
    #drone.setConfig("detect:detect_type", "3")                     # Enable universal detection
    drone.setMConfig("detect:detect_type","10")
    #drone.setMConfig("detect:detections_select_h", "128")           # oriented roundel front camera
    drone.setMConfig("detect:detections_select_v", "128")   # oriented roundel with ground camera
    CDC = drone.ConfigDataCount
    while CDC == drone.ConfigDataCount:    time.sleep(0.01)        # Wait until configuration has been set

    ## select camera
    if front_cam == True:
        drone.frontCam()    # front camera
        print "Front camera: on"
        print "Back camera: off"
    else:
        drone.groundCam()   # back camera
        print "Front camera: off"
        print "Back camera: on"

else:
    ## see default config
    print "default IDs:"
    for i in drone.ConfigData:
        if i[0].count("custom:")==1 and i[0].count("_id")==1:    print str(i)
    
    ## set mode of data packages
    if demo_mode == True:
        drone.useDemoMode(True)
        drone.getNDpackage(["demo", "vision_detect"])
    else:
        drone.useDemoMode(False)    # Get data 200 times a second
        drone.getNDpackage(["demo", "time", "pwm", "altitude", "magneto", "vision_detect", "chksum"])   # Packets, which shall be decoded
    #drone.getNDpackage(["all"])         # Packets, which shall be decoded

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

# check what data packages are being sent/received
if drone.State[10] == 0:
    print "Navdata: all"
else:
    print "Navdata: demo"
#    drone.useDemoMode(True)
#    drone.getNDpackage("all")
#    time.sleep(0.5)
#    if drone.State[10] == 0:
#        print "Navdata: changed to all"

drone.takeoff()
print "Takeoff"
boots.wait_nav(drone, 7.0)

while drone.NavData["demo"][0][2]: time.sleep(0.1)  # still in landed mode?
drone.mtrim()
print "mtrim"
boots.wait_nav(drone, 3.0)

move_time = []

#move_time.append(drone.NavData["time"][0])
drone.moveUp(1)
print "move up"
boots.wait_nav(drone, 0.5)
#move_time.append(drone.NavData["time"][0])

drone.hover()
print "hover"
boots.wait_nav(drone, 0.5)

#move_time.append(drone.NavData["time"][0])
drone.anim(0,1000)
print "anim 0"
boots.wait_nav(drone, 0.5)
#move_time.append(drone.NavData["time"][0])

drone.stop()
print "stop"
boots.wait_nav(drone, 0.45)

drone.land()
print "land"
boots.wait_nav(drone, 2.0)

boots.save_nav()
