from drone_dancer import drone_dancer
import time
from play_song import play_song

beat_num = 0
onset_num = 0

# function to be called on a beat event
def beat_hook():
    global previous_mood, beat_num

    print 'beat %d' % beat_num

    # print('beat %d' % beat_num)
    # print('bpm %f confidence %f' % (audio.current_bpm(), audio.current_bpm_confidence()))
    # if audio.is_chorus():
    #     print 'chorus!'
    # else:
    #     print 'sparse...'


    if beat_num > 16:
        dancer.enqueue_move(dancer.dance_moves.MOVE_BOB_FBLR, 0.15, delay=0.15)
    else:
        dancer.enqueue_move(dancer.dance_moves.MOVE_BOB_FB, 0.15, delay=0.15)

    beat_num = beat_num + 1

# function to be called on the onset event
def onset_hook():
    global onset_num
    # time.sleep(0.15)

    print('onset %d' % onset_num)

    dancer.enqueue_move(dancer.dance_moves.MOVE_BOB_CLOCKWISE, 0.15, delay=0.15)

    onset_num = onset_num + 1


filename = '../music/actionclip.wav'

# analyse audio
audio = play_song(filename, 25.99)

# initialize drone
dancer = drone_dancer()
dancer.takeoff(True)
# #dancer.takeoff(False)
print('waiting for drone to be ready')
while not dancer.ready():
    time.sleep(0.05)

# configure drone
# increase max yaw speed
dancer.drone.setConfig('control:control_yaw', '6.11')
CDC = dancer.drone.ConfigDataCount
while CDC == dancer.drone.ConfigDataCount: time.sleep(0.01)

print('drone ready, starting song')
print('setting beat onset hook')
audio.set_onset_event(onset_hook)
audio.start()

# wait for audio to start
while audio.current_time() < 0.1: # this may cause underrun
    time.sleep(0.001)

# The audio has started, start the drone dancing
dancer.start_dancing()


# wait for buildup
time.sleep(13.5)

audio.set_onset_event(None)
dancer.enqueue_move(dancer.dance_moves.MOVE_SPIN_CLOCKWISE, 6.5)
print('spinning')

print('going up')

dancer.enqueue_move(dancer.dance_moves.MOVE_SPIN_CLOCKWISE_UP, 4.0)
dancer.enqueue_move(dancer.dance_moves.MOVE_NONE, 0.5)

print('flip!')
dancer.enqueue_move(dancer.dance_moves.MOVE_FLIP, 2.0)


print('moving to bpm')
print('setting beat event hook')
audio.set_beat_event(beat_hook)
audio.set_force_beat_event()


# sleep until the drone has finished its routine
time.sleep(50)

dancer.stop_dancing()

dancer.land()

audio.stop()
