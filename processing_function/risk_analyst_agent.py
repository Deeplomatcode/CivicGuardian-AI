"""
Compatibility wrapper for legacy imports used by tests.
Exports the same symbols as src.risk_analyst_agent AND exposes exponential_backoff_retry
at this module path because unit tests patch it here.
"""
from src.risk_analyst_agent import (
    analyze_risk,
    _build_risk_analysis_prompt,
    _parse_bedrock_response,
    _get_default_value,
)

# Tests patch processing_function.risk_analyst_agent.exponential_backoff_retry
# even if the real implementation imports it from retry_handler.
from src.retry_handler import exponential_backoff_retry

__all__ = [
    "analyze_risk",
    "_build_risk_analysis_prompt",
    "_parse_bedrock_response",
    "_get_default_value",
    "exponential_backoff_retry",
]
