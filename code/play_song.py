import pyaudio
import wave
import threading
import aubio
import numpy
from cluster import cluster
import scipy.io.wavfile as wavfile

# todo if bpm not confident use onset

class play_song:
    __current_time   = 0.0   # stores current time in seconds
    __chunk_size     = 1024  # chunk size todo can't change this cos of chunk chorus
    __chunk_number   = 0     # the current chunk we're playing
    __playing        = False # whether we're playing
    __current_bpm    = 0.0   # stores the current bpm
    __beat_times     = []
    __beat_event     = None
    __onset_event    = None
    __chunk_is_beat  = None
    __chunk_is_onset = None
    __chunk_bpm      = None
    __chunk_bpm_confidence = None
    __current_confidence = 0 # aubio's confidence of the current bpm
    __chunk_chorus = None
    __bpm_confidence_threshold = 0.1 # required aubio bpm confidence to use beat function rather than onset function

    # TODO ONSET threshold

    onsets          = []

    def __init__(self, filename, skip_bpm_detection_time=0.0):

        # cluster analysis
        rate, raw_data = wavfile.read(filename)
        data = (raw_data[:, 0] / 2.0 + raw_data[:, 1] / 2.0)

        # get mfcc
        time_song, labels, class_labels = cluster(data, samplerate=44100)


        self.__chunk_chorus = numpy.zeros(len(raw_data)/self.__chunk_size)

        previous_chunk_number = 0
        for i in range(0, 10*len(class_labels), 10):
            self.__chunk_chorus[previous_chunk_number: i] = class_labels[i/10]
            previous_chunk_number = i

        # aubio stuff
        self.__file = wave.open(filename, "rb")

        win_s = 512  # fft size
        hop_s = win_s // 2  # hop size
        delay = 4. * hop_s

        s = aubio.source(filename, self.__file.getframerate(), hop_s)
        samplerate = s.samplerate
        o = aubio.tempo("default", win_s, hop_s, samplerate)

        onset = aubio.onset("default", win_s, hop_s, samplerate)

        num_chunks = s.duration / self.__chunk_size
        self.__chunk_is_beat = numpy.zeros(num_chunks)
        self.__chunk_is_onset = numpy.zeros(num_chunks)
        self.__chunk_bpm = numpy.zeros(num_chunks, dtype=float)
        self.__chunk_bpm_confidence = numpy.zeros(num_chunks, dtype=float)

        o.set_delay(100)
        total_frames = 0

        while True:
            samples, read = s()

            # onset detection
            last_beat_chunk_number = 0
            beat_number = 0

            os = onset(samples)
            if os:
                this_beat = int(total_frames - delay + os[0] * hop_s)
                self.onsets.append(onset.get_last() / float(samplerate))
                current_beat_time_s = this_beat / float(samplerate)
                current_chunk_number = int((current_beat_time_s * samplerate)/self.__chunk_size)
                self.__chunk_is_onset[current_chunk_number] = 1


          #  if skip_bpm_detection_time > total_frames /  # todo current time
            is_beat = o(samples)
            if is_beat:
                this_beat = int(total_frames - delay + is_beat[0] * hop_s)
                # print("%f" % (this_beat / float(samplerate)))
                # beats.append(this_beat)
                current_beat_time_s = this_beat / float(samplerate)
                self.__beat_times.append(current_beat_time_s)

                current_chunk_number = int((current_beat_time_s * samplerate)/self.__chunk_size)
                self.__chunk_is_beat[current_chunk_number] = 1

                if beat_number == 0:
                    last_beat_chunk_number = current_chunk_number

                self.__chunk_bpm[last_beat_chunk_number:current_chunk_number] = o.get_bpm()

                self.__chunk_bpm_confidence[last_beat_chunk_number:current_chunk_number] = o.get_confidence()

                last_beat_chunk_number = current_chunk_number

                beat_number = beat_number + 1

            total_frames += read
            if read < hop_s: break


    # returns the current time in seconds as a float
    def current_time(self):
        return self.__current_time

    def current_chunk(self):
        return self.__chunk_number

    def current_bpm(self):
        # return self.__current_bpm
        return self.__chunk_bpm[self.__chunk_number]

    def current_bpm_confidence(self):
        return self.__chunk_bpm_confidence[self.__chunk_number]

    # returns a true or false value indicating whether it's a chorus
    def is_chorus(self):
        return self.__chunk_chorus[self.__chunk_number]

    def current_beat_s(self):
        if self.__current_bpm:
            return 60.0/self.__current_bpm
        else:
            return 0.3

    # begins playing audio asynchronously
    def start(self):
        self.__audio_thread = threading.Thread(target=self.__audio_worker)
        self.__playing = True
        self.__audio_thread.start()

    # stops playing audio
    def stop(self):
        self.__playing = False
        self.__audio_thread.join()
        print('Stopped playing audio')

    def set_beat_event(self, beat_event_function):
        self.__beat_event = beat_event_function

    def set_onset_event(self, onset_event_function):
        self.__onset_event = onset_event_function

    # worker for playing audio in a thread
    def __audio_worker(self):
        pyaudio_instance = pyaudio.PyAudio()
        stream = pyaudio_instance.open(format=pyaudio_instance.get_format_from_width(self.__file.getsampwidth()),
                        channels=self.__file.getnchannels(),
                        rate=self.__file.getframerate(),
                        output=True)


        chunks = self.__file.readframes(self.__chunk_size)

        beat_time_threshold = 0.05
        beat_delay_threshold = 0.1
        beat_time_iterator = 0
        last_beat_time = 0

        beat_number = 0
        onset_number = 0


        win_s = 512  # fft size
        hop_s = win_s // 2  # hop size
        samplerate = self.__file.getframerate()

        o = aubio.tempo("default", win_s, hop_s, samplerate)



        while chunks and self.__playing:
            stream.write(chunks)


            self.__current_time = (self.__chunk_size * (self.__chunk_number) + 0.0) / self.__file.getframerate()

            # todo fire beat event

            if self.__chunk_is_beat[self.__chunk_number] and self.__chunk_bpm_confidence[self.__chunk_number] >= self.__bpm_confidence_threshold:
                # print('beat! %d' % beat_number)
                beat_number = beat_number + 1
                if self.__beat_event:
                    self.__beat_event()

            if self.__chunk_is_onset[self.__chunk_number] and self.__chunk_bpm_confidence[self.__chunk_number] < self.__bpm_confidence_threshold:
                # print('onset! %d' % onset_number)
                if self.__onset_event:
                    self.__onset_event()



            #
            # if self.__beat_times[beat_time_iterator] < self.__current_time - beat_time_threshold:
            #     beat_time_iterator = beat_time_iterator + 1
            #
            # if abs(self.__current_time - self.__beat_times[beat_time_iterator]) < beat_time_threshold:
            #     # print('beat')
            #     if self.__beat_event and self.__current_time - last_beat_time > beat_delay_threshold:
            #         print('calling beat event %d' % beat_number)
            #         beat_number = beat_number + 1
            #         self.__current_bpm = 60.0/(self.__current_time - last_beat_time)
            #         last_beat_time = self.__current_time
            #         self.__beat_event()



            self.__chunk_number = self.__chunk_number + 1
            chunks = self.__file.readframes(self.__chunk_size)



        stream.stop_stream()
        stream.close()
        pyaudio_instance.terminate()