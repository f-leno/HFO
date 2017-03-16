# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 10:56:04 2016

Torrey advising implementation
@author: Felipe Leno
"""

from qlearning import QLearning
from advice_util import AdviceUtil
import actions
import math

class Torrey(QLearning):
    
    fellowAgents = None
    spentBudget = None
    budget = None
    episodeUpdateTrace = None
    threshold = None
    
    def __init__(self,agentIndex,alpha=0.2,gamma=0.9,T=0.4,budget = 350,threshold = 0.001):
         super(Torrey, self).__init__(agentIndex,alpha=alpha,gamma=gamma,T=T)
               
         self.budget = budget
         self.spentBudget = 0
         self.fellowAgents = []
         self.threshold = threshold
         
         
    
    
    def setup_advising(self,agentIndex,allAgents):
        """ This method is called in preparation for advising """
        self.adviceObject = AdviceUtil()
        #Get the next agent
        index = (agentIndex+1)%len(allAgents)
        advisors = [allAgents[index]]
        self.adviceObject.setupAdvisors(advisors)
        
    def get_used_budget(self):
        return self.spentBudget
        
    def advise_action(self,uNum,state):
        """Verifies if the agent can advice a friend, and return the action if possible"""
        if self.spentBudget < self.budget:
            #Check if the agent should advise
            advise,advisedAction = self.check_advise(state)
            if advise:
                self.spentBudget = self.spentBudget + 1
                return advisedAction
        return None    
                        
    def check_advise(self,state): 
        """Returns if the agent should advice in this state.
        The advised action is also returned in the positive case"""
            
        
        importance = self.state_importance(state)

        if importance > self.threshold:
            advisedAction = self.action(state,True)
            return True,advisedAction          
            
        return False,None
        
    def state_importance(self,state):
        """Calculates the state importance
        state - the state
        typeProb - is the state importance being calculated in regard to
        the number of visits or also by Q-table values?"""
               
        allActions = [actions.NORTH, actions.SOUTH, actions.WEST, actions.EAST]
        maxQ,minQ = self.get_max_min_q_value(state,allActions)
       

        qImportance = math.fabs(maxQ - minQ) 
        
        
        
        return qImportance                                 

    
       
    def observe_reward(self,state,action,statePrime,reward) :
        """Does the necessary updates (Q-table, etc)"""
        super(Torrey, self).observe_reward(state,action,statePrime,reward)         
            
    def combineAdvice(self,advised):
        return int(max(set(advised), key=advised.count))  
             
        
    def action(self,state,noAdvice = False):
        """Returns the action for the current state"""
        if self.exploring and not noAdvice and state[0] != float('inf'):
            #Ask for advice
            advised = self.adviceObject.ask_advice(self.agentIndex,state)
            if advised:
                    try:                
                        action = self.combineAdvice(advised)
                        return action
                    except:
                        print "Exception when combining the advice " + str(advised)
        return super(Torrey, self).action(state,noAdvice)
        


