def apply_policy_update(policy, interpretation):
    """
    RL LEARNING STEP
    Updates policy based on reward + direction
    """

    reward = interpretation.get("reward", 0)
    dims = interpretation.get("dimensions", {})

    # Learn only if reward is negative
    if reward < 0:
        if dims.get("verbosity") == "increase":
            policy.verbosity = "detailed"
        elif dims.get("verbosity") == "decrease":
            policy.verbosity = "short"

        if dims.get("tone") == "more_friendly":
            policy.tone = "friendly"
        elif dims.get("tone") == "more_formal":
            policy.tone = "formal"
