# MTRX5700-Major

## Dancing Drone Planning

### Equipment we need:

- either one big drone or two small ones

- microphone

- controller hardware

- speakers

- rpi maybe

### Things we want to achieve in order of priority

(1) make the drone move - and then try more complicated moves

(2) make it return back to its original starting position on the ground

(3) drone that moves in time with music - pre-loaded, steps are pre-planned

    (a) not crash into shit

    (b) pick out bars first

    (c) if the drone is fast enough, try smaller chunks - choreography

    (c) phrases - notes and stuff - might be hard

(4) drone that moves in time with live music - use the mic, do filtering

(5) movement/visual spectrum analyser


## Modules

### Laptop: music processing

- bar detection - plot the output in the time domain against the audio data

- BPM detection - plot the output in the time domain against the audio data

- mood dection, e.g. build up, drop, sad, happy

- optional: receive live audio input

### Laptop: sending appropriate commands for the desired dance moves

- resolve any latency issues

- process the detected bars or beats into a sequence of organised dance moves

### Drone: feedback controlled

- read sensor data

- correct for the drift

- ensure the desired dance move is executed properly

### Drone: sick dance moves

- dance moves to achieve: spin, flip, bobbing, figure of 8, circling

- determine length of each dance move, and when the dance move would be suitable, e.g. bobbing is for beats, figure of 8 is for bars, spinning for build ups, etc...

- set the desired motion commands

### Drone: powering up and down

- lift off at power up, return to same location at power down

## Things to get working by the end of this week (20/05/17)

- get the drone to take off and land - must be controlled by laptop/rpi/keyboard/game controller/joystick and not from phone app

- upload a test program to run on the drone as embedded software

- receive data from the sensors

- be able to detect the beat in various genres of music

## If wer're really feeling ambitious:

- be able to detect bars in music

- be able to detect sparse/non-rhythmic sections in music

- execute a simple dance move
