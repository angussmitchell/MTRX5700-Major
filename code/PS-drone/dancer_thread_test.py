from drone_dancer import drone_dancer
import time

dancer = drone_dancer()

dancer.enqueue_move(dancer.dance_moves.MOVE_FLIP, 5)
dancer.enqueue_move(dancer.dance_moves.MOVE_WIGGLE, 2, 2.5)
dancer.enqueue_move(dancer.dance_moves.MOVE_QUICK_BOB, 2)

dancer.start_dancing()

print('after')

time.sleep(6)

dancer.stop_dancing()
