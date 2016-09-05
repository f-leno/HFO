#!/usr/bin/env python
# encoding: utf-8

# Before running this program, first Start HFO server:
# $> ./bin/HFO --offense-agents 1

import sys, itertools
from hfo import *
import time, ctypes

def main():
  # Create the HFO Environment
  hfo = HFOEnvironment()
  # Connect to the server with the specified
  # feature set. See feature sets in hfo.py/hfo.hpp.
  hfo.connectToServer(HIGH_LEVEL_FEATURE_SET,
                      '/home/leno/HFO/HFO-master/bin/teams/base/config/formations-dt', 6000,
                      'localhost', 'base_left', False)
  for episode in itertools.count():
    status = IN_GAME
    while status == IN_GAME:
      # Grab the state features from the environment
      print "------"+str(hfo.getUnum())
      features = hfo.getState()

      hfo.say(ctypes.c_char_p('Hello!'))
     # hfo.say('Hello!')
      #time.sleep(0.1)
      # Get any incoming communication
      msg = hfo.hear()
      # Print the incoming communication
      if msg:
        print('Heard: %s'% msg)
      # Take an action
      hfo.act(MOVE)
      # Create outgoing communication
      
      # Advance the environment and get the game status
      status = hfo.step()
    # Check the outcome of the episode
    print('Episode %d ended with %s'%(episode, hfo.statusToString(status)))
    # Quit if the server goes down
    if status == SERVER_DOWN:
      hfo.act(QUIT)
      break

if __name__ == '__main__':
  main()
