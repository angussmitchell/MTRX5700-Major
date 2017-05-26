import time
from drone_dancer import drone_dancer

dancer = drone_dancer()

# start bobbing upwards
# dancer.start_bob()

for i in range(0, 10):
    # current_time_s = i/10.0
    # dancer.dance(current_time_s)
    if i == 0:
        dancer.start_bob()
    dancer.beat()
    time.sleep(1)

print('landing drone...')
dancer.chill()