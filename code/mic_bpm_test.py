import aubio
import numpy as num
import pyaudio
import time
import numpy
from Queue import Queue

# todo debug


samplerate = 44100

# PyAudio object.
p = pyaudio.PyAudio()

# Open in_stream.
in_stream = p.open(format=pyaudio.paFloat32,
    channels=2, rate=samplerate, input=True,
    frames_per_buffer=1024)

out_stream = p.open(format=pyaudio.paFloat32,
                        channels=2,
                        rate=samplerate,
                        output=True,
                        output_device_index=6,
                        frames_per_buffer=1024)

win_s = 512    # fft size - was 512

hop_s = win_s // 2  # hop size
delay = 4. * hop_s

print('delay is ' + str(delay))
beat_detection = aubio.tempo("default", win_s, hop_s, samplerate)

beat_detection.set_delay_ms(200)

beat_number = 0

start_time = time.time()
previous_time = start_time

in_chunk_number = 0
out_chunk_number = 0
beat_data = []
beat_data_samples = []
beat_data_chunks = []

prev_data = Queue()
prev_beats = Queue()

beat_data_iterator = 0

chunk_read_size = 256

# todo add a delay of 4 blocks
#
while True:

    data = in_stream.read(chunk_read_size)

    mono_data = data[1::2]

    samples = num.fromstring(mono_data,
        dtype=aubio.float_type)


    prev_data.put(data)


    current_time = time.time()

    # delay audio
    if prev_data.qsize() == delay:
        out_stream.write(prev_data.get())
        #
        # if len(beat_data) > 0 and beat_data_iterator + 1 < len(beat_data) and beat_data[beat_data_iterator] < current_time - start_time:
        #     beat_data_iterator = beat_data_iterator + 1
        #     print('beat %d' % beat_number)
        #     beat_number = beat_number + 1

        if len(beat_data_chunks) > 0:

            while beat_data_chunks[beat_data_iterator] < out_chunk_number \
                    and beat_data_iterator + 1 < len(beat_data_chunks):
                beat_data_iterator = beat_data_iterator + 1

            if beat_data_chunks[beat_data_iterator] == out_chunk_number:
                print('BEAT! %d out chunk number %d' % (beat_number, out_chunk_number))
                beat_number = beat_number + 1

            out_chunk_number = out_chunk_number + 1

        # print(prev_beats.get())
    # aubio below

    beat_array = beat_detection(samples)

    # print('beat_array detect' + str(beat_detection.get_last()))

    if in_chunk_number == 0:
        initial_aubio_sample_offset = beat_detection.get_last()

    in_chunk_number = in_chunk_number + 1

    is_beat = beat_array[0]

    if is_beat:
        current_time = time.time()

        current_bpm = beat_detection.get_bpm() #60.0/(current_time - previous_time)
        current_confidence = beat_detection.get_confidence()
        # print('BEAT %d: bpm: %f confidence: %f' % (beat_number, current_bpm, current_confidence))
        beat_number = beat_number + 1
        previous_time = current_time

        # prev_beats.put('BEAT %d: bpm: %f confidence: %f' % (beat_number, current_bpm, current_confidence))


        this_beat = int(in_chunk_number - delay + is_beat * hop_s)
        # print("%f" % (this_beat / float(samplerate)))
        # print("%d" % this_beat)
        beat_data.append(current_time - start_time + beat_detection.get_last_ms())

        # beat_data_samples.append(beat_detection.get_last() - initial_aubio_sample_offset)

        beat_data_chunks.append(in_chunk_number)

        # print('beat detected at %d' % int(beat_detection.get_last() - 2147483648))


