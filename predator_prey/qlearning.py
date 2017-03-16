# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 13:01:48 2016
Q-Learning agent for the prey-predator
@author: Felipe Leno
"""

from agent import Agent
import actions
import random
import math

class QLearning(Agent):
    
    alpha = None
    gamma = None
    T = None
    qTable = None
    
    def __init__(self,agentIndex,alpha=0.2,gamma=0.9,T=0.4):
        super(QLearning, self).__init__(agentIndex=agentIndex)
        self.alpha = alpha
        self.gamma = gamma
        self.T = T
        self.qTable = {}
     
    def observe_reward(self,state,action,statePrime,reward) :
        """Does the necessary updates (Q-table, etc)"""
        if self.exploring:
            allActions = [actions.NORTH, actions.SOUTH, actions.WEST, actions.EAST]
            qValue= self.qTable.get((state,action),0)
            V = self.get_max_q_value(statePrime,allActions)
            
            newQ = qValue + (self.alpha) * (reward + self.gamma * V - qValue)
            
            self.qTable[(state,action)] = newQ
             
        
    def action(self,state,advise=False):
        """Returns the action for the current state"""
        
        allActions = [actions.NORTH, actions.SOUTH, actions.WEST, actions.EAST]
        if state == tuple('blind'):
            return random.choice(allActions)
        if(self.exploring):
            if advise:
                act = self.get_max_q_action(state,allActions)
            else:
                act = self.explore_boltzmann(state,allActions)            
        else:
            act = self.get_max_q_action(state,allActions)            
            #act = self.get_max_q_action(state,allActions)      
            
                   
        return act
       
    def explore_boltzmann(self,state,allActions):
        """Selects one action using the boltzmann exploration"""
        prob = random.random()
        if prob <= 0.1:
             return random.choice(allActions)
        return self.get_max_q_action(state,allActions)
#        valueActions = []
#        sumActions = 0
#        for action in allActions:
#            qValue = self.qTable.get((state,action),0)
#            vBoltz = math.pow(math.e,qValue/self.T)
#            valueActions.append(vBoltz)
#            sumActions += vBoltz
#        
#        probAct = []
#        for index in range(len(allActions)):
#            probAct.append(valueActions[index] / sumActions)
#        
#        rndVal = random.random()
#        
#        sumProbs = 0
#        i=-1
#        
#        while sumProbs <= rndVal:
#            i = i+1
#            sumProbs += probAct[i]
#        
#        return allActions[i]
            
    def get_max_q_value_action(self,state,allActions):
        """Returns the maximum Q value and correspondent action to a given state"""
        maxActions = []
        maxValue = -float('Inf')
        
        for act in allActions:
            qV = self.qTable.get((state,act),0)
            if(qV>maxValue):
                maxActions = [act]
                maxValue = qV
            elif(qV==maxValue):
                maxActions.append(act)
        
        
        action = random.choice(maxActions)


        
        return maxValue,action
        
    def get_max_min_q_value(self,state,allActions):
        """Returns both the maximum and minimun Q-value for a given state"""
        maxValue = -float('Inf')
        minValue = float('Inf')
        
        for act in allActions:
            qV = self.qTable.get((state,act),0)
            if(qV>maxValue):
                maxValue = qV
            elif(qV<=minValue):
                minValue = qV      
        return maxValue,minValue
        
    
    def get_max_q_value(self,state,allActions):
        """Returns the value of the greatest Q value for that state"""
        v,a =  self.get_max_q_value_action(state,allActions)
        return v
            
        
    def get_max_q_action(self,state,allActions):
        """Returns the action correspondent to the max Q value"""
        v,a =  self.get_max_q_value_action(state,allActions)
        return a
        
    
    
    



