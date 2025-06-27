# Agentic AI Healthcare Backend

This project is a backend system for a Healthcare Practice, powered by **Agentic AI** using the **Google Agent Development Kit (ADK)** and the `gemini-2.0-flash` model.

It provides a multi-agent architecture to intelligently route patient queries and execute specialized tasks related to appointments, billing, and claims.

## Architecture

The backend is built with **FastAPI** and leverages a centralized **Orchestrator Agent** to manage incoming user requests. The orchestrator delegates tasks to specialized sub-agents:

- **Orchestrator Agent**: The central routing agent that understands the user's intent and delegates requests to the appropriate specialist agent.
- **Appointment Agent**: Handles appointment scheduling, querying availability, and managing patient appointments.
- **Billing Agent**: Manages queries related to patient invoices, payment status, and general billing questions.
- **Claims Agent**: Handles insurance claims, status checks, and claims processing questions.

Each agent is equipped with specific tools and prompts to execute its tasks effectively.

## Project Structure

```text
google_adk/
├── app/
│   ├── agents/
│   │   ├── appointment_agent.py   # Appointment scheduling agent
│   │   ├── billing_agent.py       # Billing queries agent
│   │   ├── claims_agent.py        # Insurance claims agent
│   │   └── orch_agent.py          # Orchestrator routing agent
│   ├── core/                      # Core configs & Middlewares
│   ├── db/                        # Database Sessions
│   ├── llm/                       # LLM templates, prompts, and client code
│   ├── memory/                    # In-memory session runner configurations
│   ├── tools/                     # Tool definitions for agents
│   └── main.py                    # FastAPI application entry point
```

## Setup & Execution

### Prerequisites
- Python 3.9+
- Google ADK (`google.adk`)
- FastAPI (`fastapi`)
- Uvicorn (`uvicorn`) for running the server

### Environment Variables
Ensure you have the required API keys set in your environment (e.g., `GEMINI_API_KEY` for Google ADK LLM access).

### Running the Server

Start the FastAPI server using Uvicorn:

```bash
uvicorn google_adk.app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### `GET /health`
Checks the health and status of the API, in-memory runner, database, and request context.

**Response:**
```json
{
  "status": {
    "status": 200,
    "api": "api is live and kicking"
  },
  "res": { ... }
}
```

### `POST /chat`
The main entry point for conversational interactions with the Agentic AI.

**Headers:**
- `authtoken` (Required): Acts as the `patient_id` for context and verification.

**Body:**
- `request`: The text query from the user.

**Example Request:**
```json
{
  "request": "Can you check the status of my recent insurance claim?"
}
```

**Response:**
```json
{
  "response": "Your claim is currently under review..."
}
```

## Logging
Logs are saved locally inside `google_adk/app/logs/app.log`.

## Database & Memory
- Context is managed locally using context variables and the FastApi Request Context Middleware.
- Interaction history and multi-step tasks are resolved inside the Google ADK `memory_runner`.
