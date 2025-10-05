from app.core.logging import get_logger
from fastapi import FastAPI,Response,Body,Depends
from fastapi import Header,HTTPException
from app.memory.in_memory import session_manager, memory_runner
from app.db.session import get_db
from app.agents.orch_agent import get_orchestrator_agent
from app.llm.client import run_client_coordiator
logger = get_logger(__name__, log_file="logs/app.log")
logger.info("App started")


from contextvars import ContextVar
current_user: ContextVar[dict | None] = ContextVar("current_user", default=None)

from app.core.middleware import RequestContextMiddleware
from app.core.context import get_context
from app.api.v1.router import api_router

root_agent = get_orchestrator_agent()

# Keep a default runner around for generic endpoints or backwards compatibility
runner = memory_runner(root_agent)
app = FastAPI()
app.add_middleware(RequestContextMiddleware)

# Expose REST endpoints
app.include_router(api_router, prefix="/api/v1")


def get_patient_id(patient_id : str = Header(...,alias="authtoken")) :

    print("PATIENT ID:", patient_id, flush=True)
    if not patient_id:
        raise HTTPException(status_code=401, detail="patient id missing in the header")
    current_user.set({"patient_id":patient_id})
    return {"patient_id": patient_id}


@app.get('/status_check')
async def status_check():
    status = {}
    try:
        status['active_sessions'] = list(session_manager.active_runners.keys())
        status['db_status'] = get_db()
        status['request_context'] = get_context()
    except Exception as e:
        logger.error(f"{e}")
    return {'status' : status}

@app.get('/health')
async def health_check():
    try:
        status = {'status':200, 'api':"api is live and kicking"}
        res = await status_check()
        return {"status":status,"res":res}
    except Exception as e:
        return {'error': 'e'}

@app.post("/chat")
def chat(patient_id= Depends(get_patient_id),request: str = Body(...)):
    try:
        logger.info('/chat called')
        
        # Extract patient ID string from the Dependency return value
        patient_id_str = patient_id.get("patient_id") if isinstance(patient_id, dict) else str(patient_id)
        
        # Use patient_id as the session ID for memory isolation
        session_id = patient_id_str
        
        request = request + f" patient_id = {patient_id_str}"
        
        # Get or create an isolated runner for this session
        session_runner = session_manager.get_or_create_runner(session_id, root_agent)
        
        res = run_client_coordiator(session_runner, request, session_id=session_id, user_id=patient_id_str)
        return {"response": res}
    except Exception as e:
        logger.error(f"Error in /chat endpoint: {e}")
        return {"error": str(e)}