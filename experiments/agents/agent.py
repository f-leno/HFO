import logging
_logger = logging.getLogger(__name__)

import abc

class Agent(object):
    """ This is the base class for all agent implementations.

    The agent gets its available actions from the environment, keeps track of
    his current state and saves his experiences in a replay memory while acting
    in the environment.

    Attributes:
        name (str): The name of the network object.
        env (Environment): The envirnoment in which the agent actuates (which is an HFO object).
        rng (mtrand.RandomState): Initialized Mersenne Twister pseudo-random number generator.
        n_steps_total (int): Counter of all training steps.
        callback (Statistics): The stats module that attaches itself to the agent.
        exploring: variable to indicate if the agent is exploring or exploiting

    Note:
        All subclasses must inherite this class --> 'class NewClass(Agent)'

    """
    __metaclass__ = abc.ABCMeta

    def __str__(self):
        """ Overwrites the object.__str__ method.

        Returns:
            string (str): Important parameters of the object.
        """
        return "'name':" + str(self.name) + ", " + \
               "'epsilon_start':" + str(self.epsilon_start) + ", " + \
               "'epsilon_end':" + str(self.epsilon_end) + ", " + \
               "'epsilon_decay_steps':" + str(self.epsilon_decay_steps) + ", " + \
               "'n_avail_actions':" + str(self.n_avail_actions) + ", " + \
               "'avail_actions':" + str(self.avail_actions)

    def __init__(self, env, args, rng, name):
        """ Initializes an agent for a given environment.

        Args:
            env (Environment): The envirnoment in which the agent actuates.
            mem (Memory): The replay memory to save the experiences.
            net (Learner): Object of one of the Learner modules.
            args (argparse.Namespace): All settings either with a default value or set via command line arguments.
            rng (mtrand.RandomState): initialized Mersenne Twister pseudo-random number generator.
            name (str): The name of the agent.

        """
        _logger.debug("Initialize object of type " + str(type(self).__name__))
        self.name = name
        self.env = env
        self.rng = rng
        self.n_steps_total = 0
        #self.phase = None
        #self.callback = None
        self.exploring = True

    @abc.abstractmethod
    def act(self,state):
        """ When this method is called, the agent executes an action. """
        pass

    @abc.abstractmethod
    def observeReward(self,state,reward,statePrime):
        """ After executing an action, the agent is informed about the state-reward-state tuple """
        pass
    
    def setExploring(self,exploring):
        """ The agent keeps track if it should explore in the current state (used for evaluations) """
        self.exploring = exploring
        
