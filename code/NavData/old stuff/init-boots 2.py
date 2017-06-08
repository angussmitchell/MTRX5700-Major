## MTRX5700
# Xue Yin Zhang
#
# Get some navigation while starting up and calibrating and doing a move

## clean startup sequence
import time, sys
import ps_drone         # Import PS-Drone-API
import pickle           # python library to save and restore variables
import boot

## create empty lists wher we store the navdata
pitch = []
roll = []
yaw = []
demo_alt = []
nav_time = []
magneto = []
magneto_raw = []
pwm_fl = []
pwm_fr = []
pwm_br = []
pwm_bl = []
altitude_ref = []
detect_n = []
detect_type = []
detect_x = []
detect_y = []
detect_width = []
detect_depth = []
detect_dist = []
detect_ang = []
detect_rot = []
checksum = []

## function to store all the navdata
def append_nav():
    pitch.append(drone.NavData["demo"][2][0])   # theta
    roll.append(drone.NavData["demo"][2][1])    # phi
    yaw.append(drone.NavData["demo"][2][2])     # psi
    demo_alt.append(drone.NavData["demo"][3])   # altitude in
    vx.append(drone.NavData["demoe"][4][0])     # velocity in
    nav_time.append(drone.NavData["time"][0])
    magneto.append(drone.NavData["magneto"][0])
    magneto_raw.append(drone.NavData["magneto"][1])
    pwm_fl.append(drone.NavData["pwm"][0][0])
    pwm_fr.append(drone.NavData["pwm"][0][1])
    pwm_br.append(drone.NavData["pwm"][0][2])
    pwm_bl.append(drone.NavData["pwm"][0][3])
    altitude_ref.append(drone.NavData["altitude"][3])   # altitude in mm
    detect_n.append(drone.NavData["vision_detect"][0])      # number of markers detected
    if detect_n[-1] > 0:
        print "detected tag"
    detect_type.append(drone.NavData["vision_detect"][1])   # types of detected markers
    detect_x.append(drone.NavData["vision_detect"][2])
    detect_y.append(drone.NavData["vision_detect"][3])
    detect_width.append(drone.NavData["vision_detect"][4])
    detect_depth.append(drone.NavData["vision_detect"][5])
    detect_dist.append(drone.NavData["vision_detect"][6])
    detect_ang.append(drone.NavData["vision_detect"][7])
    detect_rot.append(drone.NavData["vision_detect"][9])
    return

def wait_nav(time_s):
    NDC = drone.NavDataCount
    start = time.time()
    while (time.time() - start) < time_s:
        while drone.NavDataCount == NDC:  time.sleep(0.001)                       # Wait until next time-unit
        NDC = drone.NavDataCount
        append_nav()
    return

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

drone.moveUp(0.5)
print "anim 0"
wait_nav(0.45)

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
    pickle.dump([pitch, roll, yaw, demo_alt, nav_time, magneto, magneto_raw, pwm_fl, pwm_fr, pwm_br, pwm_bl, detect_n, detect_type, detect_x, detect_y, detect_width, detect_depth, detect_dist, detect_ang, detect_rot, checksum], f)
