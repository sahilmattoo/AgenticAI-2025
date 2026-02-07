def apply_policy_update(policy, interpretation):
    dims = interpretation.get("dimensions", {})

    # Verbosity
    if dims.get("verbosity") == "increase":
        policy.verbosity = "detailed"
    elif dims.get("verbosity") == "decrease":
        policy.verbosity = "short"

    # Tone
    if dims.get("tone") == "more_friendly":
        policy.tone = "friendly"
    elif dims.get("tone") == "more_formal":
        policy.tone = "formal"
