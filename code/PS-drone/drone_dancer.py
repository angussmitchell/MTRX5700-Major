import ps_drone
import time
import math
from Queue import Queue
import threading

# like Mao's last dancer, but drone version
class drone_dancer:
    # drone connection
    drone = ps_drone.Drone()

    # current move queue
    move_queue = Queue()

    # dance move class for queue
    class dance_move:
        def __init__(self, move_type = 1, duration = 1, frequency = 2):
            move_type = move_type # move type, from dance_moves class
            duration  = duration # duration in seconds
            frequency = frequency


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
        MOVE_QUICK_BOB      = 10 # single bob like in ardrone demo
        MOVE_BOB_CLOCKWISE  = 11 # automatically bobs in the next direction, forward, back, left, right

    # the current move we're doing
    current_move = dance_moves.MOVE_NONE

    # possible bob motion states
    class bob_motion:
        MOTION_NONE     = 0
        MOTION_FORWARD  = 1
        MOTION_LEFT     = 2
        MOTION_RIGHT    = 3
        MOTION_BACK     = 4

    bob_state_current   = bob_motion.MOTION_NONE

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

    # adds a move to the drone's queue
    def enqueue_move(self, move_type, duration):
        self.move_queue.put(self.dance_move(move_type, duration))

    # worker function that reads moves from the move queue and dances accordingly
    def __dance_worker(self):
        while self.dancing:
            if self.move_queue.empty():
                time.sleep(0.001) # wait a bit if we don't have any moves to do
            else:
                self.do_move(self.move_queue.get())

    # start the drone dancing at the next move in the move queue, hovers if the queue is empty
    def start_dancing(self):
        self.__dance_thread = threading.Thread(target=self.__dance_worker)
        self.__dancing = True
        self.__dance_thread.start() # start the dancer worker function
        self.__dance_thread.join()

    # stop the drone dancing when the current move is complete
    def stop_dancing(self):
        if not self.__dance_thread or self.__dance_thread.isAlive() == False:
            print('Unable to stop dancing: The drone is not currently dancing.')
        else:
            self.dancing = False

    # do_move wrapper todo just change do_move to this
    def __do_move(self, dance_move):
        self.do_move(dance_move.move_type, dance_move.duration, dance_move.frequency)

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
            self.drone.move(0.0, 0.0, 0.5, 1.0)
            time.sleep(1.1)
            self.drone.move(0.0, 0.0, 0.0, 1.0)
            time.sleep(0.3)
            self.do_move(self.dance_moves.MOVE_FLIP)
            self.drone.move(0.0, 0.0, -0.25, 1.0)
            time.sleep(2)
            self.drone.move(0.0, 0.0, 0.75, 1.0)
            time.sleep(1.1)
            self.drone.move(0.0, 0.0, 0.0, 1.0)
            time.sleep(0.3)
            self.drone.move(0.0, 0.0, -0.25, 1.0)
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

        elif move_type == self.dance_moves.MOVE_BOB_CLOCKWISE: # todo test this
            print('clockwise bob!')
            if self.bob_state_current == self.bob_motion.MOTION_LEFT \
                    or self.bob_state_current == self.bob_motion.MOTION_NONE:
                print('no bob motion, bobbing forward')
                self.drone.anim(0, 1000)
                self.bob_state_current = self.bob_motion.MOTION_FORWARD
            elif self.bob_state_current == self.bob_motion.MOTION_FORWARD:
                print('bobbed forwards last, bobbing right')
                self.drone.anim(2, 1000)
                self.bob_state_current = self.bob_motion.MOTION_RIGHT
            elif self.bob_state_current == self.bob_motion.MOTION_RIGHT:
                print('bobbed right last, bobbing back')
                self.drone.anim(1, 1000)
                self.bob_state_current = self.bob_motion.MOTION_BACK
            elif self.bob_state_current == self.bob_motion.MOTION_BACK:
                print('bobbed back last, bobbing left')
                self.drone.anim(3, 1000)
                self.bob_state_current = self.bob_motion.MOTION_LEFT

            time.sleep(0.1)
            self.chill()

    def chill(self):
        self.drone.hover()
        self.drone_state = self.drone_states.STATE_HOVER

