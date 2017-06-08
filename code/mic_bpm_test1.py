import aubio
import numpy as num
import pyaudio
import time

# todo debug


samplerate = 44100

# PyAudio object.
p = pyaudio.PyAudio()

# Open stream.
stream = p.open(format=pyaudio.paFloat32,
    channels=1, rate=samplerate, input=True,
    frames_per_buffer=1024)


win_s = 128    # fft size - was 512

hop_s = win_s // 2  # hop size
beat_detection = aubio.tempo("default", win_s, hop_s, samplerate)

beat_detection.set_delay_ms(200)

beat_number = 0

previous_time = time.time()


# todo add a delay





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
        beat_number = beat_number + 1
        previous_time = current_time