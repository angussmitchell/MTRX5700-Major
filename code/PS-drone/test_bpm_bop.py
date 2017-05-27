import time
from drone_dancer import drone_dancer

dancer = drone_dancer()


# dancer.drone.doggyWag()
# dancer.drone.led(9, 1, 6)

# time.sleep(7.5)

# start bobbing upwards
# dancer.start_bob()
#
# for i in range(0, 4):
#     # current_time_s = i/10.0
#     # dancer.dance(current_time_s)
#     if i == 0:
#         dancer.start_bob()
#     dancer.beat()
#     time.sleep(1)


print('landing drone...')
dancer.chill()