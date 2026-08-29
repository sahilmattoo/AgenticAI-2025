from hr_agent import agent_executor

while True:

    query = input("Ask HR Assistant: ")

    if query.lower() in ["exit", "quit"]:
        break

    result = agent_executor.invoke({"input": query})

    print("\nFinal Answer:\n")
    print(result["output"])