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
                     
  goalsAllTrials = 0.0
  totalTimeToGoal = 0.0
  for episode in itertools.count():
    numSteps =  0
    status = IN_GAME
    while status == IN_GAME:
      numSteps = numSteps+1
      # Get the vector of state features for the current state
      state = hfo.getState()
      # Perform the action
      if state[5] == 1: # State[5] is 1 when the player can kick the ball
        hfo.act(random.choice([SHOOT, DRIBBLE]))
      else:
        hfo.act(MOVE)
      # Advance the environment and get the game status
      status = hfo.step()
      
     # print "Reward:  "+str(getReward(status));
      
      
      if(status==GOAL):
          goalsAllTrials = goalsAllTrials+1
          totalTimeToGoal = totalTimeToGoal + numSteps         
     

          
    # Check the outcome of the episode
    print('Episode %d ended with %s'%(episode, hfo.statusToString(status)))
    # Quit if the server goes down
    if status == SERVER_DOWN:
      hfo.act(QUIT)
      break
   
  print "Goal Percentage:  "+str(goalsAllTrials/episode*100)
  print "Time to Goal:     "+str(totalTimeToGoal/episode)
    
        
def getReward(status):
     if(status == CAPTURED_BY_DEFENSE):
          return -1
     elif(status==GOAL):
          return +1
     return 0;

if __name__ == '__main__':
  main()#arguments)
  
  

  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
