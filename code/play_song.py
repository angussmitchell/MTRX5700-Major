import pyaudio
import wave
import threading
import aubio
import numpy

class play_song:
    __current_time  = 0.0   # stores current time in seconds
    __chunk_size    = 1024  # chunk size
    __chunk_number  = 0     # the current chunk we're playing
    __playing       = False # whether we're playing
    __current_bpm   = 0.0   # stores the current bpm
    __beat_times    = []
    __beat_event    = None

    def __init__(self, filename):
        self.__file = wave.open(filename, "rb")

        win_s = 512  # fft size
        hop_s = win_s // 2  # hop size
        delay = 4. * hop_s

        s = aubio.source(filename, self.__file.getframerate(), hop_s)
        samplerate = s.samplerate
        o = aubio.tempo("default", win_s, hop_s, samplerate)

        total_frames = 0
        while True:
            samples, read = s()

            is_beat = o(samples)
            if is_beat:
                this_beat = int(total_frames - delay + is_beat[0] * hop_s)
                # print("%f" % (this_beat / float(samplerate)))
                # beats.append(this_beat)
                self.__beat_times.append(this_beat / float(samplerate))
            total_frames += read
            if read < hop_s: break


    # returns the current time in seconds as a float
    def current_time(self):
        return self.__current_time

    def current_bpm(self):
        return self.__current_bpm

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

        while chunks and self.__playing:
            stream.write(chunks)



            self.__current_time = (self.__chunk_size * (self.__chunk_number) + 0.0) / self.__file.getframerate()

            if self.__beat_times[beat_time_iterator] < self.__current_time - beat_time_threshold:
                beat_time_iterator = beat_time_iterator + 1

            if abs(self.__current_time - self.__beat_times[beat_time_iterator]) < beat_time_threshold:
                # print('beat')
                if self.__beat_event and self.__current_time - last_beat_time > beat_delay_threshold:
                    print('calling beat event %d' % beat_number)
                    beat_number = beat_number + 1
                    self.__current_bpm = 60.0/(self.__current_time - last_beat_time)
                    last_beat_time = self.__current_time
                    self.__beat_event()



            self.__chunk_number = self.__chunk_number + 1
            chunks = self.__file.readframes(self.__chunk_size)



        stream.stop_stream()
        stream.close()
        pyaudio_instance.terminate()