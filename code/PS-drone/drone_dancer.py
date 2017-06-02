import ps_drone
import time
import math

# like Mao's last dancer, but drone version
class drone_dancer:
    # drone connection
    drone = ps_drone.Drone()

    # not sure if we need this - code is sequential anyway but I'll leave it in for now
    class drone_states:
        STATE_LANDED    = 0
        STATE_HOVER     = 1
        STATE_DANCING   = 2

    drone_state = drone_states.STATE_LANDED

    # todo wiggle, circle, flip
    class dance_moves:
        MOVE_NONE           = 0  # do no move
        MOVE_WIGGLE         = 1  # wiggle
        MOVE_WIGGLE_TOGGLE  = 2  # toggle wiggle, initially right, then left, then through the 4th dimension
        MOVE_WIGGLE_STOP    = 3  # stops wiggling
        MOVE_CIRCLE         = 4  # circle
        MOVE_BOB            = 5  # bob up/down
        MOVE_FLIP           = 6  # flip
        MOVE_FIGURE_EIGHT   = 7  # figure 8 on horizontal plane
        MOVE_SPIRAL_UP      = 8  # todo spiral up
        MOVE_SPIRAL_DOWN    = 9  # todo spiral down
        MOVE_QUICK_BOB      = 10 # todo single bob like in ardrone demo

    # the current move we're doing
    current_move = dance_moves.MOVE_NONE

    # possible bob motion states
    class bob_motion:
        MOTION_NONE     = 0
        MOTION_UP       = 1
        MOTION_DOWN     = 2

    bob_state_current   = bob_motion.MOTION_NONE
    bob_state_next      = bob_motion.MOTION_NONE

    # the possible wiggle motions
    class wiggle_motion:
        WIGGLE_NONE     = 0
        WIGGLE_LEFT     = 1
        WIGGLE_RIGHT    = 2

    wiggle_motion_current = wiggle_motion.WIGGLE_NONE

    def __init__(self):
        self.drone.startup()
        self.drone.reset()
        print("battery level: " + str(self.drone.getBattery()[0]) + '%')
        print('initialized drone dancer')

    # 3 2 1 liftoff
    def takeoff(self, mtrim):
        self.drone.takeoff()
        time.sleep(7.5)

        if mtrim:
            self.drone.mtrim()
            time.sleep(4)

        self.drone.hover()
        self.drone_state = self.drone_states.STATE_HOVER

    # lands the drone
    def land(self):
        self.drone_state = self.drone_states.STATE_LANDED
        self.drone.land()

    # bust a move! # todo currently no way to set speed, only duration - you can use ps drone setspeed for now
    def do_move(self, move_type, duration=1, frequency=2.5):  # todo fix sleep related errors
        self.drone_state = self.drone_states.STATE_DANCING

        if move_type == self.dance_moves.MOVE_NONE:
            self.drone_state = self.drone_states.STATE_HOVER
            self.drone.hover()
            time.sleep(duration)

        elif move_type == self.dance_moves.MOVE_FLIP:
            print('flipping!')
            self.drone.anim(18, 15)
            time.sleep(0.45)
            self.drone.stop()

            if (duration < 0.45):
                time.sleep(0.45 - duration)
            elif duration > 0.45:
                time.sleep(duration - 0.45)
            self.drone.stop()

        elif move_type == self.dance_moves.MOVE_WIGGLE:
            print('wiggling!')
            for i in range(0, int(math.ceil(duration * frequency)), 1):
                if i % 2:
                    print('wiggle left')
                    self.drone.moveLeft(1)
                else:
                    print('wiggle right')
                    self.drone.moveRight(1)

                time.sleep((duration + 0.0) / frequency)
            self.drone.stop()

        elif move_type == self.dance_moves.MOVE_WIGGLE_TOGGLE:
            print('toggling wiggle ma niggle')
            if self.wiggle_motion_current == self.wiggle_motion.WIGGLE_NONE:
                print('wiggle none, wiggling right...')
                self.wiggle_motion_current = self.wiggle_motion.WIGGLE_RIGHT
                self.drone.moveRight(1)
            elif self.wiggle_motion_current == self.wiggle_motion.WIGGLE_LEFT:
                print('wiggle left, wiggling right...')
                self.wiggle_motion_current = self.wiggle_motion.WIGGLE_RIGHT
                self.drone.moveRight(1)
            elif self.wiggle_motion_current == self.wiggle_motion.WIGGLE_RIGHT:
                print('wiggle right, wiggling left...')
                self.wiggle_motion_current = self.wiggle_motion.WIGGLE_LEFT
                self.drone.moveLeft(1)

        elif move_type == self.dance_moves.MOVE_WIGGLE_STOP:
            print('stopping wiggling ma niggling')
            self.wiggle_motion_current = self.wiggle_motion.WIGGLE_NONE
            self.chill()

        elif move_type == self.dance_moves.MOVE_CIRCLE:
            print('circle!')
            self.drone.turnLeft(duration, 1.2)
            time.sleep(duration)
            self.chill()
        elif move_type == self.dance_moves.MOVE_FIGURE_EIGHT:
            print('figure 8!')
            dancer.drone.move(0.0, 0.0, 0.5, 1.0)
            time.sleep(1.1)
            dancer.drone.move(0.0, 0.0, 0.0, 1.0)
            time.sleep(0.3)
            dancer.do_move(dancer.dance_moves.MOVE_FLIP)
            dancer.drone.move(0.0, 0.0, -0.25, 1.0)
            time.sleep(2)
            dancer.drone.move(0.0, 0.0, 0.75, 1.0)
            time.sleep(1.1)
            dancer.drone.move(0.0, 0.0, 0.0, 1.0)
            time.sleep(0.3)
            dancer.drone.move(0.0, 0.0, -0.25, 1.0)
            time.sleep(2)
            self.chill()

        elif move_type == self.dance_moves.MOVE_QUICK_BOB:
            print('quick bob!')
            # self.drone.moveForward(1)
            #2.0943952e-01 default
            self.drone.setConfig('control:euler_angle_max', '2')
            nod_time = 0.1
            # hover_time = 0.1
            self.drone.moveForward(1)
            # self.drone.move(0.0, 1.0, 0.0, 0.0)
            time.sleep(nod_time)
            self.drone.moveBackward(1)
            # self.drone.move(0.0, -1.0, 0.0, 0.0)
            time.sleep(nod_time)
            # self.drone.stop()
            # time.sleep(hover_time)
            self.drone.setConfig('control:euler_angle_max', '0.21')
            self.chill()


    def chill(self):
        self.drone.hover()
        self.drone_state = self.drone_states.STATE_HOVER

