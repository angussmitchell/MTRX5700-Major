import scipy.io.wavfile as wavfile
import numpy

# a = read("Toneshifterz - Land Down Under (Bootleg).wav")
# b = numpy.array(a[1])

rate,data = wavfile.read("k1h_1277_335480_20151029_205514_30_0.wav")
data[:5]

print('hellooo')