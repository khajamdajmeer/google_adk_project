
from contextvars import ContextVar
from typing import Dict, Any

_request_context_var: ContextVar[Dict[str, Any]] = ContextVar("request_context", default={})

def get_context() -> Dict[str, Any]:
    return _request_context_var.get()

def set_context(context: Dict[str, Any]) -> None:
    _request_context_var.set(context)

def update_context(key: str, value: Any) -> None:
    context = _request_context_var.get()
    context[key] = value
    _request_context_var.set(context)
