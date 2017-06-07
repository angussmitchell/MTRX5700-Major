from drone_dancer import drone_dancer
import time

dancer = drone_dancer()

dancer.takeoff(True)


print('waiting for drone to be ready')
while not dancer.ready():
    time.sleep(0.05)


dancer.do_move(dancer.dance_moves.MOVE_BOB_FBLR, 0.5)
time.sleep(0.5)
dancer.do_move(dancer.dance_moves.MOVE_BOB_FBLR, 0.5)
time.sleep(0.5)
dancer.do_move(dancer.dance_moves.MOVE_BOB_FBLR, 0.5)
time.sleep(0.5)
dancer.do_move(dancer.dance_moves.MOVE_BOB_FBLR, 0.5)
time.sleep(0.5)

dancer.land()