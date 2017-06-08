from play_song import play_song
import time
#


def beat_hook():
    print('meat hook')

audio = play_song('./music/AllForNothing.wav')

audio.start()


audio.set_beat_event(beat_hook)

# for i in range(0, 100):
#     # print('current time is %f' % audio.current_time())
#     print('bpm is %f' % audio.current_bpm())
#     time.sleep(0.1)

time.sleep(100)


audio.stop()
#
#
# import pyaudio
# p = pyaudio.PyAudio()
# info = p.get_host_api_info_by_index(0)
# numdevices = info.get('deviceCount')
# for i in range(0, numdevices):
#         if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
#             print "Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name')