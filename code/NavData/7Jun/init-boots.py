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
print "Battery: "+str(drone.getBattery()[0])+"%  "+str(drone.getBattery()[1]) # Gives a battery-status
drone.useDemoMode(False)                                                      # Give me everything...fast
drone.getNDpackage(["demo", "time", "pwm", "altitude", "magneto", "vision_detect", "chksum"])       # Packets, which shall be decoded
#drone.getNDpackage(["all"])       # Packets, which shall be decoded
time.sleep(1.0)                                                               # Give it some time to awake fully after reset

## see default config
print "default IDs:"
for i in drone.ConfigData:
    if i[0].count("custom:")==1 and i[0].count("_id")==1:    print str(i)

## switch to multi-configuration mode
print "set default multiconfiguration:"
drone.setConfigAllID()
CDC = drone.ConfigDataCount
while CDC == drone.ConfigDataCount:    time.sleep(0.0001)    # Wait until configuration has been set (after resync is done)
for i in drone.ConfigData:
    if i[0].count("custom:")==1 and i[0].count("_id")==1:    print str(i)

## use ground camera
drone.groundCam()

### use front camera
#drone.frontCam()

# Setting up detection...
# Shell-Tag=1, Roundel=2, Black Roundel=4, Stripe=8, Cap=16, Shell-Tag V2=32, Tower Side=64, Oriented Roundel=128
#drone.setConfig("detect:detect_type", "3")                     # Enable universal detection
drone.setMConfig("detect:detect_type","5")
#drone.setMConfig("detect:detections_select_h", "128")           # Detect "Oriented Roundel" with front-camera
drone.setMConfig("detect:detections_select_v", "128")             # No detection with ground cam
CDC = drone.ConfigDataCount
while CDC == drone.ConfigDataCount:    time.sleep(0.01)        # Wait until configuration has been set

drone.trim()                # Recalibrate sensors
drone.getSelfRotation(5)    # Auto-alteration-value of gyroscope-sensor
print "Auto-alternation: " + str(drone.selfRotation) + "deg/sec"

## main program

drone.takeoff()
print "Takeoff"
wait_nav(7.0)

while drone.NavData["demo"][0][2]: time.sleep(0.1)  # still in landed mode?
drone.mtrim()
print "mtrim"
wait_nav(3.0)

drone.moveUp(1)
print "move up"
wait_nav(0.5)

drone.hover()
print "hover"
wait_nav(0.5)

drone.stop()
print "stop"
wait_nav(0.45)

drone.land()
print "land"
wait_nav(2.0)

with open('navdata-vars.pickle', 'w') as f:  # Python 3: open(..., 'wb')
    pickle.dump([pitch, roll, yaw, demo_alt, vx, vy, vz, nav_time, magneto, magneto_raw, pwm_fl, pwm_fr, pwm_br, pwm_bl, detect_n, detect_type, detect_x, detect_y, detect_width, detect_depth, detect_dist, detect_ang, detect_rot, checksum], f)
