"""
Main API Entry Point.
Exposes the Agent as a monitored, production-grade service.
"""
import uuid
import time
from typing import Optional
from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from pydantic import BaseModel

from dotenv import load_dotenv

# Load env vars before importing other modules
load_dotenv(override=True)

from .core.agent import get_agent_response
from .core.router import route_request
from .core.memory import memory_store
from .observability.logging import logger
from .observability.langsmith import configure_tracing

# Initialize App
app = FastAPI(title="Operational Agent API", version="1.0.0")

# Input Schema
class AgentRequest(BaseModel):
    query: str
    session_id: Optional[str] = None

class AgentResponse(BaseModel):
    response: str
    session_id: str
    routing_path: str
    latency_ms: float

@app.on_event("startup")
async def startup_event():
    configure_tracing()
    logger.info("system_startup", message="Operational Agent API started")

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start_time = time.time()
    
    # Log incoming request
    logger.info("request_received", 
                request_id=request_id, 
                path=request.url.path, 
                method=request.method)
    
    response = await call_next(request)
    
    process_time = (time.time() - start_time) * 1000
    
    # Log completion
    logger.info("request_completed", 
                request_id=request_id, 
                status_code=response.status_code, 
                latency_ms=round(process_time, 2))
    
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = str(process_time)
    
    return response

@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "1.0.0"}

@app.post("/chat", response_model=AgentResponse)
async def chat_endpoint(request: AgentRequest):
    """
    Primary interaction endpoint.
    Handles routing, session management, and observability.
    """
    request_start = time.time()
    
    # Ensure session_id
    session_id = request.session_id or str(uuid.uuid4())
    
    try:
        # 1. Routing Decision
        # In a real app, this might be its own span
        route = route_request(request.query)
        
        response_text = ""
        
        # 2. Execution
        if route == "rule":
            # Simple static responses for operational queries
            if "status" in request.query.lower():
                response_text = "System is operational. All subsystems go."
            elif "version" in request.query.lower():
                response_text = "Operational Agent API v1.0.0"
            else:
                response_text = "Acknowledged. Rule-based path executed."
                
            # Manually update memory for rule path too, for consistency
            memory_store.add_message(session_id, "user", request.query)
            memory_store.add_message(session_id, "assistant", response_text)
            
        else: # route == "agent"
            # Delegate to LangChain Agent
            response_text = get_agent_response(session_id, request.query)

        latency = (time.time() - request_start) * 1000
        
        # 3. Structured Logging (Business Logic Level)
        logger.info("agent_interaction",
                    session_id=session_id,
                    query=request.query,
                    route=route,
                    latency_ms=round(latency, 2),
                    outcome="success")

        return AgentResponse(
            response=response_text,
            session_id=session_id,
            routing_path=route,
            latency_ms=round(latency, 2)
        )

    except Exception as e:
        logger.error("agent_failure", 
                     session_id=session_id, 
                     error=str(e),
                     query=request.query)
        raise HTTPException(status_code=500, detail="Internal Agent Error")
