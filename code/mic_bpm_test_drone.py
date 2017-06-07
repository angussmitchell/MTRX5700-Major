import aubio
import numpy as num
import pyaudio
import time
from drone_dancer import drone_dancer

# todo debug


samplerate = 44100

# PyAudio object.
p = pyaudio.PyAudio()



win_s = 128    # fft size - was 512

hop_s = win_s // 2  # hop size
beat_detection = aubio.tempo("default", win_s, hop_s, samplerate)

beat_detection.set_delay_ms(500)

beat_number = 0

previous_time = time.time()


# todo add a delay



dancer = drone_dancer()

dancer.takeoff(True)



def hook():
    dancer.enqueue_move(dancer.dance_moves.MOVE_BOB_CLOCKWISE, 0.15)



# Open stream.
stream = p.open(format=pyaudio.paFloat32,
    channels=1, rate=samplerate, input=True,
    frames_per_buffer=1024)

while True:

    data = stream.read(64)
    samples = num.fromstring(data,
        dtype=aubio.float_type)


    beat_array = beat_detection(samples)
    is_beat = beat_array[0]

    if is_beat:
        current_time = time.time()
        current_bpm = beat_detection.get_bpm() #60.0/(current_time - previous_time)
        current_confidence = beat_detection.get_confidence()
        print('BEAT %d: bpm: %f confidence: %f' % (beat_number, current_bpm, current_confidence))
        if current_confidence > 0.03:
            dancer.start_dancing()
            hook()
        else:
            dancer.stop_dancing()
        beat_number = beat_number + 1
        previous_time = current_time

        if beat_number == 50:
            break


# time.sleep(30)
dancer.stop_dancing()
dancer.land()