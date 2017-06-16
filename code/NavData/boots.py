## MTRX5700
# Xue Yin Zhang
#
# Get some navigation while starting up and calibrating and doing a move

## clean startup sequence
import time, sys
import ps_drone         # Import PS-Drone-API
import pickle
import numpy as np

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
    start = time.time()
    NDC = drone.NavDataCount
    while (time.time() - start) < time_s:
        
        if drone.NavData["altitude"][0] > 1500:     # drone has reached soft altitude limit
            print "drone too high, stop and land"
            drone.stop()
            print "stopped"
            time.sleep(1.0)
            drone.moveDown(1.0)
            print "moving down"
            time.sleep(3.0)
            print "landing"
            drone.land()
            save_nav()
            sys.exit("exited program")
    
        if drone.NavData["vision_detect"][0] > 0:   # drone sees a tag
            print "detected tag, telling drone to stop and land"
#            drone.stop()        # stop the drone
#            time.sleep(2.0)
#            alpha = drone.NavData["vision_detect"][7][0]
            self_correct(drone)
        
#            beta = 180.0 - alpha
#            if beta == 180.0:
#                beta = beta + 0.1
#            drone.turnAngle(beta,0.25)
#            time.sleep(2.0)
#            drone.moveForward(0.1)
#            time.sleep(6.0)

#            drone.stop()
#            print "stop"
#            time.sleep(0.5)
#            drone.land()
#            save_nav()
#            sys.exit("exited program")

        dbstart = time.time()
#        print "start time: " + str(dbstart)
        # wait for the next data package
        while drone.NavDataCount == NDC:  time.sleep(0.001)                       # Wait until next time-unit
        NDC = drone.NavDataCount
        append_nav(drone)
        print "delta time: " + str(time.time() - dbstart)

    return

def self_correct(drone):
    
    drone.stop()        # stop the drone
    time.sleep(1.0)
    print "drone has seen marker, drone stopped"
    
    # get new angle reading
    NDC = drone.NavDataCount
    while drone.NavDataCount == NDC:  time.sleep(0.001)                       # Wait until next time-unit
    alpha = drone.NavData["vision_detect"][7][0]
    
    speed_scale = 0.08   # set the speed for the movement
    
#    alpha = alpha + 180.0       # because of maths!! see my notepad (in red pen) for more details
    alpha = alpha - 90.0

    move1 = speed_scale*np.cos(np.deg2rad(alpha))   # left and right movements
    move1 = float(move1)
    move2 = speed_scale*np.sin(np.deg2rad(alpha))   # front and back movements
    move2 = float(move2)
#    print "motor 1 (L/R): " + move1
#    print "motor 2 (F/B): " + move2
    print move1
    print move2

#    drone.land()
#    time.sleep(2.0)
#    sys.exit("do not attempt drone.move yet")

    print "starting to move away from edge"
    drone.move(move1, move2, 0.0, 0.0)  # back away from the edge
    time.sleep(2.0)
    print "finished moving away from edge"
    
    drone.move(move1, move2, 0.0, 0.0)  # back away from the edge
    time.sleep(2.0)

#    drone.stop()
#    time.sleep(2.0)
#    if alpha > 190.0:           # drone needs to turn anti-clockwise to self-correct
#        
#        print "drone is turning left to self-correct"
#        drone.turnLeft(0.2)     # try to self-correct
#        
#        while alpha > 190.0:    # wait til angle is close enough
#            NDC = drone.NavDataCount
#            while drone.NavDataCount == NDC:  time.sleep(0.001) # wait for the next data package
#            alpha = drone.NavData["vision_detect"][7][0]
#        
#        print "done self-correcting for angle"
#    
#    elif alpha < 170.0:         # drone needs to turn clockwise to self-correct
#        
#        print "drone is turning right to self-correct"
#        drone.turnRight(0.2)    # try to self correct
#        
#        while alpha < 170.0:    # wait til angle is close enough
#            NDC = drone.NavDataCount
#            while drone.NavDataCount == NDC:  time.sleep(0.001) # wait for the next data package
#            alpha = drone.NavData["vision_detect"][7][0]
#        
#        print "done self-correcting for angle"
#    
#    # all cases of the previous if statement runs this bit of code
#    print "moving away from the edge"
#    drone.moveForward(0.25)
#    time.sleep(5.0)
#    print "done moving away from edge"
    return

def save_nav():
    print "trying to save data..."
    with open('navdata-vars.pickle', 'w') as f:  # Python 3: open(..., 'wb')
        pickle.dump([pitch, roll, yaw, vx, vy, vz, nav_time, mx, my, mz, altitude_ref, detect_n, detect_dist, detect_rot], f)
    print "saved navdata"

    return
