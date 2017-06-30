import ps_drone
import time
import math
from Queue import Queue
import threading
import boots
import numpy as np


# TODO battery check before flips

# like Mao's last dancer, but drone version
class drone_dancer:
    # drone connection
    drone = ps_drone.Drone()

    # current move queue
    move_queue = Queue()

    test_mode = False

    __dance_thread = None
    __retrieving_navdata = False
    __navdata_thread = None

    # dance move class for queue
    class dance_move:
        def __init__(self, move_type=1, duration=1.0, frequency=2.0, delay=0.0):
            self.move_type = move_type  # move type, from dance_moves class
            self.duration = duration  # duration in seconds
            self.frequency = frequency
            self.delay = 0.0

    class dance_moods:
        MOOD_CHILL = 0
        MOOD_GO_HARD = 1

    __current_dance_mood = dance_moods.MOOD_GO_HARD

    # stores the current beat count for move determination, e.g. every 8 beats change dance style
    __current_beat_count = 0

    # not sure if we need this - code is sequential anyway but I'll leave it in for now
    class drone_states:
        STATE_LANDED = 0
        STATE_CALIBRATING = 1
        STATE_HOVER = 2
        STATE_DANCING = 3

    drone_state = drone_states.STATE_LANDED

    # todo wiggle, circle, flip
    class dance_moves:
        MOVE_NONE = 0  # do no move
        MOVE_WIGGLE = 1  # wiggle
        MOVE_WIGGLE_TOGGLE = 2  # toggle wiggle, initially right, then left, then through the 4th dimension
        MOVE_WIGGLE_STOP = 3  # stops wiggling
        MOVE_CIRCLE = 4  # circle
        MOVE_BOB = 5  # bob up/down
        MOVE_FLIP = 6  # flip
        MOVE_FIGURE_EIGHT = 7  # figure 8 on horizontal plane
        MOVE_SPIRAL_UP = 8  # todo spiral up
        MOVE_SPIRAL_DOWN = 9  # todo spiral down
        MOVE_QUICK_BOB = 10  # single bob like in ardrone demo
        MOVE_BOB_CLOCKWISE = 11  # automatically bobs in the next direction, forward, back, left, right
        MOVE_BOB_FBLR = 12  # front back left right bob
        MOVE_BOB_FB = 13  # bobs back and forward
        MOVE_BOX_LFRB = 14  # moves in a box, left -> forwards -> right -> back
        MOVE_BOX_WITH_BOB = 15  # todo box with bob in opposite direction to where we're going next
        MOVE_HEIGHT_CHANGE = 16
        MOVE_SPIN_CLOCKWISE = 17
        MOVE_SPIN_CLOCKWISE_UP = 18
        MOVE_SPIN_ALTERNATE = 19

    # the current move we're doing
    current_move = dance_moves.MOVE_NONE

    # possible spin states
    class spin_motion:
        MOTION_NONE = 0
        MOTION_CW = 1
        MOTION_CCW = 2

    __current_spin_direction = spin_motion.MOTION_NONE

    # possible box motion states
    class box_motion:
        MOTION_NONE = 0
        MOTION_FORWARD = 1
        MOTION_LEFT = 2
        MOTION_RIGHT = 3
        MOTION_BACK = 4

    __current_box_motion = box_motion.MOTION_NONE

    # possible bob motion states
    class bob_motion:
        MOTION_NONE = 0
        MOTION_FORWARD = 1
        MOTION_LEFT = 2
        MOTION_RIGHT = 3
        MOTION_BACK = 4

    bob_state_current = bob_motion.MOTION_NONE

    # the possible wiggle motions
    class wiggle_motion:
        WIGGLE_NONE = 0
        WIGGLE_LEFT = 1
        WIGGLE_RIGHT = 2

    wiggle_motion_current = wiggle_motion.WIGGLE_NONE

    def __init__(self):
        self.drone.startup()
        self.drone.reset()
        while (self.drone.getBattery()[0] == -1):  time.sleep(0.1)  # Wait until the drone has done its reset
        self.drone.useDemoMode(False)
        self.drone.getNDpackage(
            ["demo", "time", "altitude", "magneto", "vision_detect"])  # Packets, which shall be decoded
        time.sleep(1.5)
        print("battery level: " + str(self.drone.getBattery()[0]) + '%')
        print('initialized drone dancer')

        CDC = self.drone.ConfigDataCount
        self.drone.setConfig("control:altitude_max", "1500")  # Request change of an option
        self.drone.setConfig("control:control_yaw", "6.11")

        ## set up vision detection
        # Shell-Tag=1, Roundel=2, Black Roundel=4, Stripe=8, Cap=16, Shell-Tag V2=32, Tower Side=64, Oriented Roundel=128
        self.drone.setConfig("detect:detect_type", "5")
        self.drone.setConfig("detect:detections_select_v", "128")  # oriented roundel with ground camera

        while CDC == self.drone.ConfigDataCount:     time.sleep(0.001)  # Wait until configuration has been
        # set (after resync is done)

        time.sleep(2.0)  # Give it some time to awake fully

        self.drone.trim()  # Recalibrate sensors
        self.drone.getSelfRotation(5)  # Auto-alteration-value of gyroscope-sensor
        print "Auto-alternation: " + str(self.drone.selfRotation) + "deg/sec"

        # check what data packages are being sent/received
        if self.drone.State[10] == 0:
            print "Navdata: all"
        else:
            print "Navdata: demo. dumb drone"
            self.drone.useDemoMode(False)
            time.sleep(2.0)

        self.__dancing = False
        print('drone init complete')

    # 3 2 1 liftoff
    def takeoff(self, mtrim):
        self.drone.takeoff()
        self.drone_state = self.drone_states.STATE_CALIBRATING
        time.sleep(7.5)

        if mtrim:
            self.drone.mtrim()
            time.sleep(4)

        self.start_getting_navdata()
        self.drone.hover()
        self.drone_state = self.drone_states.STATE_HOVER

    # lands the drone
    def land(self):
        self.stop_dancing()
        self.stop_getting_navdata()
        self.drone_state = self.drone_states.STATE_LANDED
        self.drone.land()

    __current_auto_dance_move = dance_moves.MOVE_BOB_FB

    # should be called on the beat, automatically selects a dance move, drone should be dancing
    def auto_dance(self, duration=1.0, frequency=1.0, delay=0.0):
        if self.__dancing == False:  # if we aren't dancing we have nothing to do
            return

        print('beat count %d' % self.__current_beat_count)

        # ignore adding moves if we're already doing a move
        if self.move_queue.qsize() > 0:
            return

        if self.__current_dance_mood == self.dance_moods.MOOD_CHILL:  # should be called once a bar
            print('auto dance - chill')
            # self.enqueue_move(self.dance_moves.MOVE_FIGURE_EIGHT, duration)
            self.enqueue_move(self.dance_moves.MOVE_BOX_LFRB, duration)
        elif self.__current_dance_mood == self.dance_moods.MOOD_GO_HARD:
            print('auto dance - going hard!')
            self.enqueue_move(self.dance_moves.MOVE_BOB_FB, 0.15)

            if self.__current_beat_count % 7 == 0:
                move_number = np.random.randint(0, 10)

                if move_number == 0:
                    self.enqueue_move(self.dance_moves.MOVE_SPIN_ALTERNATE, duration, delay)
                elif move_number == 1:
                    self.enqueue_move(self.dance_moves.MOVE_BOB_CLOCKWISE, duration, delay)
                elif move_number == 2:
                    self.enqueue_move(self.dance_moves.MOVE_BOB_FBLR, duration, delay)
                elif move_number == 3:
                    self.enqueue_move(self.dance_moves.MOVE_WIGGLE, duration, frequency, delay)
                    # elif move_number == 4:

        self.__current_beat_count = (self.__current_beat_count + 1) % 16

        # if self.__current_beat_count < 8:
        #     self.enqueue_move(self.dance_moves.MOVE_BOB_CLOCKWISE, 0.15)
        # elif self.__current_beat_count > 8:
        #     self.enqueue_move(self.dance_moves.MOVE_BOB_FBLR, 0.15)
        # elif self.__current_beat_count == 14:
        #     self.enqueue_move(self.dance_moves.MOVE_FLIP, 0.5)

    def set_mood(self, mood=dance_moods.MOOD_GO_HARD):
        self.__current_dance_mood = mood

    def mood(self):
        return self.__current_dance_mood

    def reset_beat_count(self):
        self.__current_beat_count = 0

    # returns whether the drone is ready to do dance moves
    def ready(self):
        return self.drone_state != self.drone_states.STATE_CALIBRATING

    # adds a move to the drone's queue
    def enqueue_move(self, move_type, duration, frequency=0.0, delay=0.0):
        print(
        'enqueued move number ' + str(move_type) + ' with duration ' + str(duration) + ', frequency ' + str(frequency))
        self.move_queue.put(self.dance_move(move_type, duration, frequency, delay))

    def get_back_in_the_box(self):
        print('get back in the box called')

        drone_should_be_dancing = self.__dancing
        if drone_should_be_dancing:
            self.stop_dancing()

        self.drone.stop()  # stop the drone
        #
        time.sleep(1.0)  # todo maybe we need this to give it time to stop
        print "drone has seen marker, drone stopped"

        # save the original angle in case we need to bail
        original_alpha = self.drone.NavData["vision_detect"][7][0]

        # get new angle reading
        NDC = self.drone.NavDataCount
        while self.drone.NavDataCount == NDC:  time.sleep(0.001)  # Wait until next time-unit
        alpha = self.drone.NavData["vision_detect"][7][0]

        # todo save drone angle on time of detection
        if not self.drone.NavData["vision_detect"][0] > 0:  # drone lost the tag
            print('lost the tag, using old estimate')
            alpha = original_alpha
        else:
            print('saw the tag, after new detection')

        speed_scale = 0.06  # TODO  # set the speed for the movement

        #    alpha = alpha + 180.0       # because of maths!! see my notepad (in red pen) for more details
        alpha = alpha - 90.0

        move1 = speed_scale * np.cos(np.deg2rad(alpha))  # left and right movements
        move1 = float(move1)
        move2 = speed_scale * np.sin(np.deg2rad(alpha))  # front and back movements
        move2 = float(move2)
        #    print "motor 1 (L/R): " + move1
        #    print "motor 2 (F/B): " + move2
        print move1
        print move2

        print "starting to move away from edge"
        self.drone.move(move1, move2, 0.0, 0.0)  # back away from the edge
        time.sleep(2.5)
        print "finished moving away from edge"

        if drone_should_be_dancing:
            self.start_dancing()

    def start_getting_navdata(self):
        print('start getting navdata called')
        self.__navdata_thread = threading.Thread(target=self.__navdata_worker)
        self.__retrieving_navdata = True
        self.__navdata_thread.start()

    def stop_getting_navdata(self):
        print('stopping getting navdata')
        self.__retrieving_navdata = False
        self.__navdata_thread.join()

    def __navdata_worker(self):
        print('started navdata worker')
        # test_iteration_count = 0
        while self.__retrieving_navdata:
            NDC = self.drone.NavDataCount

            if self.drone.NavData["altitude"][0] > 1500:  # drone has reached soft altitude limit
                print "drone too high, stop and land"
                self.drone.stop()
                print "stopped"
                time.sleep(1.0)
                self.drone.moveDown(1.0)
                print "moving down"
                time.sleep(3.0)
                print "landing"
                self.stop_dancing()
                self.land()

            if self.drone.NavData["vision_detect"][0] > 0:  # drone sees a tag
                print "detected tag, get back in the box"
                print str(self.drone.NavDataTimeStamp)
                self.get_back_in_the_box()

            while self.drone.NavDataCount == NDC:  time.sleep(0.001)  # Wait until next time-unit
            NDC = self.drone.NavDataCount  # TODO DOES IT BUFFER?

            # print('navdata decododed, iteration: %d' % test_iteration_count)
            # test_iteration_count = test_iteration_count + 1

    # worker function that reads moves from the move queue and dances accordingly
    def __dance_worker(self):
        while self.__dancing:
            if self.move_queue.empty():
                time.sleep(0.01)  # wait a bit if we don't have any moves to do
            else:
                move = self.move_queue.get()
                print('doing move number ' + str(move.move_type))
                self.__do_move(move)

    # start the drone dancing at the next move in the move queue, hovers if the queue is empty
    def start_dancing(self):
        if not self.__dancing:
            print('starting to dance')
            self.__dance_thread = threading.Thread(target=self.__dance_worker)
            self.__dancing = True
            self.__dance_thread.start()  # start the dancer worker function
            self.reset_beat_count()  # reset the beat count
        else:
            print('already dancing')

    # stop the drone dancing when the current move is complete, clears the move queue
    def stop_dancing(self):
        if not self.__dance_thread or self.__dance_thread.isAlive() == False:
            print('Unable to stop dancing: The drone is not currently dancing.')
        else:
            print('Telling dance worker to stop...')
            self.__dancing = False
            self.__dance_thread.join()
            self.move_queue.queue.clear()
            print('Stopped dancing')

    # converts a bpm to a frequency in Hz
    def bpm_to_frequency(self, bpm=128.0):
        return float(bpm) / 60.0

    # do_move wrapper todo just change do_move to this
    def __do_move(self, dance_move):
        self.do_move(dance_move.move_type, dance_move.duration, dance_move.frequency, dance_move.delay)

    # bust a move! # todo currently no way to set speed, only duration - you can use ps drone setspeed for now
    def do_move(self, move_type, duration=1.0, frequency=2.5, delay=0.0):  # todo fix sleep related errors
        self.drone_state = self.drone_states.STATE_DANCING

        if delay > 0.0:
            time.sleep(delay)

        if move_type == self.dance_moves.MOVE_NONE:
            self.drone_state = self.drone_states.STATE_HOVER
            self.drone.hover()
            time.sleep(duration)

        elif move_type == self.dance_moves.MOVE_FLIP:
            if self.drone.getBattery() < 45:
                print('drone is too low on battery to do a flip, have a forward back bob instead...')
                self.do_move(self.dance_moves.MOVE_BOB_FB, duration)
            else:
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
            # time.sleep(1.1)
            time.sleep(duration / 7.0)
            self.drone.move(0.0, 0.0, 0.0, 1.0)
            time.sleep(duration / 14.0)
            # time.sleep(0.3)
            self.drone.move(0.0, 0.0, -0.25, 1.0)
            time.sleep(2 * duration / 7.0)
            # time.sleep(2)
            self.drone.move(0.0, 0.0, 0.75, 1.0)
            # time.sleep(1.1)
            time.sleep(duration / 7.0)
            self.drone.move(0.0, 0.0, 0.0, 1.0)
            time.sleep(duration / 14.0)
            # time.sleep(0.3)
            self.drone.move(0.0, 0.0, -0.25, 1.0)
            # time.sleep(2)
            time.sleep(2 * duration / 7.0)
            self.chill()

        elif move_type == self.dance_moves.MOVE_QUICK_BOB:  # todo use anim instead
            print('quick bob!')
            # self.drone.moveForward(1)
            # 2.0943952e-01 default
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

        elif move_type == self.dance_moves.MOVE_BOB_CLOCKWISE:
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

            time.sleep(0.1)  # todo send heaps of these for a funky hoola effect
            self.chill()
            if duration > 0.1:
                time.sleep(duration - 0.1)

        elif move_type == self.dance_moves.MOVE_BOB_FBLR:
            print('fblr bob!')
            if self.bob_state_current == self.bob_motion.MOTION_LEFT \
                    or self.bob_state_current == self.bob_motion.MOTION_NONE:
                print('no bob motion, bobbing forward')
                self.drone.anim(2, 1000)
                self.bob_state_current = self.bob_motion.MOTION_FORWARD
            elif self.bob_state_current == self.bob_motion.MOTION_FORWARD:
                print('bobbed forward last, bobbing back')
                self.drone.anim(3, 1000)
                self.bob_state_current = self.bob_motion.MOTION_BACK
            elif self.bob_state_current == self.bob_motion.MOTION_BACK:
                print('bobbed back last, bobbing right')
                self.drone.anim(1, 1000)
                self.bob_state_current = self.bob_motion.MOTION_RIGHT
            elif self.bob_state_current == self.bob_motion.MOTION_RIGHT:
                print('bobbed right last, bobbing left')
                self.drone.anim(0, 1000)
                self.bob_state_current = self.bob_motion.MOTION_LEFT

            time.sleep(0.1)
            self.chill()
            if duration > 0.1:
                time.sleep(duration - 0.1)

        elif move_type == self.dance_moves.MOVE_BOB_FB:
            print('fb bob!')
            if self.bob_state_current != self.bob_motion.MOTION_FORWARD:
                print('bobbing forward')
                self.drone.anim(2, 1000)
                self.bob_state_current = self.bob_motion.MOTION_FORWARD
            else:
                print('bobbing back')
                self.drone.anim(3, 1000)
                self.bob_state_current = self.bob_motion.MOTION_BACK

            time.sleep(0.1)
            self.chill()
            if duration > 0.1:
                time.sleep(duration - 0.1)


        elif move_type == self.dance_moves.MOVE_BOX_LFRB:
            print('fblr BOX!')
            move_speed = 0.1
            if self.__current_box_motion == self.box_motion.MOTION_BACK \
                    or self.__current_box_motion == self.box_motion.MOTION_NONE:
                print('no box motion, going left')
                self.drone.moveLeft(move_speed)
                self.__current_box_motion = self.box_motion.MOTION_LEFT
            elif self.__current_box_motion == self.box_motion.MOTION_LEFT:
                print('boxed left last, moving forward')
                self.drone.moveForward(move_speed)
                self.__current_box_motion = self.box_motion.MOTION_FORWARD
            elif self.__current_box_motion == self.box_motion.MOTION_FORWARD:
                print('boxed forward last, moving right')
                self.drone.moveRight(move_speed)
                self.__current_box_motion = self.box_motion.MOTION_RIGHT
            elif self.__current_box_motion == self.box_motion.MOTION_RIGHT:
                print('boxed right last, moving back')
                self.drone.moveBackward(move_speed)
                self.__current_box_motion = self.box_motion.MOTION_BACK

            time.sleep(duration - 0.01)
            self.chill()

        elif move_type == self.dance_moves.MOVE_SPIN_CLOCKWISE:
            self.drone.move(0.0, 0.0, 0.0, 1.0)
            time.sleep(duration)

        elif move_type == self.dance_moves.MOVE_SPIN_CLOCKWISE_UP:
            self.drone.move(0.0, 0.0, 0.2, 1.0)
            time.sleep(duration)

        elif move_type == self.dance_moves.MOVE_SPIN_ALTERNATE:
            print('Alternating spin')
            if self.__current_spin_direction == self.spin_motion.MOTION_NONE or \
                            self.__current_spin_direction == self.spin_motion.MOTION_CCW:
                print('No spin or ccw spin last, spinning cw')
                self.drone.move(0.0, 0.0, 0.0, 1.0)
                self.__current_spin_direction = self.spin_motion.MOTION_CW
            elif self.__current_spin_direction == self.spin_motion.MOTION_CW:
                print('spun cw last now we gonna spin counter clockwise')
                self.drone.move(0.0, 0.0, 0.0, -1.0)
                self.__current_spin_direction = self.spin_motion.MOTION_CCW

            time.sleep(duration)

    def chill(self):
        self.drone.hover()
        self.drone_state = self.drone_states.STATE_HOVER

