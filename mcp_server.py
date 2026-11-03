"""
MCP Server implementation for Somatosensory Sympathetic Skin Response (SSR) & Sudomotor Autonomic Reflex Skill.
Exposes standard FastMCP-compatible tools for postganglionic sympathetic autonomic reflex assessment.
"""

import sys
import json
from typing import Dict, Any, Optional
from client import SympatheticSkinResponseClient


def evaluate_sympathetic_skin_response(
    palmar_latency_seconds: float,
    palmar_amplitude_mv: float,
    plantar_latency_seconds: Optional[float] = None,
    plantar_amplitude_mv: Optional[float] = None,
    amplitude_trial_5_mv: Optional[float] = None,
    patient_age_years: Optional[int] = 40,
    limb_temperature_c: Optional[float] = 32.5
) -> str:
    """
    Evaluates Sympathetic Skin Response (SSR) latency, amplitude, and habituation.
    Returns structured analysis of sudomotor autonomic reflex arc.
    """
    client = SympatheticSkinResponseClient()
    result = client.evaluate_ssr(
        palmar_latency_seconds=palmar_latency_seconds,
        palmar_amplitude_mv=palmar_amplitude_mv,
        plantar_latency_seconds=plantar_latency_seconds,
        plantar_amplitude_mv=plantar_amplitude_mv,
        amplitude_trial_5_mv=amplitude_trial_5_mv,
        patient_age_years=patient_age_years,
        limb_temperature_c=limb_temperature_c
    )
    return json.dumps(result, indent=2)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--tools":
        tools = [
            {
                "name": "evaluate_sympathetic_skin_response",
                "description": "Quantifies palmar and plantar sympathetic skin response (SSR) latency, amplitude, habituation, and sudomotor autonomic neuropathy staging.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "palmar_latency_seconds": {"type": "number", "description": "Palmar SSR onset latency in seconds (normal: 1.20 - 1.60 s)"},
                        "palmar_amplitude_mv": {"type": "number", "description": "Palmar peak-to-peak amplitude in mV (normal >= 1.0 mV)"},
                        "plantar_latency_seconds": {"type": "number", "description": "Optional plantar SSR latency in seconds (normal: 1.80 - 2.25 s)"},
                        "plantar_amplitude_mv": {"type": "number", "description": "Optional plantar peak-to-peak amplitude in mV (normal >= 0.5 mV)"},
                        "amplitude_trial_5_mv": {"type": "number", "description": "Optional 5th stimulus trial amplitude in mV to evaluate habituation ratio"},
                        "patient_age_years": {"type": "integer", "description": "Patient age in years (default: 40)"},
                        "limb_temperature_c": {"type": "number", "description": "Limb skin temperature in Celsius (normal: >= 32.0 C)"}
                    },
                    "required": ["palmar_latency_seconds", "palmar_amplitude_mv"]
                }
            }
        ]
        print(json.dumps(tools, indent=2))
    else:
        # Simple self-test
        client = SympatheticSkinResponseClient()
        test_res = client.evaluate_ssr(
            palmar_latency_seconds=1.38,
            palmar_amplitude_mv=2.2,
            plantar_latency_seconds=1.95,
            plantar_amplitude_mv=0.9
        )
        print("Self-test passed:")
        print(json.dumps(test_res, indent=2))
