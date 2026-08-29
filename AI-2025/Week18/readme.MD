## Structure of the code  -- final_v.py

User Query
    ↓
Guardrails / Ethics Check
    ↓
Retriever (Policy Documents)
    ↓
Draft Response Generator
    ↓
Response Evaluator (LLM as Judge)
    ↓
Final Safe Answer


## Pattern to Add Drift Tools

    User Query
    ↓
    Guardrails
    ↓
    Retriever
    ↓
    Concept Drift Detector
    ↓
    Draft Response
    ↓
    Evaluation


## Bias Pattern Flow

    User Query
        ↓
    Guardrails Check
        ↓
    Policy Retrieval
        ↓
    Draft Response
        ↓
    Bias Detection  ← NEW
        ↓
    Response Evaluation
        ↓
    Drift Detection
        ↓
    Final Answer


## Governance Pipeline

             USER QUERY
                 ↓
            Guardrails
        (misuse protection)
                 ↓
             Retrieval
        (policy grounding)
                 ↓
           Draft Response
                 ↓
           Bias Detector
          (fairness check)
                 ↓
           Evaluation
          (quality check)
                 ↓
           Drift Detector
        (system monitoring)
                 ↓
            FINAL ANSWER