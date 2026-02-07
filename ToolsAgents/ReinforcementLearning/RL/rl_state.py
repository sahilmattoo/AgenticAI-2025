class RLState:
    """
    RL STATE s_t
    What the agent remembers about interaction so far
    """

    def __init__(self):
        self.step = 0
        self.last_action = None
        self.last_reward = None

    def update(self, action, reward):
        self.step += 1
        self.last_action = action
        self.last_reward = reward

    def as_dict(self):
        return {
            "step": self.step,
            "last_action": self.last_action,
            "last_reward": self.last_reward
        }
