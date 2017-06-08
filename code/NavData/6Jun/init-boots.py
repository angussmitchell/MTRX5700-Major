## MTRX5700
# Xue Yin Zhang
#
# Get some navigation while starting up and calibrating and doing a move

## clean startup sequence
import time, sys
import ps_drone         # Import PS-Drone-API
import pickle           # python library to save and restore variables

## function to store all the navdata
def append_nav(drone.NavData):
    pitch.append(drone.NavData["demo"][2][0])   # theta
    roll.append(drone.NavData["demo"][2][1])    # phi
    yaw.append(drone.NavData["demo"][2][2])     # psi
    demo_alt.append(drone.NavData["demo"][3])
    nav_time.append(drone.NavData["time"])
    magneto.append(drone.NavData["magneto"][0])
    magneto_raw.append(drone.NavData["magneto"][1])
    altitude_ref.append(drone.NavData["altitude"])
    pressure_raw.append(drone.NavData["pressure_raw"])


## create empty lists wher we store the navdata
pitch = []
roll = []
yaw = []
demo_alt = []
nav_time = []
magneto = []
magneto_raw = []
altitude_ref = []
pressure_raw = []
wind_speed = []
pwm = []
vision_detect = []
checksum = []

## clean start up
drone = ps_drone.Drone()                                                      # Start using drone
drone.startup()                                                               # Connects to drone and starts subprocesses
drone.reset()                                                                 # Sets drone's status to good (LEDs turn green when red)
while (drone.getBattery()[0] == -1):  time.sleep(0.1)                         # Wait until the drone has done its reset
print "Battery: "+str(drone.getBattery()[0])+"%  "+str(drone.getBattery()[1]) # Gives a battery-status
drone.useDemoMode(False)                                                      # Give me everything...fast
drone.getNDpackage(["demo", "time", "pwm", "altitude", "magneto", "pressure_raw", "wind_speed", "wifi", "chksum"])       # Packets, which shall be decoded
#drone.getNDpackage(["all"])       # Packets, which shall be decoded
time.sleep(1.0)                                                               # Give it some time to awake fully after reset

drone.trim()                # Recalibrate sensors
drone.getSelfRotation(5)    # Auto-alteration-value of gyroscope-sensor
print "Auto-alternation: " + str(drone.selfRotation) + "deg/sec"

## main program
NDC = drone.NavDataCount
drone.takeoff()
start = time.time()
print "Takeoff"
while (time.time() - start) < 7.0:
    while drone.NavDataCount == NDC:  time.sleep(0.001)                       # Wait until next time-unit
    NDC=drone.NavDataCount
    print "-----------"
    print "Altitude / sensor / pressure: "+str(drone.NavData["altitude"][3])+" / "+str(drone.State[21])+" / "+str(drone.NavData["pressure_raw"][0])
    print "Megnetometer [X,Y,Z]:         "+str(drone.NavData["magneto"][0])
    print "Wifi link quality:            "+str(drone.NavData["wifi"])
#while drone.NavData["demo"][0][2]: time.sleep(0.1)  # still in landed mode?
drone.mtrim()
start = time.time()
print "mtrim"
while (time.time() - start) < 3.0:
    while drone.NavDataCount == NDC:  time.sleep(0.001)                       # Wait until next time-unit
    NDC=drone.NavDataCount
    print "-----------"
    print "Aptitude [X,Y,Z] :            "+str(drone.NavData["demo"][2])
    print "Altitude / sensor / pressure: "+str(drone.NavData["altitude"][3])+" / "+str(drone.State[21])+" / "+str(drone.NavData["pressure_raw"][0])
    print "Megnetometer [X,Y,Z]:         "+str(drone.NavData["magneto"][0])
    print "Wifi link quality:            "+str(drone.NavData["wifi"])

drone.anim(0,1000)
start = time.time()
print "anim 0"
while (time.time() - start) < 0.45:
    while drone.NavDataCount == NDC:  time.sleep(0.001)                       # Wait until next time-unit
    NDC=drone.NavDataCount
    print "-----------"
    print "Aptitude [X,Y,Z] :            "+str(drone.NavData["demo"][2])
    print "Altitude / sensor / pressure: "+str(drone.NavData["altitude"][3])+" / "+str(drone.State[21])+" / "+str(drone.NavData["pressure_raw"][0])
    print "Megnetometer [X,Y,Z]:         "+str(drone.NavData["magneto"][0])
    print "Wifi link quality:            "+str(drone.NavData["wifi"])

drone.stop()
start = time.time()
print "stop"
while (time.time() - start) < 0.45:
    while drone.NavDataCount == NDC:  time.sleep(0.001)                       # Wait until next time-unit
    NDC=drone.NavDataCount
    print "-----------"
    print "Aptitude [X,Y,Z] :            "+str(drone.NavData["demo"][2])
    print "Altitude / sensor / pressure: "+str(drone.NavData["altitude"][3])+" / "+str(drone.State[21])+" / "+str(drone.NavData["pressure_raw"][0])
    print "Megnetometer [X,Y,Z]:         "+str(drone.NavData["magneto"][0])
    print "Wifi link quality:            "+str(drone.NavData["wifi"])


drone.land()
print "land"
start = time.time()
while (time.time() - start) < 0.60:
    while drone.NavDataCount == NDC:  time.sleep(0.001)                       # Wait until next time-unit
    NDC=drone.NavDataCount
    print "-----------"
    print "Aptitude [X,Y,Z] :            "+str(drone.NavData["demo"][2])
    print "Altitude / sensor / pressure: "+str(drone.NavData["altitude"][3])+" / "+str(drone.State[21])+" / "+str(drone.NavData["pressure_raw"][0])
    print "Megnetometer [X,Y,Z]:         "+str(drone.NavData["magneto"][0])
    print "Wifi link quality:            "+str(drone.NavData["wifi"])

#with open('navdata-vars.pickle', 'w') as f:  # Python 3: open(..., 'wb')
#    pickle.dump([obj0, obj1, obj2], f)
