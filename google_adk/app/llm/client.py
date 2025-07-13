
from google.genai import types
from google.adk.runners import InMemoryRunner
from app.core.logging import get_logger
import uuid
import asyncio
logger = get_logger(__name__, log_file="logs/app.log")



def run_client_coordiator(
    runner: InMemoryRunner,
    request: str,
    session_id: str,
    user_id: str = "user_123",
):
    if not session_id:
        session_id = str(uuid.uuid4())

    try: 
        asyncio.run(runner.session_service.create_session(
            app_name=runner.app_name,
            user_id=user_id,
            session_id=session_id
        ))
    except Exception as e:
        logger.info('trying to find session')

        asyncio.run(runner.session_service.get_session(
            app_name=runner.app_name,
            user_id=user_id,
            session_id=session_id,
        ))

    final_result = ""

    # events = await run_in_threadpool(
    #     runner.run,
    #     user_id=user_id,
    #     session_id=session_id,
    #     new_message=types.Content(
    #         role="user",
    #         parts=[types.Part(text=request)],
    #     ),
    # )

    # for event in events:
    for event in runner.run(
            user_id=user_id,
            session_id=session_id,
            new_message=types.Content(
                role='user',
                parts=[types.Part(text=request)]
            ),
        ):
        logger.info("inside the for loop for event")
        if event.is_final_response() and event.content:
            if getattr(event.content, "text", None):
                final_result = event.content.text
            elif event.content.parts:
                final_result = "".join(
                    part.text for part in event.content.parts if part.text
                )
            break

    return final_result
