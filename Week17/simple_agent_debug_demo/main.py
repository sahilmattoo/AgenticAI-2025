"""
FastAPI entry point for the IT Support Agent.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from core.agent import simple_agent
from core.logger import log_to_file

app = FastAPI(title="IT Support Agent API", version="1.0.0")
log_to_file("IT Support Agent API server starting up")

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    query: str
    response: str
    status: str

@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "healthy", "message": "IT Support Agent API is running"}

@app.post("/predict", response_model=QueryResponse)
async def predict(request: QueryRequest):
    """Predict endpoint to handle agent queries."""
    try:
        log_to_file(f"API Request received: {request.query}")
        agent_response = simple_agent(request.query)
        
        status = "success"
        if "Agent failed" in agent_response:
            status = "error"
            
        return QueryResponse(
            query=request.query,
            response=agent_response,
            status=status
        )
    except Exception as e:
        log_to_file(f"API Error: {str(e)}", error=True)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
