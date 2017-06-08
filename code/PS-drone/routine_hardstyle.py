from drone_dancer import drone_dancer
import time
from play_song import play_song
from cluster import cluster
import scipy.io.wavfile as wavfile

# replaced this with onset
# buildup_peaks_s = [0.80, 1.85, 2.82, 3.76, 4.63, 5.47, 6.26, 7.0, 7.7, 8.36, 8.9, 9.58, 10.13, 10.68, 11.19, 11.7,
#                    12.18, 12.65, 13.1, 13.55, 13.98] # continuous at 14.39

beat_num = 0

flipped = False

# def hook():
#     if audio.current_time() > 8.0:
#         global beat_num, flipped
#
#         # if beat_num == 7:
#         #     #dancer.enqueue_move(#dancer.dance_moves.MOVE_FLIP, audio.current_beat_s() - 0.01)
#         if beat_num < 8:
#             #dancer.enqueue_move(#dancer.dance_moves.MOVE_BOB_CLOCKWISE, audio.current_beat_s())
#         else:
#             #dancer.enqueue_move(#dancer.dance_moves.MOVE_BOB_FBLR, 0.1)
#
#         beat_num = beat_num + 1
#
#     elif audio.current_time() > 7.0 and flipped == False:
#         #dancer.enqueue_move(#dancer.dance_moves.MOVE_FLIP, 1.1)
#         #dancer.start_dancing()
#         flipped = True
#

filename = '../music/actionclip.wav'

rate, raw_data = wavfile.read(filename)
data = (raw_data[:,0]/2.0+raw_data[:,1]/2.0)


# get mfcc todo use cluster labels
time_song, labels, class_labels = cluster(data,samplerate=44100)

audio = play_song(filename)

# for i in range(0, 100):
#     # print('current time is %f' % audio.current_time())
#     # print('current bpm is %f' % audio.current_bpm())
#     time.sleep(0.1)


# dancer = drone_dancer()


#dancer.takeoff(True)



print('waiting for drone to be ready')
# while not dancer.ready():
#     time.sleep(0.05)

#dancer.drone.setConfig('control:indoor_control_yaw', '6.11')


for i in range(0, 21):#len(audio.onsets)): # todo was 21
    prev_time = 0
    if i > 1:
        prev_time = audio.onsets[i-1]
        print prev_time
    #dancer.enqueue_move(#dancer.dance_moves.MOVE_BOB_CLOCKWISE, audio.onsets[i] - prev_time)


# for i in range(0, 50):
#     #dancer.enqueue_move(#dancer.dance_moves.MOVE_SPIN_CLOCKWISE, 0.1)
#


# enqueue the initial bops using onset detection todo fix the drone going nuts at the start
# for i in range(0, 20):
#     dancer.enqueue_move(#dancer.dance_moves.MOVE_BOB_CLOCKWISE, 0.5 - (i + 10)/10.0)

#dancer.enqueue_move(#dancer.dance_moves.MOVE_SPIN_CLOCKWISE, 5.0)
#dancer.enqueue_move(#dancer.dance_moves.MOVE_FLIP, 1.0)

audio.start()

cluster_array_iterator = 0

while audio.current_time() < 0.1: # todo this may cause underrun


    time.sleep(0.001)

# time.sleep(0.3)

#dancer.start_dancing()






#
# #dancer.drone.moveUp(1)
# time.sleep(1.5)
# #dancer.drone.hover()
#
# print('drone ready, starting song')
#
#
# print('setting beat event hook')
# audio.set_beat_event(hook)
#
# # #dancer.enqueue_move(#dancer.dance_moves.MOVE_FLIP, 5)
# # #dancer.enqueue_move(#dancer.dance_moves.MOVE_WIGGLE, 2, 2.5)
# # #dancer.enqueue_move(#dancer.dance_moves.MOVE_QUICK_BOB, 2)
#
# # #dancer.start_dancing()
#
# print('sleeping for 15 seconds then stopping')

# time.sleep(50)

time_threshold = 0.01

while True:
    # catch up
    while time_song[cluster_array_iterator] < audio.current_time() - time_threshold*2.0:
        print('here, current time %f' % audio.current_time())
        cluster_array_iterator = cluster_array_iterator + 1

    if abs(time_song[cluster_array_iterator] - audio.current_time()) < time_threshold:
        # print('cluster time:')
        # print time_song[cluster_array_iterator]/50.0
        # print('cluster label')
        print(labels[cluster_array_iterator])
        cluster_array_iterator = cluster_array_iterator + 1
        time.sleep(0.01)


#dancer.stop_dancing()

#dancer.land()

audio.stop()