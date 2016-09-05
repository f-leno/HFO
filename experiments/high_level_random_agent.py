#!/usr/bin/env python
# encoding: utf-8

# Before running this program, first Start HFO server:
# $> ./bin/HFO --offense-agents 1

import random, itertools
from hfo import *
from cmac import CMAC
from sarsa import SARSA


def main():
    print('New agent online!')
    print('..... Initializing learning algorithm: SARSA')
    ACTIONS = [MOVE, SHOOT, PASS_CLOSE, PASS_FAR, DRIBBLE]
    SARSA = SARSA(ACTIONS)
    print('..... Initializing discretization with CMAC')
    CMAC = CMAC(1,0.5,0.1)
    print('..... Loading HFO environment')
    hfo = HFOEnvironment()
    print('..... Connecting to HFO server')
    hfo.connectToServer(HIGH_LEVEL_FEATURE_SET,
                      'bin/teams/base/config/formations-dt', 6000,
                      'localhost', 'base_left', False)
    print('..... Start training')
    for episode in itertools.count():
        print('..... Starting episode %d' % episode)
        status = IN_GAME
        step = 0
        while status == IN_GAME:
            step += 1
            old_status = status
            # Get the vector of state features for the current state
            features = hfo.getState()
            state = transformFeatures(features)
            print('State: %s' % str(state))

            action = select_action(state)
            hfo.act(action)
            #print('Action: %s' % str(action))
            # Advance the environment and get the game status
            status = hfo.step()
            #print('Status: %s' % str(status))
            print('.......... Step %d: %s - %s - %s' % (step, str(old_status), str(action), str(status)))
        # Check the outcome of the episode
        print('..... Episode ended with %s'% hfo.statusToString(status))
        # Quit if the server goes down
        if status == SERVER_DOWN:
            hfo.act(QUIT)
            break

def transformFeatures(features):
    ''' From continuous to discrete using CMAC '''
    data = []
    for feature in features:
        quantized_features = CMAC.quantize(feature)
        data.append([pts])

def select_action(state):
    ''' for pass:
        1. sort teammembers according to proximity
        2. compare teammember angle to opponent angle and distance
        3. if pass select closest teammember with no oponent in the way

    '''

    print('Selecting action')
    # Perform the action
    if state[5] == 1: # State[5] is 1 when the player can kick the ball
        #return random.choice([SHOOT, PASS(team_mate), DRIBBLE])
        return random.choice([DRIBBLE, SHOOT])
    return MOVE


if __name__ == '__main__':
    main()
