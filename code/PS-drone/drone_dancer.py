import ps_drone

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
    drone_move_speed = 0.25

    # drone connection
    # drone = ps_drone.Drone()

    # todo wiggle, circle, flip
    class dance_moves:
        MOVE_NONE   = 0 # do no move
        MOVE_WIGGLE = 1 # wiggle
        MOVE_CIRCLE = 2 # circle
        MOVE_BOB    = 3 # bob up/down
        MOVE_FLIP   = 4 # flip

    # the current move we're doing
    current_move = dance_moves.MOVE_NONE

    # possible bob motion states
    class bob_motion:
        MOTION_NONE = 0
        MOTION_UP   = 1
        MOTION_DOWN = 2

    bob_state_current   = bob_motion.MOTION_NONE
    bob_state_next      = bob_motion.MOTION_NONE

    # todo enum for every possible move, set move and have function for main loop that takes current offset in sec

    def __init__(self): #, bpm = 60.0):
        self.drone = ps_drone.Drone()
        # self.bpm = 60.0
        print('initialized drone dancer')

    # def bpm_length_s(self):
        # return self.bpm/60.0 # todo set a variable for this, allow setting of bpm or beat length

    def start_bob(self, initial_direction = bob_motion.MOTION_UP):
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
            self.drone.moveUp(0.25)#self.drone_move_speed)
            self.bob_state_current = self.bob_motion.MOTION_DOWN
        elif self.bob_state_current == self.bob_motion.MOTION_DOWN:
            print('bob motion down')
            self.drone.moveDown(0.25)#self.drone_move_speed)
            self.bob_state_current = self.bob_motion.MOTION_UP


    def dance(self, current_time_s):
        self.current_offset_s = current_time_s - self.previous_time_s
        print('[%f] ' % self.current_offset_s)


        # check if the current beat is over
        if self.current_offset_s >= self.beat_length_s:
            print('beat')
            print('setting current offset_s to 0')
            self.current_offset_s = 0 # todo this may end up skipping beats - test

        self.bob()

    def beat(self):
        self.bob()


    def chill(self):
        self.drone.land()