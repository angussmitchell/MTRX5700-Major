from scipy.io.wavfile import read

a = read("Toneshifterz - Land Down Under (Bootleg).wav")

b = numpy.array(a[1],dtype=float)