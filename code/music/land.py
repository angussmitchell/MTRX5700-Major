from drone_dancer import drone_dancer

dancer = drone_dancer()
dancer.start_getting_navdata()


dancer.drone.stop()

dancer.drone.land()