import random


class Action(object):
    def __init__(self):
        super(Action, self).__init__()
        self.n = 4
        self.actions = list(range(4))

    def sample(self):
        action = random.sample(self.actions, 1)[0]

        return action
