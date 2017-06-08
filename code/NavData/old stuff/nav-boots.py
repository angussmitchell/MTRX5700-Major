## MTRX5700
# Xue Yin Zhang
#
# Dependencies: check init_boots.py to see which data packages have been enabled
#
# Note to Neill: check battery status before each move

##### Suggested clean drone startup sequence #####
import time, sys
import ps_drone                                                               # Import PS-Drone-API


def get_navdata(NDC_old):
    
    # check if new package has come in
    while drone.NavDataCount == NDC_old:  time.sleep(0.001)                       # Wait until next time-unit

    # check battery status
    
    # check if landed


print "-----------"
print "Aptitude [X,Y,Z] :            "+str(drone.NavData["demo"][2])
print "Altitude / sensor / pressure: "+str(drone.NavData["altitude"][3])+" / "+str(drone.State[21])+" / "+str(drone.NavData["pressure_raw"][0])
print "Megnetometer [X,Y,Z]:         "+str(drone.NavData["magneto"][0])
print "Wifi link quality:            "+str(drone.NavData["wifi"])

start = time.time()
NDC = drone.NavDataCount

while (time.time() - start) < 0.45:
    while drone.NavDataCount == NDC:  time.sleep(0.001)                       # Wait until next time-unit
    NDC=drone.NavDataCount
    print "-----------"
    print "Aptitude [X,Y,Z] :            "+str(drone.NavData["demo"][2])
    print "Altitude / sensor / pressure: "+str(drone.NavData["altitude"][3])+" / "+str(drone.State[21])+" / "+str(drone.NavData["pressure_raw"][0])
    print "Megnetometer [X,Y,Z]:         "+str(drone.NavData["magneto"][0])
    print "Wifi link quality:            "+str(drone.NavData["wifi"])

drone.stop()

while (time.time() - start) < 0.45:
    while drone.NavDataCount == NDC:  time.sleep(0.001)                       # Wait until next time-unit
    NDC=drone.NavDataCount
    print "-----------"
    print "Aptitude [X,Y,Z] :            "+str(drone.NavData["demo"][2])
    print "Altitude / sensor / pressure: "+str(drone.NavData["altitude"][3])+" / "+str(drone.State[21])+" / "+str(drone.NavData["pressure_raw"][0])
    print "Megnetometer [X,Y,Z]:         "+str(drone.NavData["magneto"][0])
    print "Wifi link quality:            "+str(drone.NavData["wifi"])


drone.land()

while (time.time() - start) < 0.60:
    while drone.NavDataCount == NDC:  time.sleep(0.001)                       # Wait until next time-unit
    NDC=drone.NavDataCount
    print "-----------"
    print "Aptitude [X,Y,Z] :            "+str(drone.NavData["demo"][2])
    print "Altitude / sensor / pressure: "+str(drone.NavData["altitude"][3])+" / "+str(drone.State[21])+" / "+str(drone.NavData["pressure_raw"][0])
    print "Megnetometer [X,Y,Z]:         "+str(drone.NavData["magneto"][0])
    print "Wifi link quality:            "+str(drone.NavData["wifi"])

