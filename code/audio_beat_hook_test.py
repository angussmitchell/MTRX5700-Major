from play_song import play_song
import time

def hook():
    print('beat here')


audio = play_song('./music/RumbleInTheJungle.wav')



audio.set_beat_event(hook)

audio.start()

time.sleep(10)

audio.stop()