from drone_dancer import drone_dancer
import time
from play_song import play_song

beat_num = -2

bar_count = -5

flipped = False

g_current_bpm = 120

def hook():
    if audio.current_time() > 8.0:
        global beat_num, flipped, bar_count

        # if beat_num == 7:
        #     dancer.enqueue_move(dancer.dance_moves.MOVE_FLIP, audio.current_beat_s() - 0.01)
        # if beat_num < 8:
        #     dancer.enqueue_move(dancer.dance_moves.MOVE_BOB_CLOCKWISE, audio.current_beat_s())
        # else:
        # dancer.enqueue_move(dancer.dance_moves.MOVE_BOB_FBLR, 0.1)
        #
        if beat_num % 4 == 0:
            # dancer.enqueue_move(dancer.dance_moves.MOVE_BOX_LFRB, audio.current_beat_s() * 2)
            # dancer.enqueue_move(dancer.dance_moves.MOVE_NONE, audio.current_beat_s()*1)
            # dancer.enqueue_move(dancer.dance_moves.MOVE_BOB_FBLR, audio.current_beat_s() * 1)
            print 'changing!'
            bar_count = bar_count + 1
            if bar_count == 0:
                dancer.move_queue.queue.clear()
                # dancer.enqueue_move(dancer.dance_moves.MOVE_FLIP, audio.current_beat_s())
                dancer.set_mood(dancer.dance_moods.MOOD_GO_HARD)
            elif bar_count > 0 and bar_count < 8:
                print ('in this section')
                # print 'moving'
                # if bar_count % 2 == 0:
                #     print 'moving up'
                #     dancer.drone.moveUp(0.4)
                # else:
                #     print 'moving down'
                #     dancer.drone.moveDown(1)
            else:
                print 'hovering'
                dancer.drone.hover()

        if dancer.mood() == dancer.dance_moods.MOOD_GO_HARD:
            dancer.auto_dance()
        elif beat_num % 8 == 0:
            dancer.auto_dance(audio.current_beat_s()*8 - 0.05)
        beat_num = beat_num + 1


        # dancer.auto_dance()

    # elif audio.current_time() > 7.5 and flipped == False:
    #     dancer.enqueue_move(dancer.dance_moves.MOVE_FLIP, 1.1)
    #     dancer.start_dancing()
    #     flipped = True


audio = play_song('../music/AllTheSmallThings.flac.wav')

# for i in range(0, 100):
#     # print('current time is %f' % audio.current_time())
#     # print('current bpm is %f' % audio.current_bpm())
#     time.sleep(0.1)


dancer = drone_dancer()

# dancer.takeoff(False)

dancer.takeoff(True)



print('waiting for drone to be ready')
while not dancer.ready():
    time.sleep(0.05)

audio.start()


# dancer.drone.moveUp(1)
# time.sleep(1.5)
# dancer.drone.hover()

print('drone ready, starting song')

dancer.set_mood(dancer.dance_moods.MOOD_CHILL)

#
# time.sleep(10)

print('setting beat event hook')
audio.set_beat_event(hook)

# dancer.enqueue_move(dancer.dance_moves.MOVE_FLIP, 5)
# dancer.enqueue_move(dancer.dance_moves.MOVE_WIGGLE, 2, 2.5)
# dancer.enqueue_move(dancer.dance_moves.MOVE_QUICK_BOB, 2)


dancer.start_dancing()

print('sleeping for 15 seconds then stopping')

time.sleep(200)

# dancer.stop_dancing()
#
# dancer.land()

audio.stop()