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
        self.__audio_thread.join()
        print('Stopped playing audio')

    # worker for playing audio in a thread
    def __audio_worker(self):
        pyaudio_instance = pyaudio.PyAudio()
        stream = pyaudio_instance.open(format=pyaudio_instance.get_format_from_width(self.__file.getsampwidth()),
                        channels=self.__file.getnchannels(),
                        rate=self.__file.getframerate(),
                        output=True)
        chunks = self.__file.readframes(self.__chunk_size)

        while chunks and self.__playing:
            stream.write(chunks)
            self.__current_time = (self.__chunk_size * (self.__chunk_number) + 0.0) / self.__file.getframerate()
            self.__chunk_number = self.__chunk_number + 1
            chunks = self.__file.readframes(self.__chunk_size)


        stream.stop_stream()
        stream.close()
        pyaudio_instance.terminate()