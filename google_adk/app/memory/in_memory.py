from typing import Dict, Any
from google.adk.runners import InMemoryRunner
from app.core.logging import get_logger

logger = get_logger(__name__, log_file="logs/app.log")

class SessionMemoryManager:
    def __init__(self):
        self.active_runners: Dict[str, InMemoryRunner] = {}

    def get_or_create_runner(self, session_id: str, agent: Any) -> InMemoryRunner:
        if session_id not in self.active_runners:
            logger.info(f"Creating new InMemoryRunner for session: {session_id}")
            self.active_runners[session_id] = InMemoryRunner(agent)
        else:
            logger.info(f"Using existing InMemoryRunner for session: {session_id}")
        return self.active_runners[session_id]

    def remove_runner(self, session_id: str):
        if session_id in self.active_runners:
            logger.info(f"Removing InMemoryRunner for session: {session_id}")
            del self.active_runners[session_id]

    def clear_all(self):
        logger.info("Clearing all InMemoryRunners")
        self.active_runners.clear()

session_manager = SessionMemoryManager()

def memory_runner(agent):
    logger.warning("Using legacy single-instance memory runner")
    runner = InMemoryRunner(agent)
    return runner
