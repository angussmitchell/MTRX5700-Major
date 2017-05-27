### MTRX5700
# Dancing Drone
# Angus, Neill, Xue Yin
#
# drone_presets.py
#  - collection of functions for preset moves on the drone
#  - e.g. clean start up, bobbing, spinning, landing


## clean start up routine
def clean_start():
    drone = ps_drone.Drone()    # Initializes the PS-Drone-API
    drone.startup()             # Connects to the drone and starts subprocesses

    drone.reset()               # Sets drones LEDs to green when red
    while (drone.getBattery()[0]==-1): time.sleep(0.1) # Reset completed?
    print "battery:" + str(drone.getBattery()[0]) + "% " + str(drone.getBattery()[1])
    if drone.getBattery()[1] == "empty": sys.exit()

    drone.useDemoMode(True)     # 15 basic datasets per second (default)
    drone.getNDpackage(["demo"])    # Packets, which shall be decoded
    time.sleep(0.5)             # Give it some time to fully awake

    drone.trim()                # Recalibrate sensors
    drone.getSelfRotation(5)    # Auto-alteration-value of gyroscope-sensor
    print "Auto-alternation: " + str(drone.selfRotation) + "deg/sec"

    drone.takeoff()
    time.sleep(7.5)             # gives the drone time to start
    while drone.NavData["demo"][0][2]: time.sleep(0.1)  # still in landed mode?
    return drone

