import pyaudio
import numpy as np
import pylab
import wave
import time


wf = wave.open('../music/5783146_All_For_Nothing_Extended_Version.wav', 'rb')


def soundplot(stream):
    t1 = time.time()
    data = np.fromstring(stream.read(CHUNK), dtype=np.int16)
    pylab.plot(data)
    pylab.title(i)
    pylab.grid()
    pylab.axis([0, len(data), -2 ** 16 / 2, 2 ** 16 / 2])
    pylab.savefig("03.png", dpi=50)
    pylab.close('all')
    print("took %.02f ms" % ((time.time() - t1) * 1000))




RATE = wf.getframerate()
CHUNK = int(RATE / 20)  # RATE / number of updates per second

if __name__ == "__main__":
    p = pyaudio.PyAudio()
    # stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True,
    #                 frames_per_buffer=CHUNK)
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    frames_per_buffer=CHUNK)

    # for i in range(int(20 * RATE / CHUNK)):  # do this for 10 seconds
        # soundplot(stream)
    stream.stop_stream()
    stream.close()
    p.terminate()
