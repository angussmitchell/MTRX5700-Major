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

        elif move_type == self.dance_moves.MOVE_WIGGLE_TOGGLE:
            print('toggling wiggle ma niggle')
            if self.wiggle_motion_current == self.wiggle_motion.WIGGLE_NONE:
                print('wiggle none, wiggling right...')
                self.drone.moveRight(1)
                self.wiggle_motion_current = self.wiggle_motion.WIGGLE_RIGHT
            if self.wiggle_motion_current == self.wiggle_motion.WIGGLE_LEFT:
                print('wiggle left, wiggling right...')
                self.drone.moveRight(1)
                self.wiggle_motion_current = self.wiggle_motion.WIGGLE_RIGHT
            if self.wiggle_motion_current == self.wiggle_motion.WIGGLE_RIGHT:
                print('wiggle right, wiggling left...')
                self.drone.moveLeft(1)
                self.wiggle_motion_current = self.wiggle_motion.WIGGLE_LEFT

        elif move_type == self.dance_moves.MOVE_WIGGLE_STOP:
            print('stopping wiggling ma niggling')
            self.wiggle_motion_current = self.wiggle_motion.WIGGLE_NONE
            self.drone.stop()

        elif move_type == self.dance_moves.MOVE_CIRCLE:
            print('circle!')
            self.drone.turnLeft(duration, 1.2)
            time.sleep(duration)
        elif move_type == self.dance_moves.MOVE_FIGURE_EIGHT:
            print('figure 8!')
            self.drone.turnLeft(duration, 1.2)
            time.sleep(duration)
            self.drone.turnRight(duration, 1.2)
            time.sleep(duration)

        self.drone.hover()
        self.drone_state = self.drone_states.STATE_HOVER

    # todo put in dance function
    #
    # def start_bob(self, initial_direction=bob_motion.MOTION_UP):
    #     # bob_state_next = initial_direction
    #     self.bob_state_current = initial_direction
    #
    # def bob(self):
    #     print('bobbing...')
    #
    #     # # check if we need to change the move state
    #     # if self.current_offset_s > (self.beat_length_s - self.movement_pre_offset_s):
    #     #     print('changing movement state')
    #     #     if self.bob_state_current == self.bob_motion.MOTION_DOWN:
    #     #         self.bob_state_next = self.bob_motion.MOTION_UP
    #     #     elif self.bob_state_current == self.bob_motion.MOTION_UP:
    #     #         self.bob_state_next = self.bob_motion.MOTION_DOWN
    #     #     elif self.bob_state_current == self.bob_motion.MOTION_NONE:
    #     #         print('not changing bob state, current state is none')
    #
    #
    #     # # change the move state if we need to
    #     # if self.bob_state_current != self.bob_state_next:
    #     #     print('changing current bob state')
    #     #     if self.bob_state_next == self.bob_motion.MOTION_NONE:
    #     #         print('bob motion none')
    #     #         self.drone.hover()
    #     #     elif self.bob_state_next == self.bob_motion.MOTION_UP:
    #     #         print('bob motion up')
    #     #         self.drone.moveUp(self.drone_move_speed)
    #     #     elif self.bob_state_next == self.bob_motion.MOTION_DOWN:
    #     #         print('bob motion down')
    #     #         self.drone.moveDown(self.drone_move_speed)
    #
    #     if self.bob_state_current == self.bob_motion.MOTION_NONE:
    #         print('bob motion none')
    #         self.drone.hover()
    #
    #     elif self.bob_state_current == self.bob_motion.MOTION_UP:
    #         print('bob motion up')
    #         self.drone.moveUp(self.drone_move_speed_up)
    #         self.bob_state_current = self.bob_motion.MOTION_DOWN
    #
    #     elif self.bob_state_current == self.bob_motion.MOTION_DOWN:
    #         print('bob motion down')
    #         # self.drone.moveDown(self.drone_move_speed_down)
    #         # self.drone.thrust(0, 0, 0, 0)
    #         self.drone.at("PWM", [1, 1, 1, 1])
    #         self.bob_state_current = self.bob_motion.MOTION_UP

