from drone_dancer import drone_dancer
import time
from play_song import play_song

beat_num = 0

flipped = False

def hook():
    if audio.current_time() > 8.0:
        global beat_num, flipped

        if beat_num == 7:
            dancer.enqueue_move(dancer.dance_moves.MOVE_FLIP, audio.current_beat_s() - 0.01)
        elif beat_num < 8:
            dancer.enqueue_move(dancer.dance_moves.MOVE_BOB_CLOCKWISE, audio.current_beat_s())
        else:
            dancer.enqueue_move(dancer.dance_moves.MOVE_BOB_FBLR, 0.1)

        beat_num = beat_num + 1

    elif audio.current_time() > 7.5 and flipped == False:
        dancer.do_move(dancer.enqueue_move(dancer.dance_moves.MOVE_FLIP, 1.1))
        dancer.start_dancing()
        flipped = True


audio = play_song('./music/buildupdrop.wav')

# for i in range(0, 100):
#     # print('current time is %f' % audio.current_time())
#     # print('current bpm is %f' % audio.current_bpm())
#     time.sleep(0.1)


dancer = drone_dancer()


dancer.takeoff(True)



print('waiting for drone to be ready')
while not dancer.ready():
    time.sleep(0.05)

audio.start()


dancer.drone.moveUp(1)
time.sleep(1.5)
dancer.drone.hover()

print('drone ready, starting song')


print('setting beat event hook')
audio.set_beat_event(hook)

# dancer.enqueue_move(dancer.dance_moves.MOVE_FLIP, 5)
# dancer.enqueue_move(dancer.dance_moves.MOVE_WIGGLE, 2, 2.5)
# dancer.enqueue_move(dancer.dance_moves.MOVE_QUICK_BOB, 2)

# dancer.start_dancing()

print('sleeping for 15 seconds then stopping')

time.sleep(15)

dancer.stop_dancing()

dancer.land()

audio.stop()