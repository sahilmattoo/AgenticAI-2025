# policy.py
class ResponsePolicy:
    def __init__(self):
        self.verbosity = "medium"     # short | medium | detailed
        self.tone = "neutral"         # neutral | friendly | formal

    def update(self, delta: dict):
        for k, v in delta.items():
            setattr(self, k, v)

    def as_dict(self):
        return {
            "verbosity": self.verbosity,
            "tone": self.tone
        }

    def __repr__(self):
        return f"Policy(verbosity={self.verbosity}, tone={self.tone})"
