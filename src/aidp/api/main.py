import uuid
import asyncio

from fastapi import BackgroundTasks, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from aidp.reasoning_engine.master_orchestrator import MasterOrchestrator
from aidp.platform.epistemic_logger import EpistemicLedger

app = FastAPI(title="AIDP - Artificial Intelligence Discovery Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DiscoveryRequest(BaseModel):
    query: str

class JobStatus(BaseModel):
    job_id: str
    status: str
    result: dict | None = None
    orchestration_logs: list[str] | None = None

jobs = {}
# Initialize the Prominent Orchestrator globally
orchestrator = MasterOrchestrator()

def run_discovery_task_sync(job_id: str, query: str):
    """Wrapper to run the async orchestrator inside FastAPI's sync background tasks."""
    async def _run():
        try:
            # Execute the prominent, end-to-end 20+ agent orchestration
            result_context = await orchestrator.execute_pipeline({"target": query})
            
            jobs[job_id]["status"] = "completed"
            jobs[job_id]["result"] = {
                "state": "SUCCESS",
                "hypothesis": query,
                "orchestration_data": result_context
            }
        except Exception as e:
            jobs[job_id]["status"] = "failed"
            jobs[job_id]["result"] = {"error": str(e)}
            
    # Run the async loop
    asyncio.run(_run())

@app.post("/api/discovery", response_model=JobStatus)
def start_discovery(request: DiscoveryRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    jobs[job_id] = {
        "status": "running", 
        "result": None,
        "orchestration_logs": ["Initializing Prominent Orchestrator...", f"Loaded {len(orchestrator.agents)} advanced agents."]
    }
    background_tasks.add_task(run_discovery_task_sync, job_id, request.query)
    return {"job_id": job_id, "status": "running"}

@app.get("/api/discovery/{job_id}", response_model=JobStatus)
def get_discovery_status(job_id: str):
    return jobs.get(job_id, {"job_id": job_id, "status": "not_found", "result": None})

from fastapi.responses import StreamingResponse

@app.get("/api/discovery/{job_id}/stream")
async def stream_orchestrator(job_id: str, query: str):
    async def event_generator():
        try:
            # We will use the actual orchestrator to yield tokens and logs
            async for chunk in orchestrator.execute_pipeline_stream({"target": query}):
                yield f"data: {chunk}\n\n"
            
            jobs[job_id] = jobs.get(job_id, {})
            jobs[job_id]["status"] = "completed"
            yield f"data: [DONE]\n\n"
        except Exception as e:
            yield f"data: [ERROR] {str(e)}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.get("/api/ledger")
def get_ledger():
    ledger = EpistemicLedger()
    claims = ledger.get_all_claims()
    return {"claims": [c.model_dump() for c in claims]}
