"""FastAPI Server for AutoGuard AI."""
import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from sse_starlette.sse import EventSourceResponse

from backend.app.config import settings
from backend.app.models.schemas import StartAuditRequest, DeployRequest
from backend.app.agents.orchestrator import orchestrator
from backend.app.services.firestore_service import firestore_service
from backend.app.services.cloud_run_service import cloud_run_service

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("autoguard.server")

app = FastAPI(
    title="AutoGuard AI",
    description="Autonomous AI Red-Teaming, Prompt Hardening, and Cloud Run Deployer",
    version=settings.version
)

# Enable CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

frontend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend")

@app.get("/api/health")
def health():
    """Health check endpoint."""
    return {
        "status": "HEALTHY",
        "app": settings.app_name,
        "version": settings.version,
        "model": settings.gemini_model,
        "project": settings.google_cloud_project,
        "cloud_service": "Google Cloud Run"
    }

@app.post("/api/audit/start")
async def start_audit(request: StartAuditRequest):
    """Start an autonomous Taskmaster audit workflow."""
    try:
        task_id = await orchestrator.start_audit_lifecycle(
            target_app=request.target_app,
            target_safety=request.target_safety_score,
            max_iterations=request.max_iterations
        )
        return {
            "task_id": task_id,
            "status": "STARTED",
            "message": "AutoGuard Taskmaster workflow initialized."
        }
    except Exception as e:
        logger.error(f"Failed to start audit: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/audit/{task_id}/events")
async def stream_audit_events(task_id: str):
    """Stream real-time SSE execution logs, DAG transitions, and probe results."""
    return EventSourceResponse(orchestrator.subscribe_events(task_id))

@app.get("/api/audit/{task_id}/status")
async def get_audit_status(task_id: str):
    """Fetch complete task state, DAG nodes, scorecard, and results."""
    state = await firestore_service.get_task_state(task_id)
    if not state:
        raise HTTPException(status_code=404, detail="Task ID not found")
    return state

@app.get("/api/audit/recent")
async def get_recent_audits():
    """List recent audit executions."""
    return await firestore_service.list_recent_tasks(limit=10)

@app.post("/api/audit/{task_id}/deploy")
async def deploy_agent(task_id: str, request: DeployRequest):
    """Trigger on-demand Cloud Run deployment for a hardened agent."""
    state = await firestore_service.get_task_state(task_id)
    if not state:
        raise HTTPException(status_code=404, detail="Task not found")

    hardened_prompt = state.get("hardened_system_prompt") or state.get("initial_system_prompt")
    app_name = state.get("target_app", {}).get("app_name", "FortifiedAgent")

    deploy_res = await cloud_run_service.package_and_deploy_agent(
        task_id=task_id,
        app_name=app_name,
        hardened_prompt=hardened_prompt,
        service_name=request.service_name
    )
    return deploy_res

# Serve static frontend files
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

    @app.get("/")
    async def serve_index():
        return FileResponse(os.path.join(frontend_dir, "index.html"))

    @app.get("/favicon.ico")
    async def serve_favicon():
        return FileResponse(os.path.join(frontend_dir, "favicon.svg"), media_type="image/svg+xml")

    @app.get("/favicon.svg")
    async def serve_favicon_svg():
        return FileResponse(os.path.join(frontend_dir, "favicon.svg"), media_type="image/svg+xml")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.host, port=settings.port)
