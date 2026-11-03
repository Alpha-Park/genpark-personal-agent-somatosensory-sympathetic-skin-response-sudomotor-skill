"""
Somatosensory Sympathetic Skin Response (SSR) & Sudomotor Autonomic Reflex Client.
Zero-mock pure Python standard library implementation.
Calculates Palmar and Plantar SSR Onset Latency (seconds), Peak-to-Peak Amplitude (mV),
Habituation Index (% drop), and small-fiber sudomotor dysautonomia staging.
"""

import math
from typing import Dict, Any, Optional


class SympatheticSkinResponseClient:
    """
    Evaluates postganglionic unmyelinated sympathetic C-fiber and eccrine sudomotor function:
    - Palmar Latency (s): normal 1.20 to 1.60 s
    - Plantar Latency (s): normal 1.80 to 2.20 s
    - Plantar-to-Palmar Latency Delta (s): normal 0.50 to 0.80 s
    - Peak-to-Peak Amplitude (mV): normal >= 1.0 mV (palm), >= 0.5 mV (sole)
    - Habituation Index (HI%): A5 / A1 * 100 (normal < 50% habituation)
    - Differentiates peripheral autonomic neuropathy from sympathetic hyperexcitability.
    """

    def __init__(self):
        pass

    def evaluate_ssr(
        self,
        palmar_latency_seconds: float,
        palmar_amplitude_mv: float,
        plantar_latency_seconds: Optional[float] = None,
        plantar_amplitude_mv: Optional[float] = None,
        amplitude_trial_5_mv: Optional[float] = None,
        patient_age_years: Optional[int] = 40,
        limb_temperature_c: Optional[float] = 32.5
    ) -> Dict[str, Any]:
        """
        Calculates Sympathetic Skin Response (SSR) metrics.
        palmar_latency_seconds: palmar onset latency in seconds (e.g. 1.38 s).
        palmar_amplitude_mv: palmar peak-to-peak amplitude in mV (e.g. 2.2 mV).
        plantar_latency_seconds: plantar onset latency in seconds (optional, e.g. 1.95 s).
        plantar_amplitude_mv: plantar peak-to-peak amplitude in mV (optional, e.g. 0.9 mV).
        """
        if palmar_latency_seconds < 0 or palmar_amplitude_mv < 0:
            raise ValueError("Latency and amplitude cannot be negative.")

        # Check for complete absence of response
        is_palmar_absent = (palmar_amplitude_mv == 0.0 or palmar_latency_seconds == 0.0)
        is_plantar_absent = (plantar_amplitude_mv == 0.0 or plantar_latency_seconds == 0.0) if plantar_amplitude_mv is not None else None

        # Plantar-Palmar Latency Gradient
        latency_gradient_s = None
        if plantar_latency_seconds and palmar_latency_seconds and not is_palmar_absent and not is_plantar_absent:
            latency_gradient_s = round(plantar_latency_seconds - palmar_latency_seconds, 2)

        # Habituation Ratio (A5 / A1 * 100)
        habituation_ratio_pct = None
        if amplitude_trial_5_mv is not None and palmar_amplitude_mv > 0:
            habituation_ratio_pct = round((amplitude_trial_5_mv / palmar_amplitude_mv) * 100.0, 1)

        # Clinical Autonomic Neuropathy Staging (American Academy of Neurology standards):
        # Normal Palmar: Latency 1.20 - 1.60 s, Amplitude >= 1.0 mV
        # Normal Plantar: Latency 1.80 - 2.25 s, Amplitude >= 0.5 mV
        if is_palmar_absent or (is_plantar_absent is True):
            autonomic_status = "Absent Sympathetic Skin Response (Definite Sudomotor Neuropathy)"
            clinical_risk = "Complete loss of eccrine gland sympathetic sudomotor innervation; strongly indicates small-fiber autonomic polyneuropathy (diabetic, amyloid, or pure autonomic failure)."
        elif palmar_latency_seconds > 1.75 or (plantar_latency_seconds and plantar_latency_seconds > 2.40):
            autonomic_status = "Prolonged SSR Latency (Unmyelinated C-Fiber Conduction Delay)"
            clinical_risk = "Delayed central or postganglionic sympathetic conduction velocity; early subclinical autonomic neuropathy."
        elif palmar_amplitude_mv < 0.6 or (plantar_amplitude_mv and plantar_amplitude_mv < 0.3):
            autonomic_status = "Attenuated SSR Amplitude (Partial Sudomotor Denervation)"
            clinical_risk = "Reduced synchronized sweat gland synchronous depolarization; partial distal autonomic axonal degeneration."
        elif habituation_ratio_pct and habituation_ratio_pct > 80.0:
            autonomic_status = "Sympathetic Hyperexcitability / Failure of Habituation"
            clinical_risk = "Intact sudomotor efferents with impaired central autonomic habituation; seen in sympathetic hyperarousal states."
        else:
            autonomic_status = "Normal Physiological Sympathetic Skin Response"
            clinical_risk = "Preserved postganglionic cholinergic sympathetic transmission and healthy peripheral sudomotor reflex arc."

        return {
            "status": "success",
            "ssr_kinetics": {
                "palmar_latency_seconds": round(palmar_latency_seconds, 2) if not is_palmar_absent else None,
                "palmar_amplitude_mv": round(palmar_amplitude_mv, 2),
                "plantar_latency_seconds": round(plantar_latency_seconds, 2) if (plantar_latency_seconds and not is_plantar_absent) else None,
                "plantar_amplitude_mv": round(plantar_amplitude_mv, 2) if plantar_amplitude_mv is not None else None,
                "plantar_palmar_latency_gradient_s": latency_gradient_s,
                "habituation_ratio_pct": habituation_ratio_pct
            },
            "recording_context": {
                "patient_age_years": patient_age_years,
                "limb_temperature_c": limb_temperature_c
            },
            "autonomic_assessment": {
                "autonomic_status": autonomic_status,
                "pathophysiology_summary": clinical_risk
            }
        }
