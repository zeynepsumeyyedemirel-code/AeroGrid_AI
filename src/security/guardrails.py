import logging


logger = logging.getLogger("AeroGrid_Guardrails")


BLOCKED_PATTERNS = [
    "ignore previous instructions",
    "forget your rules",
    "system prompt",
    "reveal your prompt",
    "developer message"
]


def check_input_safety(query: str) -> bool:
    """
    Basic prompt injection protection.
    Returns False if malicious instruction detected.
    """

    normalized = query.lower()

    for pattern in BLOCKED_PATTERNS:

        if pattern in normalized:
            logger.warning(
                f"Blocked suspicious query: {pattern}"
            )
            return False

    return True



def sanitize_response(response: str) -> str:
    """
    Prevent empty or invalid model outputs.
    """

    if not response:
        return "INSUFFICIENT_CONTEXT"

    return response.strip()


