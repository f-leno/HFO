# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 13:01:48 2016
Dummy agent for the prey-predator
@author: Felipe Leno
"""

from agent import Agent
import actions
import random

class Dummy(Agent):
    
    
    def __init__(self,agentIndex):
        super(Dummy, self).__init__(agentIndex=agentIndex)
     
    def observe_reward(self,state,action,statePrime,reward) :
        """Does the necessary updates (Q-table, etc)"""
        pass     
        
    def action(self,state):
        """Returns the action for the current state"""
        
        allActions = [actions.NORTH, actions.SOUTH, actions.WEST, actions.EAST]
        act = random.choice(allActions)
        return act
        
        pass
    



