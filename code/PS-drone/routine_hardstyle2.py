from drone_dancer import drone_dancer
import time
from play_song import play_song

# flipped = False

# def hook():
#     if audio.current_time() > 8.0:
#         global beat_num, flipped
#
#         # if beat_num == 7:
#         #     ###dancer.enqueue_move(###dancer.dance_moves.MOVE_FLIP, audio.current_beat_s() - 0.01)
#         if beat_num < 8:
#             ###dancer.enqueue_move(###dancer.dance_moves.MOVE_BOB_CLOCKWISE, audio.current_beat_s())
#         else:
#             ###dancer.enqueue_move(###dancer.dance_moves.MOVE_BOB_FBLR, 0.1)
#
#         beat_num = beat_num + 1
#
#     elif audio.current_time() > 7.0 and flipped == False:
#         ###dancer.enqueue_move(###dancer.dance_moves.MOVE_FLIP, 1.1)
#         ###dancer.start_dancing()
#         flipped = True
#


# previous_mood = drone_##dancer.dance_moods.MOOD_GO_HARD

beat_num = -4 # we actually skip the first bar
onset_num = 0

def beat_hook():
    global previous_mood, beat_num

    print 'beat %d' % beat_num

    # print('beat %d' % beat_num)
    # print('bpm %f confidence %f' % (audio.current_bpm(), audio.current_bpm_confidence()))
    # if audio.is_chorus():
    #     print 'chorus!'
    # else:
    #     print 'sparse...'

    # #dancer.enqueue_move(#dancer.dance_moves.MOVE_BOB_FB, 0.15, delay=0.15) # this was the original move

    # should start with fb bob
    dancer.auto_dance(audio.current_beat_s() - 0.05, dancer.bpm_to_frequency(audio.current_bpm())*2, delay=0.15)

    if beat_num == 4:
        dancer.reset_beat_count()

    beat_num = beat_num + 1

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
dancer.start_getting_navdata()

dancer.takeoff(True)

#dancer.takeoff(False)
print('waiting for drone to be ready')
while not dancer.ready():
    time.sleep(0.05)



print('drone ready, starting song')

print('setting beat onset hook')
audio.set_onset_event(onset_hook)

audio.start()


# wait for audio to start
while audio.current_time() < 0.1: # todo this may cause underrun
    time.sleep(0.001)

# The audio has started, start the drone dancing
dancer.start_dancing()


# wait for buildup
time.sleep(13.5)

audio.set_onset_event(None)
dancer.enqueue_move(dancer.dance_moves.MOVE_SPIN_CLOCKWISE, 6.5)
print('spinning')
time.sleep(8) #todo remove this


print('going up')
time.sleep(3.5) #todo remove this

dancer.enqueue_move(dancer.dance_moves.MOVE_SPIN_CLOCKWISE_UP, 4.0)
dancer.enqueue_move(dancer.dance_moves.MOVE_NONE, 0.5)

print('flip!')
time.sleep(2) # todo remove this
dancer.enqueue_move(dancer.dance_moves.MOVE_FLIP, 2.0)


print('moving to bpm')
print('setting beat event hook')

audio.set_beat_event(beat_hook)
audio.set_force_beat_event()

print('moving forward back, then auto dance for rest of song')

time.sleep(60)

# DEBUG

# while True:
#     # print audio.current_bpm_confidence()
#     # print audio.current_bpm()
#     # print audio.current_time()
#     time.sleep(0.5)


dancer.stop_dancing()

dancer.land()

audio.stop()