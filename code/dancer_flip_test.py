from drone_dancer import drone_dancer
import time

dancer = drone_dancer()


dancer.takeoff(True)



dancer.drone.moveUp(1)
time.sleep(1)


dancer.do_move(dancer.dance_moves.MOVE_FLIP, 2)

time.sleep(1)

dancer.drone.stop()

dancer.land()