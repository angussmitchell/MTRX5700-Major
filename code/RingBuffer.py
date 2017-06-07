class HistBuffer:
    def __init__(self,maxBPM,rate):
        maxBPM = 180  # set maxBPM
        maxSamples = ((maxBPM / 60) * rate) / 10  # set max samples
        maxSamples = (maxSamples / 256) * 256  # round max sampels, so 256 buffers fit in perfectly
        size = maxSamples
        self.data = [None for i in xrange(size)]

    def append(self, x):
        self.data = self.data[256:] #get rid of the first 256 elements
        self.data = self.data + x   #add on the next 256 elements


    def get(self):
        return self.data
