from drone_dancer import drone_dancer
import time

dancer = drone_dancer()

dancer.start_getting_navdata()

dancer.takeoff(True)

print('MOVING FORWARD')
dancer.drone.moveForward(0.1)

time.sleep(1000)
