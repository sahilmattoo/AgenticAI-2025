from .policy_engine import ResponsePolicy

class PromptBuilder:
    """
    Constructs system prompts based on the active ResponsePolicy.
    """
    
    @staticmethod
    def build_system_prompt(policy: ResponsePolicy) -> str:
        
        # Tone instructions
        tone_map = {
            "formal": "Use professional, academic, and precise language. Avoid slang or contractions.",
            "neutral": "Use clear, objective, and balanced language. Be professional but accessible.",
            "casual": "Use friendly, conversational, and relaxed language. You can be personable."
        }
        
        # Structure instructions
        structure_map = {
            "bulleted": "Present your response primarily as a list of bullet points. Use brief introductory and concluding sentences.",
            "narrative": "Present your response as connected paragraphs. Tell a coherent story or explanation.",
            "steps": "Present your response as a numbered sequence of steps. Ensure clear logical flow."
        }
        
        # Verbosity instructions
        verbosity_map = {
            "short": "Be remarkably concise. Get straight to the point. Limit response to 1-3 sentences or points where possible.",
            "medium": "Provide a balanced level of detail. Explain key concepts but avoid unnecessary fluff.",
            "long": "Be comprehensive and detailed. Explore nuances, provide examples, and ensure thorough coverage."
        }
        
        system_prompt = f"""You are an advanced adaptive agent. Your goal is to be helpful and accurate.

CRITICAL INSTRUCTIONS ON BEHAVIOR:
1. TONE: {tone_map.get(policy.tone, tone_map['neutral'])}
2. STRUCTURE: {structure_map.get(policy.structure, structure_map['narrative'])}
3. LENGTH/DEPTH: {verbosity_map.get(policy.verbosity, verbosity_map['medium'])}

Follow these instructions strictly for every response.
"""
        return system_prompt
