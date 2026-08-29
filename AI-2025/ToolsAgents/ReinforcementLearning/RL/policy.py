class ResponsePolicy:
    """
    RL POLICY π(s)
    Maps state → action (behavior choice)
    """

    def __init__(self):
        self.verbosity = "medium"
        self.tone = "neutral"

    def update(self, delta: dict):
        for k, v in delta.items():
            setattr(self, k, v)

    def as_dict(self):
        return {
            "verbosity": self.verbosity,
            "tone": self.tone
        }
