## MTRX5700
# Xue Yin Zhang
#
# Get some navigation while starting up and calibrating and doing a move

## clean startup sequence
import time, sys
import ps_drone         # Import PS-Drone-API
import pickle

## create empty lists where we store the navdata
pitch = []
roll = []
yaw = []
vx = []
vy = []
vz = []
nav_time = []
mx = []
my = []
mz = []
altitude_ref = []
detect_n = []
detect_dist = []
detect_rot = []

## store all the navdata
def append_nav(drone):
    pitch.append(drone.NavData["demo"][2][0])   # theta
    roll.append(drone.NavData["demo"][2][1])    # phi
    yaw.append(drone.NavData["demo"][2][2])     # psi
    vx.append(drone.NavData["demo"][4][0])      # velocity in x-direction
    vy.append(drone.NavData["demo"][4][1])      # velocity in y-direction
    vz.append(drone.NavData["demo"][4][2])
    nav_time.append(drone.NavData["time"][0])
    mx.append(drone.NavData["magneto"][0][0])
    my.append(drone.NavData["magneto"][0][1])
    mz.append(drone.NavData["magneto"][0][2])
    altitude_ref.append(drone.NavData["altitude"][0])   # altitude in mm
    detect_n.append(drone.NavData["vision_detect"][0])      # number of markers detected
    detect_dist.append(drone.NavData["vision_detect"][6][0])
    detect_rot.append(drone.NavData["vision_detect"][7][0])
    return

## receive navdata packet
def wait_nav(drone, time_s):
    NDC = drone.NavDataCount
    start = time.time()
    while (time.time() - start) < time_s:
        
        if drone.NavData["altitude"][0] > 2500:
            print "drone too high, stop and land"
            drone.stop()
            print "stop"
            time.sleep(0.5)
            drone.land()
            save_nav()
            sys.exit("exited program")
    
        if drone.NavData["vision_detect"][0] > 0:
            print "detected tag, telling drone to stop and land"
            rot = drone.NavData["vision_detect"][7][0]
            
            
            drone.stop()
            print "stop"
            time.sleep(0.5)
            drone.land()
            save_nav()
            sys.exit("exited program")
    
        while drone.NavDataCount == NDC:  time.sleep(0.001)                       # Wait until next time-unit
        NDC = drone.NavDataCount
        append_nav(drone)

    return

def save_nav():
    print "trying to save data..."
    with open('navdata-vars.pickle', 'w') as f:  # Python 3: open(..., 'wb')
        pickle.dump([pitch, roll, yaw, vx, vy, vz, nav_time, mx, my, mz, altitude_ref, detect_n, detect_dist, detect_rot], f)
    print "saved navdata"
