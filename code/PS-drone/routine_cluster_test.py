from drone_dancer import drone_dancer
import time
from play_song import play_song
from cluster import cluster
import scipy.io.wavfile as wavfile

beat_num = 0

flipped = False

def hook():
    global beat_num

    duration = audio.current_beat_s() - 0.01 # 10ms less than a beat

    cluster_array_iterator = int(audio.current_chunk()/10.0)

    if class_labels[cluster_array_iterator]:
        print('setting going hard')
        dancer.set_mood(dancer.dance_moods.MOOD_GO_HARD)
        dancer.auto_dance()
    else:
        print('setting chill')
        duration = audio.current_beat_s() * 4 - 0.5 # 500ms less than a beat
        dancer.set_mood(dancer.dance_moods.MOOD_CHILL)

        if beat_num % 4 == 0:
            dancer.auto_dance()

    # todo implement auto dance every x beats

    beat_num = beat_num + 1


filename = '../music/AllForNothing.wav'

rate, raw_data = wavfile.read(filename)
data = (raw_data[:,0]/2.0+raw_data[:,1]/2.0)


# get mfcc todo use cluster labels
time_song, labels, class_labels = cluster(data,samplerate=44100)

audio = play_song(filename)

dancer = drone_dancer()

# set max yaw
# dancer.drone.setConfig('control:indoor_control_yaw', '6.11')
dancer.drone.setConfig('control:control_yaw', '6.11')
CDC = dancer.drone.ConfigDataCount
while CDC == dancer.drone.ConfigDataCount: time.sleep(0.01)


dancer.takeoff(True)


print('waiting for drone to be ready')
while not dancer.ready():
    time.sleep(0.05)



print('drone ready, starting song')
audio.start()

while audio.current_time() < 0.1: # todo this may cause underrun
    time.sleep(0.001)




print('setting beat event hook')
audio.set_beat_event(hook)

dancer.start_dancing()

# print('sleeping for 15 seconds then stopping')

# time.sleep(50)

time_threshold = 0.01

time.sleep(100)

# while True:
#     # catch up
#     while time_song[cluster_array_iterator] < audio.current_time() - time_threshold*2.0:
#         print('here, current time %f' % audio.current_time())
#         cluster_array_iterator = cluster_array_iterator + 1
#
#     if abs(time_song[cluster_array_iterator] - audio.current_time()) < time_threshold:
#         print('cluster time:')
#         print time_song[cluster_array_iterator]
#         print('cluster label')
#         print(labels[cluster_array_iterator])
#         cluster_array_iterator = cluster_array_iterator + 1
#         time.sleep(0.01)


dancer.stop_dancing()

dancer.land()

audio.stop()