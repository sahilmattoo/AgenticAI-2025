from fastapi import FastAPI, HTTPException
from app.schemas import ChatRequest, ChatResponse
from app.agent import agent, extract_final_answer

app = FastAPI(title="LangGraph Agentic API")

@app.get("/")
async def health():
    return {"status": "ResumeAnalyzer working"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        result = await agent.ainvoke({
            "messages": [
                {
                    "role": "user",
                    "content": request.message
                }
            ]
        })

        final_answer = extract_final_answer(result)

        return ChatResponse(
            session_id=request.session_id,
            response=final_answer
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

#uvicorn app.main:app --reload