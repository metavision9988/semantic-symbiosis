"""
Core Metrics Implementation for SSA v4.0
References: Section 3.3.1 (Temporal Intentionality) and 3.3.2 (Work Function)
"""
import numpy as np
from typing import List, Optional

def calculate_temporal_intentionality(keystroke_times: List[float]) -> float:
    """
    Calculates T(t): Temporal Intentionality Score.
    
    Formula: T(t) = CV(dt) * Burst_Factor * Pause_Weight
    
    Args:
        keystroke_times: List of timestamps (in seconds).
    Returns:
        float: Score typically between 0.0 and 2.0.
    """
    if len(keystroke_times) < 5:
        return 0.0  # Insufficient data
    
    # Calculate inter-keystroke intervals (flight time)
    intervals = np.diff(keystroke_times)
    
    # 1. Coefficient of Variation (CV)
    # Measures rhythm irregularity. Machines are uniform (low CV).
    mu = np.mean(intervals) + 1e-9
    sigma = np.std(intervals)
    cv = sigma / mu
    
    # 2. Burst Factor
    # Humans type in bursts. Ratio of fast intervals (<100ms) to total.
    burst_count = np.sum(intervals < 0.1)
    burst_factor = 1.0 + (burst_count / len(intervals))
    
    # 3. Pause Weight
    # Long pauses (>2s) indicate cognitive processing/hesitation.
    long_pauses = np.sum(intervals > 2.0)
    if long_pauses > 0:
        pause_weight = 1.0 + (np.log1p(long_pauses) * 0.1)
    else:
        # Penalty for robotic continuous typing
        pause_weight = 0.8
        
    T = cv * burst_factor * pause_weight
    return np.clip(T, 0.0, 2.0)


def calculate_work_function(
    content: str,
    edit_count: int,
    elapsed_time: float,
    pressure_avg: float = 1.0
) -> float:
    """
    Calculates W(x): Work Function (Thermodynamic Cost).
    
    Formula: W(x) = log(1 + E) * P_avg * (T_elapsed / T_expected)
    
    Args:
        content: Final text string.
        edit_count: Total backspaces/deletes used.
        elapsed_time: Total time taken (seconds).
        pressure_avg: Average key pressure (normalized 1.0 if unavailable).
    """
    # 1. Edit Factor (Logarithmic to prevent explosion)
    edit_factor = np.log1p(edit_count)
    if edit_factor == 0: 
        edit_factor = 0.5 # Baseline for perfect typing
        
    # 2. Time Factor (vs 60 WPM baseline)
    word_count = len(content.split())
    expected_time = (word_count / 60.0) * 60.0 # seconds
    if expected_time < 1: expected_time = 1
    
    time_factor = elapsed_time / expected_time
    
    # W(x) Calculation
    W = edit_factor * pressure_avg * time_factor
    
    return W
