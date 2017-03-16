# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 12:48:00 2016
Base agent class for the prey-predator environment
@author: Felipe Leno
"""
import abc
class Agent(object):
    
    agentIndex = None    
    exploring  = None
    
    def __init__(self,agentIndex):
        self.agentIndex = agentIndex
        self.exploring = True
        
   
    def setup_advising(self,agentIndex,allAgents):
        """Prepares the agent for the advising procedure"""
        self.agentIndex = agentIndex

    
    @abc.abstractmethod
    def action(self,state):
        """Returns the action for the current state"""
        pass
    
    @abc.abstractmethod
    def observe_reward(self,state,action,statePrime,reward) :
        """Does the necessary updates (Q-table, etc)"""
        pass
    
    def get_used_budget(self):
        """Returns the currently used budget for this agent"""
        return 0
    
    def set_exploring(self,exploring):
        """Set if the agent is exploring or not"""
        self.exploring = exploring
    
    def get_agentIndex(self):
        return self.agentIndex