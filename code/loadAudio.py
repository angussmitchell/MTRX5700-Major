import scipy.io.wavfile as wavfile
import numpy as np
import matplotlib.pyplot as plt

rate, raw_data = wavfile.read("music/rome.wav")

windowSize = 120             # 2 minutes
window = rate*windowSize     #how many samples we need to get a window

plt.plot(raw_data[0:window],'r')
plt.ylabel('amplitude')
plt.xlabel('sample No.')
plt.title('raw .WAV data')
plt.axis([0, 6000000, -60000, 60000])
plt.show()
print('hello world')