def build_system_prompt(policy):
    return f"""
You are an assistant.
Response style:
- Verbosity: {policy.verbosity}
- Tone: {policy.tone}

Follow these strictly.
"""