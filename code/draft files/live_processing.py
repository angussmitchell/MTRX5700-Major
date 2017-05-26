import pyaudio
import sounddevice as sd
import wave
import aubio
import numpy as np

#####################################################
#       FUNCTION DEFINITIONS                        #
#####################################################

# grab a chunk function
#def get_chunk(record_s = 5,rate = 44100,chunk = 1024):
#    frames = []#
#
#    #for i in range(0, int(rate / chunk * record_s)):
#    for i in range(0,265):
#        data = stream.read(chunk)
#        frames.append(data)  # frames contains all the data#
#
#    return frames

def get_chunk(rate = 44100,chunk = 256):
    frames = sd.rec(chunk, samplerate=rate, channels=1)
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
    total_frames = 0
    is_beat = o(samples)
    if is_beat:
        return 1
    return 0


#####################################################
#       MAIN CODE                                   #
#####################################################


channels = 1
rate = 44100
chunk = 1024
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

while(1):
    frames = get_chunk()
    print(get_beats(frames.reshape(256)))


# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()
print "finished recording"

save_capture(frames = frames)

