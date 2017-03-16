# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 15:03:00 2016
dHocTD implementation
@author: leno
"""


from adhoc import AdHoc
import math
import random
import actions 

class AdHocTD(AdHoc):
    logAdv = False
    logAsk = []
    logAdvice = []
    def __init__(self,agentIndex,alpha=0.2,gamma=0.9,T=0.4,budgetAsk = 350,budgetAdv = 350):
         super(AdHocTD, self).__init__(agentIndex,alpha=alpha,gamma=gamma,T=T,budgetAsk = budgetAsk, budgetAdv = budgetAdv)

    
    def check_advise(self,state): 
        """Returns if the agent should advice in this state.
        The advised action is also returned in the positive case"""
            
        #print "ENTER HERE"
        numberVisits = self.visitedNumber.get(state,0)
         
        
        if numberVisits == 0:
            return False,None
        
        allActions = [actions.NORTH, actions.SOUTH, actions.WEST, actions.EAST]
        maxQ,minQ = self.get_max_min_q_value(state,allActions)
            
            # print "MaxQ "+str(maxQ)
            # print "MinQ "+str(minQ)
            # print "len "+str(len(actions))
        difQ = math.fabs(maxQ - minQ)
        
        #param = 1.5
        param = 0.7
        
        value = (math.sqrt(numberVisits) * difQ )
        
        #Calculates the probability
        prob = 1 - (math.pow((1 + param),-value))
        
      
        ##
        #processedState = self.quantize_features(state)
        #numberVisits = self.number_visits(processedState)
        #if value>0:        
        #print str(numberVisits)+"  -  "+str(value)+" - "+str(prob)
        ##
        #Check if the agent should advise
        if random.random() < prob: #and prob > 0.1:
            advisedAction = self.action(state,True)
            if self.logAdv:
                self.logAdvice.append([prob,numberVisits,difQ])
            return True,advisedAction          
            
        return False,None
        
    def check_ask(self,state):
        """Returns if the agent should ask for advise in this state"""
        
        if self.exploring and self.spentBudgetAsk < self.budgetAsk and state[0] != float('inf'):#not (state in self.advisedState) and :
            
            numberVisits = self.visitedNumber.get(state,0)
            if numberVisits == 0:
                return True
            
            #param = 0.3
            param = 0.3
            #Calculates the pobability
            prob =  math.pow((1 + param),-math.sqrt(numberVisits))
            
            ##
            #processedState = self.quantize_features(state)
            #numberVisits = self.number_visits(processedState)
            #print str(numberVisits)+"  -  "+str(prob)
            ##
            
            if random.random() < prob: #and prob > 0.1:
                #print "Asked: prob:"+str(prob)+" visits: "+str(numberVisits)
                if self.logAdv:
                    self.logAsk.append([prob,numberVisits])
                return True
        return False
        
    def observe_reward(self,state,action,statePrime,reward) :
        """Does the necessary updates (Q-table, etc)"""

        super(AdHocTD, self).observe_reward(state,action,statePrime,reward)   
        if reward==1 and self.logAdv and self.exploring: #terminal state
            with open("LogAdvTD.log","w") as myFile:
                myFile.write('\n'.join(map(str, self.logAdvice)))
            with open("LogAskTD.log","w") as myFile:
                myFile.write('\n'.join(map(str, self.logAsk)))
            self.logAdvice = []
            self.logAsk = []