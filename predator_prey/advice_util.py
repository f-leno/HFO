# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 13:12:25 2016
Utilities for advising
@author: Felipe Leno
"""

class AdviceUtil():
    
    advisors = None
    
    def setupAdvisors(self,advisors):
        self.advisors = advisors

    def ask_advice(self,uNum,state):
         """This method is executed when the advisee asks for advice.
           uNum - the Uniform number of the advisee
           state - the advisee state after it is processed in the statespace_util methods
           """
         advice = []
         
         for advisor in self.advisors:
             
             a = advisor.advise_action(uNum,state)
             
             #Check if any advice was received
             if a:
                 advice.append(a)
         return advice

