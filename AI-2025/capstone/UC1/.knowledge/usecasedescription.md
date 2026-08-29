# Scenario 1: Business Operations — AI Operations Copilot (Decision Support Only)

## Safety Requirements:
- Must refuse requests to modify data or trigger actions.
- Must explain uncertainty instead of guessing.
- Must provide escalation to a human analyst.
- Must not store sensitive business data in logs.


# Project Description - 
Organizations generate large volumes of operational data (sales, inventory, customer metrics), but extracting actionable insights from this data is time-consuming and requires skilled analysts.

This project aims to design an AI Operations Copilot that assists business users in analyzing operational data, identifying trends, and supporting decision-making

# Problem Statement - 
Design an AI Operations Copilot that enables business users to query operational data in natural language and receive actionable insights, while ensuring safety through strict non-execution constraints, uncertainty handling, and escalation mechanisms.


# User Persona
Primary User - 
Business Operations Analyst / Manager
Responsible for monitoring performance and making decisions

Secondary User - 
Senior Analyst / Leadership (for escalations)

# User Journey Atleast 1 UJ 
## UJ 1 - 
Analysing the trend of fall of sales in a particular region

## UJ 2 -
Comparing sales of two regions 

## UJ 3 -
Forecasting sales for the next quarter

# Define worklow - Add more details based on User Journey 
User reviews dashboard or dataset
   ↓
User asks question (natural language)
   ↓
AI analyzes data (trends, anomalies, comparisons) [Tools: ]
   ↓
AI provides insight + explanation
   ↓
If uncertain → explains limitation
   ↓
If high-risk → escalates to human analyst

# Assumptions:

## Inputs & Outputs

📥 Inputs
Natural language queries
Structured datasets (CSV / DataFrame / database)
Historical operational data

📤 Outputs
Insights (trend, anomaly, comparison)
Explanation of reasoning
Confidence / uncertainty statement
Escalation recommendation (if required)

## Constraints & Safety Requirements
### Define Guardrails

## Agentic AI Design Architecture 
- Use Langgraph for workflow orchestration
- Use Langchain for agentic AI design
- Use OpenAI for LLM
- Use Pandas for data analysis
- Use Streamlit for UI

# Example User Queries
“Why did sales drop last week?”
“Which region is underperforming?”
“What is the trend in customer churn?”
“Should we increase inventory for product X?”
“Compare revenue across regions”

# Success Criteria
1. 10 manual is getting replaced ?
2. out of 10 how many are answered correctly ?
3. Right answer saving the money 
4. CXO question answered in 1 min earlier it use to take 3 days 



# Final Deliverables
1. Use Langchain if you want only tools
2. If you want Agents use Langgraph
3. Curate Evaluate criteria carefully  
3.1 Create or Maintain an Excel and try to present atleast 2 variations 
3.2 Result should be present for atleast 2 variations [Archtecture design , Prompt]
4. All the Tasks can be accomodated 
5. 
