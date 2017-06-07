## MTRX5700
# Xue Yin Zhang
#
# Get some navigation while starting up and calibrating and doing a move

## clean startup sequence
import time, sys
import ps_drone         # Import PS-Drone-API
import pickle           # python library to save and restore variables

## clean start up
drone = ps_drone.Drone()                                                      # Start using drone
drone.startup()                                                               # Connects to drone and starts subprocesses
drone.reset()                                                                 # Sets drone's status to good (LEDs turn green when red)
while (drone.getBattery()[0] == -1):  time.sleep(0.1)                         # Wait until the drone has done its reset
print "Battery: "+str(drone.getBattery()[0])+"%  "+str(drone.getBattery()[1]) # Gives a battery-status
drone.useDemoMode(False)                                                      # Give me everything...fast
#drone.getNDpackage(["demo", "time", "pwm", "raw_measures", "phys_measures", "gyros_offsets", "altitude", "magneto", "euler_angles", "references", "rc_references", "vision_detect", "vision", "vision_raw", "vision_of", "vision_perf", "trackers_send", "video_stream", "hdvideo_stream", "games", "trims", "pressure_raw", "wind_speed", "kalman_pressure", "watchdog", "wifi", "adc_data_frame", "zimmu_3000", "chksum"])       # Packets, which shall be decoded
drone.getNDpackage(["all"])       # Packets, which shall be decoded
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
    print "Aptitude [X,Y,Z] :            "+str(drone.NavData["demo"][2])
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

