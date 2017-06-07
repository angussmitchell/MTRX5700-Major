import pyaudio
import sounddevice as sd
import wave
import aubio
import numpy as np
from RingBuffer import HistBuffer
import matplotlib.pyplot as plt

#####################################################
#       FUNCTION DEFINITIONS                        #
#####################################################

# grab a chunk function
#def get_chunk(record_s = 5,rate = 44100,chunk = 1024):
#    frames = []#
#    #for i in range(0, int(rate / chunk * record_s)):
#    for i in range(0,265):
#        data = stream.read(chunk)
#        frames.append(data)  # frames contains all the data#
#
#    return frames

def get_chunk(rate = 44100,frame_size = 256):
    frames = sd.rec(frame_size, samplerate=rate, channels=1)
    return frames



def save_capture(frames, rate = 44100, output_filename = "file.wav",channels = 1):
    ##record song
    format = pyaudio.paInt16
    waveFile = wave.open(output_filename, 'wb')
    waveFile.setnchannels(channels)
    waveFile.setsampwidth(audio.get_sample_size(format))
    waveFile.setframerate(rate)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

def get_beats(samples, samplerate = 44100):
    # total number of frames read
    win_s = 512  # fft size
    hop_s = win_s // 2  # hop size
    o = aubio.tempo("default", win_s, hop_s, samplerate)
    is_beat = o(samples)
    if is_beat:
        return 1

    sum = np.nansum(samples)
    return sum

#a homemade sound energy implementation
def get_beats_se(samples, history, samplerate = 44100, threshold = 0, inst_threshold = 20):

    #get history
    buf = filter_array(history.data, 0,1)
    buf = filter(None, buf)   #filter out none types
    buf = np.asarray(buf)

    surrounding_pow = np.sum(abs(buf))
    instant_pow = np.sum(abs(samples))

    #see if beat detected
    if (instant_pow + threshold > surrounding_pow) & (instant_pow > inst_threshold):
        return 1

    return instant_pow


def filter_array(array, low_val,high_val):
    array = np.asarray(array)
    low_values_indices = array < low_val  # Where values are low
    high_values_indices = array > high_val
    str_values_indices = array == str
    array[low_values_indices] = 0  # All low values set to 0
    array[high_values_indices] = 0
    array[str_values_indices] = 0
    return array
#####################################################
#       MAIN CODE                                   #
#####################################################


channels = 1
rate = 44100
chunk = 256
frame_size = chunk
record_s = 5
win_s = 512                 # fft size
hop_s = win_s // 2          # hop size
format = pyaudio.paInt16
audio = pyaudio.PyAudio()

## start Recording
stream = audio.open(format=format, channels=channels,
                rate=rate, input=True,
                frames_per_buffer=chunk)

print "recording..."

#create circular history buffer
buf = HistBuffer(180,rate)                #setup RingBuf
plt.ion()

while(1):

    frames = get_chunk(frame_size = frame_size)

    buf.append(np.ndarray.tolist(frames))  #append the frames to the circular buffer (converting to list)


    #FOR PLOTTING

    # plt.clf()
    # plt.subplot(211)
    # plt.ylim([0,1])
    # toplot = np.asarray(buf.data)
    # toplot = filter(None, toplot)   #filter out none values
    # toplot = filter_array(toplot, -1,1)
    # plt.plot(toplot)
    # plt.subplot(212)
    # plt.plot(frames,'r')
    # plt.pause(0.05)

    #print
    print(get_beats_se(frames.reshape(len(frames)),history=buf))

# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()
print "finished recording"

save_capture(frames = frames)

