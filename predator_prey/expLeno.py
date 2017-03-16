# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 08:49:36 2016
Experiment facilitation
@author: Felipe Leno
"""
import subprocess
from threading import Thread
import math
import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a','--algorithm',  default='Dummy')
    parser.add_argument('-l','--log_folder',default='./results/')
    parser.add_argument('-p','--number_preys',type=int, default=1)

    return parser.parse_args()


def thread_agent(initTrial,endTrial):
       
       arg = get_args()
       alg = arg.algorithm
       logFolder = arg.log_folder
       seed = 0
       prey = arg.number_preys
    
       command = "python experiment.py -l" + logFolder + " -it " + str(initTrial) + " -r " + str(endTrial) +  \
               " -a1 " + alg + " -a2 "+alg+ " -a3 "+alg + " -s "+str(seed) + " -p "+str(prey) + \
               " -d 2"
            
       print "******Init Thread "+str(initTrial)+"-"+str(endTrial)+" - "+ alg+"**********"
    
       subprocess.call(command, shell=True)  
        
        
def runMultipleThreads():
    numThreads = 2
    numTrials = 1000
    
    dividedT = int(math.floor(numTrials / numThreads))
    
    
    agentThreads = []
    
    for i in range(numThreads):
            agentThreads.append(Thread(target = thread_agent, args=((i*dividedT)+1,(i+1)*dividedT)))
            agentThreads[i].start()
            
            
            
    #Waiting for program termination
    for i in range(len(agentThreads)):
           agentThreads[i].join()
           
    print "End of Executions ***"
    

if __name__ == '__main__':
    runMultipleThreads()