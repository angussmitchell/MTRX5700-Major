import time
from drone_dancer import drone_dancer

dancer = drone_dancer()


# dancer.takeoff(True)
#
# dancer.land()
#
# time.sleep(1)
#
dancer.takeoff(True)

dancer.drone.getConfig()
CDC = dancer.drone.ConfigDataCount
while CDC==dancer.drone.ConfigDataCount: time.sleep(0.001) #Wait until it is done


print(str(dancer.drone.ConfigData))


# dancer.drone.setConfig('control:control_vz_max', '2000')
dancer.drone.setConfig('control:indoor_control_vz_max', '2000')
dancer.drone.setConfig('control:indoor_control_yaw', '6.11')




sleeptime = 0.5

print('starting bop')

dancer.do_move(drone_dancer.dance_moves.MOVE_QUICK_BOB)
time.sleep(sleeptime)
# dancer.do_move(drone_dancer.dance_moves.MOVE_QUICK_BOB)
# time.sleep(sleeptime)
# dancer.do_move(drone_dancer.dance_moves.MOVE_QUICK_BOB)
# time.sleep(sleeptime)
# time.sleep(sleeptime)


time.sleep(2)




# figure 8 below
# dancer.drone.move(0.0, 0.0, 0.5, 1.0)
# time.sleep(1.1)
# dancer.drone.move(0.0, 0.0, 0.0, 1.0)
# time.sleep(0.3)
# dancer.do_move(dancer.dance_moves.MOVE_FLIP)
# dancer.drone.move(0.0, 0.0, -0.25, 1.0)
# time.sleep(2)
# dancer.drone.move(0.0, 0.0, 0.75, 1.0)
# time.sleep(1.1)
# dancer.drone.move(0.0, 0.0, 0.0, 1.0)
# time.sleep(0.3)
# dancer.drone.move(0.0, 0.0, -0.25, 1.0)
# time.sleep(2)




# dancer.drone.move(0.0, 0.0, -1.0, 0.0)
# time.sleep(0.6)
# dancer.drone.move(0.0, 0.0, 1.0, 0.0)
# time.sleep(0.6)
# dancer.drone.move(0.0, 0.0, -1.0, 0.0)
# time.sleep(0.6)
# dancer.drone.move(0.0, 0.0, 1.0, 0.0)
# time.sleep(0.6)
# dancer.drone.move(0.0, 0.0, -1.0, 0.0)
# time.sleep(0.6)
# dancer.drone.moveUp(1)
# time.sleep(0.5)
# dancer.drone.moveDown(1)
# # time.sleep(0.5)
# dancer.drone.hover()
# time.sleep(0.5)
# dancer.do_move(dancer.dance_moves.MOVE_WIGGLE, 2, 15)
# time.sleep(0.5)
# dancer.do_move(dancer.dance_moves.MOVE_FLIP, 3)
# dancer.do_move(dancer.dance_moves.MOVE_WIGGLE, 2, 5)
# dancer.do_move(dancer.dance_moves.MOVE_CIRCLE, 3)

# dancer.drone.moveRight(1)
# dancer.do_move(dancer.dance_moves.MOVE_WIGGLE_TOGGLE)
# print('before sleep')
# time.sleep(0.2)
# print('after sleep')
# dancer.do_move(dancer.dance_moves.MOVE_WIGGLE_TOGGLE)
# dancer.drone.moveLeft(1)
# time.sleep(0.2)

# dancer.do_move(dancer.dance_moves.MOVE_WIGGLE_TOGGLE)
# time.sleep(0.2)
# dancer.do_move(dancer.dance_moves.MOVE_WIGGLE_TOGGLE)
# time.sleep(0.1)
# dancer.do_move(dancer.dance_moves.MOVE_WIGGLE_TOGGLE)
# time.sleep(0.1)
# dancer.do_move(dancer.dance_moves.MOVE_WIGGLE_TOGGLE)
# time.sleep(0.1)
# dancer.do_move(dancer.dance_moves.MOVE_WIGGLE_TOGGLE)
# time.sleep(0.1)
# dancer.do_move(dancer.dance_moves.MOVE_WIGGLE_STOP)


# dancer.drone.turnAngle(359, 1)
# dancer.drone.relMove(0.0, 1.0, 0.0, 0.0, 0.0, 0.0)

# dancer.drone.anim(18, 15)
# time.sleep(0.45)

dancer.drone.stop()

# print('stopped drone')
#
# time.sleep(1)
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