"""
Example usage for Somatosensory Sympathetic Skin Response (SSR) & Sudomotor Autonomic Reflex Skill.
"""

from client import SympatheticSkinResponseClient


def main():
    client = SympatheticSkinResponseClient()

    print("--- Case 1: Normal Physiological Sympathetic Skin Response ---")
    normal_case = client.evaluate_ssr(
        palmar_latency_seconds=1.38,
        palmar_amplitude_mv=2.45,
        plantar_latency_seconds=1.95,
        plantar_amplitude_mv=0.88,
        amplitude_trial_5_mv=1.1,
        patient_age_years=35,
        limb_temperature_c=33.0
    )
    print("Palmar Latency:", normal_case["ssr_kinetics"]["palmar_latency_seconds"], "s")
    print("Plantar Latency:", normal_case["ssr_kinetics"]["plantar_latency_seconds"], "s")
    print("Plantar-Palmar Gradient:", normal_case["ssr_kinetics"]["plantar_palmar_latency_gradient_s"], "s")
    print("Habituation Ratio:", normal_case["ssr_kinetics"]["habituation_ratio_pct"], "%")
    print("Autonomic Status:", normal_case["autonomic_assessment"]["autonomic_status"])
    print("Pathophysiology:", normal_case["autonomic_assessment"]["pathophysiology_summary"])
    print()

    print("--- Case 2: Diabetic Small-Fiber Sudomotor Autonomic Neuropathy ---")
    neuropathy_case = client.evaluate_ssr(
        palmar_latency_seconds=0.0,
        palmar_amplitude_mv=0.0,
        plantar_latency_seconds=0.0,
        plantar_amplitude_mv=0.0,
        patient_age_years=58
    )
    print("Autonomic Status:", neuropathy_case["autonomic_assessment"]["autonomic_status"])
    print("Pathophysiology:", neuropathy_case["autonomic_assessment"]["pathophysiology_summary"])
    print()

    print("--- Case 3: Distal Unmyelinated C-Fiber Conduction Delay ---")
    delay_case = client.evaluate_ssr(
        palmar_latency_seconds=1.85,
        palmar_amplitude_mv=1.20,
        plantar_latency_seconds=2.55,
        plantar_amplitude_mv=0.55,
        patient_age_years=62
    )
    print("Autonomic Status:", delay_case["autonomic_assessment"]["autonomic_status"])
    print("Pathophysiology:", delay_case["autonomic_assessment"]["pathophysiology_summary"])


if __name__ == "__main__":
    main()
