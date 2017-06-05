import time
from drone_dancer import drone_dancer

dancer = drone_dancer()

# todo implement anim functions in drone dancer


# dancer.takeoff(True)
dancer.takeoff(True)

# dancer.drone.getConfig()
# CDC = dancer.drone.ConfigDataCount
# while CDC==dancer.drone.ConfigDataCount: time.sleep(0.001) #Wait until it is done
#
#
# print(str(dancer.drone.ConfigData))


dancer.drone.setConfig('control:indoor_control_vz_max', '2000')


# remove yaw limit
dancer.drone.setConfig('control:indoor_control_yaw', '6.11')


# dancer.drone.turnLeft(1)


# sleepytime = 0.5
#
# # for i in range(0, 8):
# #     dancer.do_move(dancer.dance_moves.MOVE_BOB_CLOCKWISE)
# #     time.sleep(sleepytime)



# anim notes - appear to try and return drone to its initial state
# 0 -
# 1 -
# 2 -
# 3 - all of these are bops
# 4 -
# 5 - this and last one are funky slides - wait for stabilisation first?
# 6 - short turn to the right
# 7 -
# 8 - yaw shake - not very noticeable, very slight movement - didnt play with duration much
# 9 - yaw dance - basically just a slower version of the above, maybe itd look good doing this then a yaw shake
# 10 - basically left right doggy wag but no control of speed
# 11 - didnt test, probably same as above but forward back
# 12 -
# 13 -
# 14 -
# 15 -

# sleep_time = 1

# CW bop
# for i in range(0, 2):
#     dancer.drone.anim(0, 1000)
#     time.sleep(sleep_time)
#     dancer.drone.anim(2, 1000)
#     time.sleep(sleep_time)
#     dancer.drone.anim(1, 1000)
#     time.sleep(sleep_time)
#     dancer.drone.anim(3, 1000)
#     time.sleep(sleep_time)

# weird slide
# for i in range(0, 2):
#     dancer.drone.anim(4, 2000)
#     time.sleep(sleep_time)
#     dancer.drone.anim(5, 2000)
#     time.sleep(sleep_time)
#
# dancer.drone.moveUp(1)
# time.sleep(0.5)
#


# dancer.drone.anim(6, 5000)
# time.sleep(0.45)
# dancer.drone.stop()
# time.sleep(2)

dancer.drone.moveUp(1)
time.sleep(0.6)

# dancer.do_move(dancer.dance_moves.MOVE_FLIP)

dancer.drone.anim(18, 15)
time.sleep(0.45)
dancer.drone.stop()
time.sleep(1)

dancer.drone.anim(19, 15)
time.sleep(0.45)
dancer.drone.stop()
time.sleep(1)

dancer.drone.anim(16, 15)
time.sleep(0.45)
dancer.drone.stop()
time.sleep(1)

dancer.drone.anim(17, 15)
time.sleep(0.45)
dancer.drone.stop()
time.sleep(1)




dancer.drone.stop()
time.sleep(1)

dancer.drone.stop()

print('landing drone...')
dancer.land()

