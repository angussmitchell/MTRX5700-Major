from play_song import play_song
import time

audio = play_song('./music/FasterFurther.wav')

audio.start()


for i in range(0, 1000):
    print('current time is %f' % audio.current_time())
    time.sleep(0.1)


audio.stop()
