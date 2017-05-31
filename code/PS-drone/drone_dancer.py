import ps_drone
import time
import math


class drone_dancer:
    # time between beats in seconds
    beat_length_s = 1.0

    # moves per bpm
    bpm_scale = 1.0

    # previous offset from last beat in s
    previous_time_s = 0.0

    # current offset from last beat in s
    current_offset_s = 0.0

    # the preemptive amount of time to start motion
    movement_pre_offset_s = 0.0

    # drone move speed
    drone_move_speed_up = 0.5
    drone_move_speed_down = 1

    # drone connection
    drone = ps_drone.Drone()

    class drone_states:
        STATE_LANDED = 0
        STATE_HOVER = 1
        STATE_DANCING = 2

    drone_state = drone_states.STATE_LANDED

    # todo wiggle, circle, flip
    class dance_moves:
        MOVE_NONE = 0  # do no move
        MOVE_WIGGLE = 1  # wiggle
        MOVE_CIRCLE = 2  # circle
        MOVE_BOB = 3  # bob up/down
        MOVE_FLIP = 4  # flip

    # the current move we're doing
    current_move = dance_moves.MOVE_NONE

    # possible bob motion states
    class bob_motion:
        MOTION_NONE = 0
        MOTION_UP = 1
        MOTION_DOWN = 2

    bob_state_current = bob_motion.MOTION_NONE
    bob_state_next = bob_motion.MOTION_NONE

    # todo enum for every possible move, set move and have function for main loop that takes current offset in sec

    def __init__(self):  # , bpm = 60.0):
        self.drone.startup()
        # self.drone.reset()
        print "battery level: " + str(self.drone.getBattery()[0])
        # time.sleep(3)
        # self.drone.anim(19, 5)

        # self.drone.pwm(1, 1, 1, 1)

        # self.bpm = 60.0
        print('initialized drone dancer')

    def takeoff(self, mtrim):
        self.drone.takeoff()
        time.sleep(7.5)

        if mtrim:
            self.drone.mtrim()
            time.sleep(4)

        self.drone.hover()
        self.drone_state = self.drone_states.STATE_HOVER

    def land(self):
        self.drone_state = self.drone_states.STATE_LANDED
        self.drone.land()

    def do_move(self, move_type, duration, frequency=2.5): # todo fix sleep related errors
        self.drone_state = self.drone_states.STATE_DANCING

        if move_type == self.dance_moves.MOVE_NONE:
            self.drone_state = self.drone_states.STATE_HOVER
            self.drone.hover()
            time.sleep(duration)
        elif move_type == self.dance_moves.MOVE_FLIP:
            print('flipping!')
            self.drone.anim(18, duration)
            # self.drone.hover()

            # self.drone_state = self.drone_states.STATE_HOVER
            time.sleep(0.03)
            self.drone.hover()

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
        elif move_type == self.dance_moves.MOVE_CIRCLE:
            print('circle!')
            self.drone.turnLeft(duration)
            time.sleep(duration)

        self.drone.hover()
        self.drone_state = self.drone_states.STATE_HOVER



                # def bpm_length_s(self):
                # return self.bpm/60.0 # todo set a variable for this, allow setting of bpm or beat length

    def start_bob(self, initial_direction=bob_motion.MOTION_UP):
        # bob_state_next = initial_direction
        self.bob_state_current = initial_direction

    def bob(self):
        print('bobbing...')

        # # check if we need to change the move state
        # if self.current_offset_s > (self.beat_length_s - self.movement_pre_offset_s):
        #     print('changing movement state')
        #     if self.bob_state_current == self.bob_motion.MOTION_DOWN:
        #         self.bob_state_next = self.bob_motion.MOTION_UP
        #     elif self.bob_state_current == self.bob_motion.MOTION_UP:
        #         self.bob_state_next = self.bob_motion.MOTION_DOWN
        #     elif self.bob_state_current == self.bob_motion.MOTION_NONE:
        #         print('not changing bob state, current state is none')


        # # change the move state if we need to
        # if self.bob_state_current != self.bob_state_next:
        #     print('changing current bob state')
        #     if self.bob_state_next == self.bob_motion.MOTION_NONE:
        #         print('bob motion none')
        #         self.drone.hover()
        #     elif self.bob_state_next == self.bob_motion.MOTION_UP:
        #         print('bob motion up')
        #         self.drone.moveUp(self.drone_move_speed)
        #     elif self.bob_state_next == self.bob_motion.MOTION_DOWN:
        #         print('bob motion down')
        #         self.drone.moveDown(self.drone_move_speed)

        if self.bob_state_current == self.bob_motion.MOTION_NONE:
            print('bob motion none')
            self.drone.hover()
        elif self.bob_state_current == self.bob_motion.MOTION_UP:
            print('bob motion up')
            self.drone.moveUp(self.drone_move_speed_up)
            self.bob_state_current = self.bob_motion.MOTION_DOWN
        elif self.bob_state_current == self.bob_motion.MOTION_DOWN:
            print('bob motion down')
            # self.drone.moveDown(self.drone_move_speed_down)
            # self.drone.thrust(0, 0, 0, 0)
            self.drone.at("PWM", [1, 1, 1, 1])
            self.bob_state_current = self.bob_motion.MOTION_UP


    def dance(self, current_time_s):
        self.current_offset_s = current_time_s - self.previous_time_s
        print('[%f] ' % self.current_offset_s)

        # check if the current beat is over
        if self.current_offset_s >= self.beat_length_s:
            print('beat')
            print('setting current offset_s to 0')
            self.current_offset_s = 0  # todo this may end up skipping beats - test

        self.bob()

    def beat(self):
        self.bob()

        #
        # def chill(self):
        #     self.drone.land()
