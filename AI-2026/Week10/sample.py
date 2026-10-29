from crewai import Agent, Task, Crew, Process

# AGENTS - Students complete the definitions

hr_analyst = Agent(
    role="...",
    goal="...",
    backstory="...",
    llm=llm
)

resume_evaluator = Agent(
    role="...",
    goal="...",
    backstory="...",
    llm=llm
)

hiring_advisor = Agent(
    role="...",
    goal="...",
    backstory="...",
    allow_delegation=True,
    llm=llm
)

# TASKS - Students design descriptions and outputs

jd_task = Task(
    description="...",
    expected_output="...",
    agent=hr_analyst
)

resume_task = Task(
    description="...",
    expected_output="...",
    agent=resume_evaluator
)

assessment_task = Task(
    description="...",
    expected_output="...",
    agent=hiring_advisor
)

# CREW

crew = Crew(
    agents=[
        hr_analyst,
        resume_evaluator,
        hiring_advisor
    ],
    tasks=[
        jd_task,
        resume_task,
        assessment_task
    ],
    process=Process.sequential,
    verbose=2
)

result = crew.kickoff(
    inputs={
        "job_description": "Python, ML, NLP, RAG...",
        "resume": "5 years Python, ML, NLP..."
    }
)

print(result)