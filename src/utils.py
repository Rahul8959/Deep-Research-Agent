import time
from functools import wraps

def timed(label: str):
    def deco(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            t0 = time.perf_counter()
            print(f"[START] {label}")
            try:
                return fn(*args, **kwargs)
            finally:
                dt = time.perf_counter() - t0
                print(f"[DONE ] {label} ({dt:.2f}s)")
        return wrapper
    return deco

def extract_text_from_message(msg) -> str:
    content = msg.content
    if isinstance(content, str): return content
    if isinstance(content, list):
        return "".join(part.get("text", "") for part in content if isinstance(part, dict) and part.get("type") == "text")
    return str(content)

def _coerce_text(value) -> str:
    """Normalize streaming content (None | str | list[block] | other) into a plain string."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        parts = []
        for block in value:
            if isinstance(block, dict):
                parts.append(block.get("text") or block.get("thinking") or "")
            elif isinstance(block, str):
                parts.append(block)
        return "".join(parts)
    return str(value)