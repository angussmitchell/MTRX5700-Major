### MTRX5700
# Dancing Drone
# Angus, Neill, Xue Yin
#
# main.py
#  - combines the drone preset moves module with the music processing module

import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wavfile
import time
import sys
import ps_drone         # PS-drone API
import drone_presets    # import drone functions that we wrote
from recorded_music import get_beats  #import music processing functions
import os

drone = drone_presets.clean_start()


drone.land()        #finish program, land drone