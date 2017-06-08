## MTRX5700
# Xue Yin Zhang
#
# Get some navigation while starting up and calibrating and doing a move

## clean startup sequence
import time, sys
import ps_drone         # Import PS-Drone-API
import pickle           # python library to save and restore variables
#import boots

## create empty lists where we store the navdata
pitch = []
roll = []
yaw = []
demo_alt = []
vx = []
vy = []
vz = []
nav_time = []
mx = []
my = []
mz = []
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

## store all the navdata
def append_nav(drone):
    pitch.append(drone.NavData["demo"][2][0])   # theta
    roll.append(drone.NavData["demo"][2][1])    # phi
    yaw.append(drone.NavData["demo"][2][2])     # psi
    demo_alt.append(drone.NavData["demo"][3])   # altitude in
    vx.append(drone.NavData["demo"][4][0])      # velocity in x-direction
    vy.append(drone.NavData["demo"][4][1])      # velocity in y-direction
    vz.append(drone.NavData["demo"][4][2])
    nav_time.append(drone.NavData["time"][0])
    mx.append(drone.NavData["magneto"][0][0])
    my.append(drone.NavData["magneto"][0][1])
    mz.append(drone.NavData["magneto"][0][2])
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

## receive navdata packet
def wait_nav(drone, time_s):
    NDC = drone.NavDataCount
    start = time.time()
    while (time.time() - start) < time_s:
        while drone.NavDataCount == NDC:  time.sleep(0.001)                       # Wait until next time-unit
        NDC = drone.NavDataCount
        append_nav(drone)
    return

def save_nav():
    with open('navdata-vars.pickle', 'w') as f:  # Python 3: open(..., 'wb')
        pickle.dump([pitch, roll, yaw, demo_alt, vx, vy, vz, nav_time, mx, my, mz, pwm_fl, pwm_fr, pwm_br, pwm_bl, detect_n, detect_type, detect_x, detect_y, detect_width, detect_depth, detect_dist, detect_ang, detect_rot, checksum], f)

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
drone.useDemoMode(False)
drone.getNDpackage(["demo", "time", "pwm", "altitude", "magneto", "vision_detect", "chksum"])         # Packets, which shall be decoded
time.sleep(1.0)

## set up vision detection
# Shell-Tag=1, Roundel=2, Black Roundel=4, Stripe=8, Cap=16, Shell-Tag V2=32, Tower Side=64, Oriented Roundel=128
#drone.setConfig("detect:detect_type", "3")                     # Enable universal detection
drone.setConfig("detect:detect_type","10")
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

# check what data packages are being sent/received
if drone.State[10] == 0:
    print "Navdata: all"
else:
    print "Navdata: demo. dumb drone"
    drone.useDemoMode(demo_mode)

drone.takeoff()
print "Takeoff"
wait_nav(drone, 7.0)

while drone.NavData["demo"][0][2]: time.sleep(0.1)  # still in landed mode?
drone.mtrim()
print "mtrim"
wait_nav(drone, 3.0)

move_time = []

#move_time.append(drone.NavData["time"][0])
drone.moveUp(1)
print "move up"
wait_nav(drone, 0.5)
#move_time.append(drone.NavData["time"][0])

drone.hover()
print "hover"
wait_nav(drone, 0.5)

#move_time.append(drone.NavData["time"][0])
drone.anim(0,1000)
print "anim 0"
wait_nav(drone, 0.5)
#move_time.append(drone.NavData["time"][0])

drone.stop()
print "stop"
wait_nav(drone, 0.45)

drone.land()
print "land"
wait_nav(drone, 2.0)

save_nav()
