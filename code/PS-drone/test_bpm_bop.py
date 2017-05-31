import time
from drone_dancer import drone_dancer

dancer = drone_dancer()


dancer.takeoff(True)
#
# dancer.land()
#
# time.sleep(1)
#
# dancer.takeoff(False)

time.sleep(1)

dancer.drone.moveUp(1)
time.sleep(3.5)
dancer.drone.hover()
# time.sleep(1)
dancer.do_move(dancer.dance_moves.MOVE_WIGGLE, 1, 15)
time.sleep(0.5)
dancer.do_move(dancer.dance_moves.MOVE_FLIP, 3)
dancer.do_move(dancer.dance_moves.MOVE_CIRCLE, 3)


# dancer.drone.turnAngle(359, 1)
# dancer.drone.relMove(0.0, 1.0, 0.0, 0.0, 0.0, 0.0)

# dancer.drone.anim(18, 15)
# time.sleep(0.45)

dancer.drone.stop()

print('after move')

time.sleep(1)
# time.sleep(0.2)
#
# dancer.drone.moveUp(1)
# time.sleep(3)
# dancer.drone.hover()
# time.sleep(0.5)

print('landing drone...')
dancer.land()


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


# dancer.chill()