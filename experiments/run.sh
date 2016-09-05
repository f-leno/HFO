#!/bin/bash
which python
./bin/HFO --offense-agents=1 --no-sync --fullstate --trials 1 &
sleep 5
./experiments/high_level_random_agent.py 6000 &
#sleep 5
#./experiments/high_level_random_agent 6000 &

# The magic line
#   $$ holds the PID for this script
#   Negation means kill by process group id instead of PID
trap "kill -TERM -$$" SIGINT
wait
