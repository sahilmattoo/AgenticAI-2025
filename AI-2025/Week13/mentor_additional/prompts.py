from langchain.prompts import PromptTemplate

prompt_template_v1 = PromptTemplate(
    input_variables=["v1", "v2"],
    template="""
You are a senior legal contract analyst.

You are given two versions of the same License Agreement.

--- VERSION 1 (ROUND 1) ---
{v1}

--- VERSION 2 (ROUND 2) ---
{v2}

TASK:
1. Identify ONLY clauses that are changed, clarified, restricted, or newly structured in Version 2.
2. For each change:
   - Clause / Topic Name
   - Position in Version 1
   - Position in Version 2
   - Change Classification:
     [Restriction | Clarification | Sequencing | Scope Narrowing | Governance Change | Operational Structuring]
3. Ignore clauses that remain unchanged.
4. Do NOT summarize the documents.
5. Output a clean, clause-by-clause difference report.

Be precise. Avoid assumptions.
"""
)

prompt_template_v2 = PromptTemplate(
    input_variables=["v1", "v2"],
    template="""
You are a senior legal contract analyst.

You are given two versions of the same License Agreement.

--- VERSION 1 (ROUND 1) ---
{v1}

--- VERSION 2 (ROUND 2) ---
{v2}

TASK:
1. Give the list of the clauses which got updated 
2. Write in 2 - 3 sentences key parts which got updated in the contract. Also specify the clause name.
3. The clauses which could potentially be impacted later.

OUTPUT:
1. Create difference between Version 1 and Version 2 in a tabular format

| Clause Name | Version 1 Position | Version 2 Position | Change Classification |
|-------------|---------------------|---------------------|-----------------------|
|             |                     |                     |                       |

Be precise. Avoid assumptions.
"""
)



prompt_template_v3 = PromptTemplate(
    input_variables=["v1", "v2"],
    template="""
You are a senior legal contract analyst.

You are given two versions of the same License Agreement.

--- VERSION 1 (ROUND 1) ---
{v1}

--- VERSION 2 (ROUND 2) ---
{v2}

TASK:
1. Give the list of the clauses which got updated 
2. Focus on Salary clause and how it has changed
3. How Timing of different Staff members get affected
4. Check the financial implications of the changes
5. Check for all liabilities 

OUTPUT:
1. Create difference between Version 1 and Version 2 in a tabular format

| Clause Name | Version 1 Position | Version 2 Position | Change Classification |
|-------------|---------------------|---------------------|-----------------------|
|             |                     |                     |                       |

Be precise. Avoid assumptions.
"""
)

