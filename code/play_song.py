import pyaudio
import wave
import threading

class play_song:
    __current_time  = 0.0 # stores current time in seconds
    __chunk_size    = 1024 # chunk size
    __chunk_number  = 0 # the current chunk we're playing
    __playing       = False # whether we're playing

    def __init__(self, filename):
        self.__file = wave.open(filename, "rb")
        self.__pyaudio = pyaudio.PyAudio()
        self.__stream = self.__pyaudio.open(format=self.__pyaudio.get_format_from_width(self.__file.getsampwidth()),
                        channels=self.__file.getnchannels(),
                        rate=self.__file.getframerate(),
                        output=True)
        self.__chunks = self.__file.readframes(self.__chunk_size)

    # returns the current time in seconds as a float
    def current_time(self):
        return self.__current_time

    # begins playing audio asynchronously
    def start(self):
        self.__audio_thread = threading.Thread(target=self.__audio_worker)
        self.__playing = True
        self.__audio_thread.start()

    # stops playing audio
    def stop(self):
        self.__playing = False
        self.__stream.stop_stream()
        self.__stream.close()
        self.__pyaudio.terminate()
        self.__audio_thread.join()
        print('Stopped playing audio')

    # worker for playing audio in a thread
    def __audio_worker(self):
        while self.__chunks and self.__playing:
            self.__stream.write(self.__chunks)
            self.__current_time = (self.__chunk_size * (self.__chunk_number) + 0.0) / self.__file.getframerate()
            self.__chunk_number = self.__chunk_number + 1
            self.__chunks = self.__file.readframes(self.__chunk_size)