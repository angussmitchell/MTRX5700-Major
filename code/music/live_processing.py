import pyaudio
import wave

#####################################################
#       FUNCTION DEFINITIONS                        #
#####################################################

# grab a chunk function
def get_chunk(record_s = 5,rate = 44100,chunk = 1024):
    frames = []

    for i in range(0, int(rate / chunk * record_s)):
        data = stream.read(chunk)
        frames.append(data)  # frames contains all the data

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


#####################################################
#       MAIN CODE                                   #
#####################################################


channels = 1
rate = 44100
chunk = 1024
record_s = 5
format = pyaudio.paInt16
audio = pyaudio.PyAudio()

## start Recording
stream = audio.open(format=format, channels=channels,
                rate=rate, input=True,
                frames_per_buffer=chunk)
print "recording..."

frames = get_chunk()

# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()
print "finished recording"

save_capture(frames = frames)

