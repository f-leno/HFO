# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 13:41:41 2016
AdHoc implementation
@author: Felipe Leno
"""

from qlearning import QLearning
from advice_util import AdviceUtil
import actions
import math
import abc

class AdHoc(QLearning):
    
    
    spentBudgetAsk = None
    spentBudgetAdv = None
    budgetAsk = None
    budgetAdv = None
    visitedNumber = None
    advisedState = None
    adviceObject = None
    
    
    
    def __init__(self,agentIndex,alpha=0.2,gamma=0.9,T=0.4,budgetAsk = 350,budgetAdv = 350):
         super(AdHoc, self).__init__(agentIndex,alpha=alpha,gamma=gamma,T=T)
               
         self.budgetAsk = budgetAsk
         self.budgetAdv = budgetAdv
         self.spentBudgetAsk = 0
         self.spentBudgetAdv = 0
         self.fellowAgents = []
         self.visitedNumber = {}
         self.advisedState = {}
         
         
         
    
    
    def setup_advising(self,agentIndex,allAgents):
        """ This method is called in preparation for advising """
        self.adviceObject = AdviceUtil()
        fellows = [x for i,x in enumerate(allAgents) if i!=agentIndex]
        self.adviceObject.setupAdvisors(fellows)
        
    def get_used_budget(self):
        return self.spentBudgetAdv
        
    def advise_action(self,uNum,state):
        """Verifies if the agent can advice a friend, and return the action if possible"""
        if self.spentBudgetAdv < self.budgetAdv:
            #Check if the agent should advise
            advise,advisedAction = self.check_advise(state)
            if advise:
                self.spentBudgetAdv = self.spentBudgetAdv + 1
                return advisedAction
        return None    
             
    @abc.abstractmethod
    def check_advise(self,state): 
        """Returns if the agent should advice in this state.
        The advised action is also returned in the positive case"""
        pass
    @abc.abstractmethod
    def check_ask(self,state): 
        """Returns if the agent should advice in this state.
        The advised action is also returned in the positive case"""
        pass
                

    
       
    def observe_reward(self,state,action,statePrime,reward) :
        """Does the necessary updates (Q-table, etc)"""

        super(AdHoc, self).observe_reward(state,action,statePrime,reward)   
        if reward==1: #terminal state
            self.advisedState = {}
            
    def combineAdvice(self,advised):
        return int(max(set(advised), key=advised.count))  
             
        
    def action(self,state,noAdvice = False):
        """Returns the action for the current state"""
        if self.exploring and not noAdvice:
            self.visitedNumber[state] = self.visitedNumber.get(state,0) + 1
            ask = self.check_ask(state)
            if ask:            
                #Ask for advice
                advised = self.adviceObject.ask_advice(self.agentIndex,state)
                if advised:
                        try: 
                            self.spentBudgetAsk = self.spentBudgetAsk + 1
                            action = self.combineAdvice(advised)
                            self.advisedState[state] = True
                            return action
                        except:
                            print "Exception when combining the advice " + str(advised)
        return super(AdHoc, self).action(state,noAdvice)
        


