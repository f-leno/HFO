# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 17:29:45 2016

@author:Felipe Leno

Before running this program, first Start HFO server:
$> ./bin/HFO --offense-agents 1

This file executes the learning loop of one trial. Execute this file as:
python learningLoop.py -trials <n> -agent <agentType> -o <outputFile> -path <HFO folder>
<n> is the number of the trial
<agentType> is the name of the algorithm to be executed
<outputFile> is the path to output the results
<HFO folder> path for the HFO main folder (optional)

The experiment parameters are in exp_param.py.

"""

#!/usr/bin/env python
# encoding: utf-8

# Before running this program, first Start HFO server:
# $> ./bin/HFO --offense-agents 1

import random, itertools
from hfo import *

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
      # Get the vector of state features for the current state
      state = hfo.getState()
      # Perform the action
      if state[5] == 1: # State[5] is 1 when the player can kick the ball
        hfo.act(random.choice([SHOOT, DRIBBLE]))
      else:
        hfo.act(MOVE)
      # Advance the environment and get the game status
      status = hfo.step()
      if(status == CAPTURED_BY_DEFENSE):
          print("LOST")
      elif(status==GOAL):
          print("WIN")

          
    # Check the outcome of the episode
    print('Episode %d ended with %s'%(episode, hfo.statusToString(status)))
    # Quit if the server goes down
    if status == SERVER_DOWN:
      hfo.act(QUIT)
      break
  
  
# Reads the arguments and format them into a tuple
def processArguments(arguments):
    outputfile = '.'
    hfofile = '.'
    nTrials = 1
    agentname = ''
    
    opts, args = getopt.getopt(arguments,"o",["trials","agent","path"])
    except getopt.GetoptError:
        print "python learningLoop.py -trials <n> -agent <agentType> -o <outputFile> -path <HFO folder>"
    for opt, args in opts
    
    
    

if __name__ == '__main__':
  arguments = processArguments(sys.argv)
  #main()#arguments)
  
  

  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
