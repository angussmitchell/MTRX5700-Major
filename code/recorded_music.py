### MTRX5700
# Dancing Drone
# Angus, Neill, Xue Yin
#
# recorded_music.py
#  - all the music processing functions
import aubio
import numpy as np

## detect the beats in the song
def get_beats(filename, win_s, delay_b):

    samplerate = 0
    hop_s = win_s // 2          # hop size
    s = aubio.source(filename, samplerate, hop_s)
    samplerate = s.samplerate
    o = aubio.tempo("default", win_s, hop_s, samplerate)

    delay = delay_b * hop_s     # tempo detection delay (samples) for the aubio module to catch up with
    beats = []                  # list of beats (samples)
    total_frames = 0            # counter for frames read
    # look for beats
    while True:
        samples, read = s()
        is_beat = o(samples)
        if is_beat:
            this_beat = int(total_frames - delay + is_beat[0] * hop_s)
            #print("%f" % (this_beat / float(samplerate)))
            beats.append(this_beat)
        total_frames += read
        if read < hop_s: break  # end of file reached

    beats = np.asarray(beats)   #convert beats from list to array
    return samplerate, beats

### convert an array of sample indices to time in seconds
#def samples_to_seconds(samples_ind)
#
## convert beat array to time array
#beat_times = beats/float(samplerate)
##get dt array
#dt = [j-i for i, j in zip(beat_times[:-1], beat_times[1:])]
#
#    return samples_sec
