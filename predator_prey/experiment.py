# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 15:42:22 2016
Experiment for the prey-predator environment
@author: Felipe Leno
"""
import argparse
import sys
import csv

import random

import os
from environment import PredatorPreyEnvironment,GoldMineEnvironment



def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n','--number_agents',type=int, default=3)
    parser.add_argument('-p','--number_preys',type=int, default=3)
    parser.add_argument('-a1','--agent1',  default='Dummy')
    parser.add_argument('-a2','--agent2',  default='Dummy')
    parser.add_argument('-a3','--agent3',  default='Dummy')
    parser.add_argument('-a4','--agent4',  default='Dummy')
    parser.add_argument('-a5','--agent5',  default='Dummy')
    parser.add_argument('-a6','--agent6',  default='Dummy')
    parser.add_argument('-a7','--agent7',  default='Dummy')
    parser.add_argument('-a8','--agent8',  default='Dummy')
    parser.add_argument('-a9','--agent9',  default='Dummy')
    parser.add_argument('-a10','--agent10',default='Dummy')
    parser.add_argument('-a11','--agent11',default='Dummy')
    parser.add_argument('-t','--learning_trials',type=int, default=1000)
    parser.add_argument('-i','--evaluation_interval',type=int, default=5)
    parser.add_argument('-d','--evaluation_duration',type=int, default=100)
    parser.add_argument('-s','--seed',type=int, default=0)
    parser.add_argument('-l','--log_file',default='/home/leno/HFO/predator_prey/results/')
    parser.add_argument('-r','--number_trials',type=int, default=1000)
    parser.add_argument('-it','--initial_trial',type=int, default=1)
    return parser.parse_args()

def build_agents():
    """Builds and returns the agent objects as specified by the arguments"""
    agents = []    
    
    
    parameter = get_args()
    
    for i in range(parameter.number_agents):
        agentName = getattr(parameter,"agent"+str(i+1))
        print "AgentName: "+agentName
        try:
           AgentClass = getattr(
                __import__( (agentName).lower(),
                        fromlist=[agentName]),
                agentName)
        except ImportError:
           sys.stderr.write("ERROR: missing python module: " +agentName + "\n")
           sys.exit(1)
    
        print "Creating agent"
        AGENT = AgentClass(i)
        print "OK Agent"
        agents.append(AGENT)
        
    return agents
    
def main():
    parameter = get_args()
    print parameter    
    
   # try:
    for trial in range(parameter.initial_trial,parameter.number_trials+1):
        print('***** %s: Start Trial' % str(trial))            
        random.seed(parameter.seed+trial)
        agents = build_agents()
        #The seed for initial state gneration must always be the same
        random.seed(parameter.seed)
        environment = PredatorPreyEnvironment(numberAgents = parameter.number_agents,agents = agents, 
                                              preys = parameter.number_preys, evalEpisodes = parameter.evaluation_duration,depth=3,rewardType=1,invertedAction=False,
                                              changeTransition=False)     
        #environment =GoldMineEnvironment(numberAgents = parameter.number_agents,agents = agents,preys = parameter.number_preys, evalEpisodes = parameter.evaluation_duration,depth=3 )
        random.seed(parameter.seed+trial)
                
        train_csv_writers = [None]*len(agents)
        train_csv_files = [None]*len(agents)
        eval_csv_writers = [None]*len(agents)
        eval_csv_files = [None]*len(agents)
        for i in range(len(agents)):
            logFolder = parameter.log_file + getattr(parameter,"agent"+str(i+1))
	    if not os.path.exists(logFolder):
                os.makedirs(logFolder)
	    logFolder += "/_0_"+str(trial)+"_AGENT_"+str(i+1)+"_RESULTS"
            train_csv_files[i] = open(logFolder + "_train", "wb")
            train_csv_writers[i] = csv.writer(train_csv_files[i])
            train_csv_writers[i].writerow(("trial","steps_captured","used_budget"))
            train_csv_files[i].flush()
            eval_csv_files[i] = open(logFolder + "_eval", "wb")
            eval_csv_writers[i] = csv.writer(eval_csv_files[i])
            eval_csv_writers[i].writerow(("trial","steps_captured","used_budget"))
            eval_csv_files[i].flush()
    
        print("******* OK Output File Creation*********")
        
        
        
        
        for agentIndex in range(len(agents)):
                agents[agentIndex].setup_advising(agentIndex,agents)
         
        for episode in range(0,parameter.learning_trials+1):
                        

                # perform an evaluation trial
                if(episode % parameter.evaluation_interval == 0):
                    for agentIndex in range(len(agents)):
                        agents[agentIndex].set_exploring(False)
                    stepsToCapture = 0

                    for eval_trials in range(1,parameter.evaluation_duration+1):
                        eval_step = 0
                        environment.start_evaluation_episode()

                        terminal = False
                        #For all steps...
                        #limit = float('inf')
                        while not terminal: #and eval_step <= limit:
                            eval_step += 1
                            #if episode>200:
                            #   print agents[0].state_importance(environment.get_state(0))
                            state = [None]*len(agents)
                            #Defines the action of each agent
                            for agentIndex in range(len(agents)):
                                state[agentIndex] = environment.get_state(agentIndex)                                
                                action = agents[agentIndex].action(state[agentIndex])
                                environment.act(agentIndex,action)
                            #Process state transition
                            environment.finish_state_transition()                        
                            #Updates reward                            
                            for agentIndex in range(len(agents)):
                                statePrime, action, reward = environment.step(agentIndex)                               
                                agents[agentIndex].observe_reward(state[agentIndex],action,statePrime,reward)                                          
                            
                            terminal = environment.is_terminal_state()
            
                        stepsToCapture += eval_step
                    
                    stepsToCapture = float(stepsToCapture) / parameter.evaluation_duration
                    for agentIndex in range(len(agents)):
                        #if episode != 0:
                        eval_csv_writers[agentIndex].writerow((episode,"{:.2f}".format(stepsToCapture),str(agents[agentIndex].get_used_budget())))
                        eval_csv_files[agentIndex].flush()
                        agents[agentIndex].set_exploring(True)
                    print("*******Eval OK: "+str(episode)+" - Duration: "+str(stepsToCapture))
                 
                stepsToCapture = 0       
                eval_step = 0
                environment.start_learning_episode()
                terminal = False
                #For all steps...
                while not terminal:
                    eval_step += 1
                    state = [None]*len(agents)
                    #Defines the action of each agent
                    for agentIndex in range(len(agents)):
                       state[agentIndex] = environment.get_state(agentIndex)                                
                       action = agents[agentIndex].action(state[agentIndex])
                       environment.act(agentIndex,action)
                    #Process state transition
                    environment.finish_state_transition()   
                    #Updates reward                            
                    for agentIndex in range(len(agents)):
                          statePrime, action, reward = environment.step(agentIndex)                               
                          agents[agentIndex].observe_reward(state[agentIndex],action,statePrime,reward) 
                    terminal = environment.is_terminal_state()
                    
                for agentIndex in range(len(agents)):
                    train_csv_writers[agentIndex].writerow((episode,"{:.2f}".format(eval_step),str(agents[agentIndex].get_used_budget())))
                    train_csv_files[agentIndex].flush()
                    
                    
        print('***** %s: END Trial' % str(trial)) 
            
    for agentIndex in range(len(agents)):
                    eval_csv_files[agentIndex].close()
                    train_csv_files[agentIndex].close()
        
        
       
                        
   # except Exception as e:
   #        exc_type, exc_obj, exc_tb = sys.exc_info()
   #        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
   #        print(exc_type, fname, exc_tb.tb_lineno)
   #        print e.__doc__
   #        print e.message
            
        

    

if __name__ == '__main__':
    main()