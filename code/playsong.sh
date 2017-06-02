#!/usr/bin/env bash

play $1 &
echo $! > play_pid
