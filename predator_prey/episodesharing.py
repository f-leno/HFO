# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 10:19:49 2016

Episode Sharing implementation for the predator-prey environment
@author: Felipe Leno
"""

from qlearning import QLearning

class EpisodeSharing(QLearning):
    
    fellowAgents = None
    spentBudget = None
    budget = None
    episodeUpdateTrace = None
    
    def __init__(self,agentIndex,alpha=0.2,gamma=0.9,T=0.4,budget = 350):
         super(EpisodeSharing, self).__init__(agentIndex,alpha=alpha,gamma=gamma,T=T)
               
         self.budget = budget
         self.spentBudget = 0
         self.fellowAgents = []
         self.episodeUpdateTrace = []
         
    
    
    def setup_advising(self,agentIndex,allAgents):
        """ This method is called in preparation for advising """
        fellows = [x for i,x in enumerate(allAgents) if i!=agentIndex]
        self.fellowAgents = fellows
        
    def get_used_budget(self):
        return self.spentBudget
        
    def adviseFellow(self):
        """Perform the episode sharing"""
        
        if self.spentBudget < self.budget:
            for i in range(len(self.episodeUpdateTrace)):
                state = self.episodeUpdateTrace[i][0]
                action = self.episodeUpdateTrace[i][1]
                statePrime = self.episodeUpdateTrace[i][2]
                reward = self.episodeUpdateTrace[i][3]
            
                for agent in self.fellowAgents:
                    if self.spentBudget < self.budget:
                        agent.updateFromAdvice(state,action,statePrime,reward)
                        self.spentBudget = self.spentBudget + 1  
        self.episodeUpdateTrace = []
                        
                                

    
    def updateFromAdvice(self,state,action,statePrime,reward):
        """Updates Q table from advice""" 
        nowExp = self.exploring        
        self.exploring = True
        super(EpisodeSharing, self).observe_reward(state,action,statePrime,reward)
        self.exploring = nowExp
        
    def observe_reward(self,state,action,statePrime,reward) :
        """Does the necessary updates (Q-table, etc)"""
        super(EpisodeSharing, self).observe_reward(state,action,statePrime,reward)
        if self.exploring:
            self.episodeUpdateTrace.append((state,action,statePrime,reward))
        
        if reward==1 and self.exploring: #Terminal state
            self.adviseFellow()
        
            
            
        
             
        
    def action(self,state):
        """Returns the action for the current state"""
        return super(EpisodeSharing, self).action(state)
        
