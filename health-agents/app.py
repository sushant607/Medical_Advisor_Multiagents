from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from main import HealthAgentNetwork
import json

app = FastAPI(title="7 AI Health Agents Network")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")
network = HealthAgentNetwork()

class ProcessRequest(BaseModel):
    agent_type: str
    user_input: str
    context: Optional[Dict[str, Any]] = {}
    data_type: Optional[str] = None

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/process")
async def process_health_data(request: ProcessRequest):
    """Process health data through appropriate AI agents"""
    try:
        if request.agent_type == "psychology":
            result = network.agents['psychology'].analyze_behavioral_patterns(
                request.user_input,
                request.context
            )
            return {
                "response": json.dumps(result, indent=2),
                "agents_used": ["Psychology"]  # Always return array
            }
        
        elif request.agent_type == "orchestrator":
            result = network.agents['orchestrator'].analyze_and_route(
                request.user_input,
                request.context
            )
            # Ensure agents_involved is always an array
            agents_involved = result.get("agents_involved", [])
            if isinstance(agents_involved, str):
                agents_involved = [agents_involved]
            elif not isinstance(agents_involved, list):
                agents_involved = []
            
            return {
                "response": json.dumps(result, indent=2),
                "agents_used": ["Orchestrator"] + agents_involved
            }
        
        elif request.agent_type == "h3o":
            result = network.agents['h3o'].process(request.user_input, request.context)
            return {
                "response": result,
                "agents_used": ["H3O"]  # Always return array
            }
        
        elif request.agent_type == "dayone":
            result = network.agents['dayone'].process(request.user_input, request.context)
            return {
                "response": result,
                "agents_used": ["DayOne"]  # Always return array
            }
        
        elif request.agent_type == "mha":
            result = network.agents['mha'].process(request.user_input, request.context)
            return {
                "response": result,
                "agents_used": ["MHA"]  # Always return array
            }
        
        elif request.agent_type == "vpc":
            result = network.agents['vpc'].process(request.user_input, request.context)
            return {
                "response": result,
                "agents_used": ["VPC"]  # Always return array
            }
        
        elif request.agent_type == "precision_med":
            result = network.agents['precision_med'].process(request.user_input, request.context)
            return {
                "response": result,
                "agents_used": ["Precision Medicine"]  # Always return array
            }
        
        else:  # general
            result = network.process_user_input(request.user_input, request.data_type)
            
            # Ensure agents_used is always an array
            try:
                agents_used = network.router.get_agents_for_input(
                    request.data_type or network.router.classify_input(request.user_input)
                )
                # Handle case where get_agents_for_input returns a string
                if isinstance(agents_used, str):
                    agents_used = [agents_used]
                elif not isinstance(agents_used, list):
                    agents_used = ["General"]
            except Exception:
                agents_used = ["General"]
            
            return {
                "response": result,
                "agents_used": agents_used
            }
    
    except Exception as e:
        return {
            "error": f"Processing error: {str(e)}",
            "agents_used": ["Error"]  # Always return array
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)