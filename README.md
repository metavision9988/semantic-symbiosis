# Semantic Symbiosis Architecture (SSA) v4.0

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Paper Version](https://img.shields.io/badge/Paper-v4.0-blue.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)

> "Machines process results. Humans ARE process." — Mephisto Void

## 📖 Overview
**Semantic Symbiosis** is a unified framework for AGI alignment via analog signal integration. This repository contains the reference implementation of **SSA v4.0**, proving that injecting human "process costs" (hesitation, revision, struggle) into AI training prevents **Model Collapse**.

This codebase implements the core metrics and simulation experiments described in the paper:
* **Temporal Intentionality $T(t)$**: Quantifying cognitive rhythm.
* **Work Function $W(x)$**: Measuring thermodynamic cost of creation.
* **Semantic Entropy $H_{sem}$**: Process-aware information density.

## 🚀 Installation

```bash
git clone [https://github.com/metavision9988/semantic-symbiosis.git](https://github.com/metavision9988/semantic-symbiosis.git)
cd semantic-symbiosis
pip install -r requirements.txt

🧪 Usage
1. Run Model Collapse Simulation
Reproduce the findings from Figure 5 of the paper (15-generation recursive training).

Bash

python run_simulation.py
Output: Generates model_collapse_results.png comparing baseline vs. SSA.

2. Calculate Core Metrics
Use the library to measure the "humanness" of a text input stream.

Python

from src.metrics import calculate_temporal_intentionality, calculate_work_function

# Example: A user types "hello" with some hesitation
keystroke_times = [0.0, 0.2, 0.4, 1.5, 1.7, 1.9] # Seconds
T_score = calculate_temporal_intentionality(keystroke_times)

print(f"Temporal Intentionality T(t): {T_score:.4f}")
# Result < 0.2 indicates automation, 0.3-0.8 indicates human cognition
📜 Citation
If you use this framework in your research, please cite:

코드 스니펫

@article{void2026semantic,
  title={Semantic Symbiosis: A Unified Framework for AGI Alignment via Analog Signal Integration},
  author={Void, Mephisto},
  journal={VOID PRESS Technical Papers},
  version={4.0},
  year={2026},
  url={[https://github.com/metavision9988/semantic-symbiosis](https://github.com/metavision9988/semantic-symbiosis)}
}
🛡️ License
This project is licensed under the MIT License - see the LICENSE file for details.


5.  **Commit changes...** 버튼을 눌러 저장합니다.

---

### 3. `run_simulation.py` 만들기 (메인 실행 파일)
이 파일도 `src` 폴더 안이 아니라 **바깥쪽(Root)**에 있어야 합니다. 그래야 `README`에 적힌 사용법(`python run_simulation.py`)대로 작동합니다.

1.  메인 화면에서 **[Add file]** -> **[Create new file]**.
2.  파일 이름: `run_simulation.py`
3.  내용 (아까 드린 코드):

```python
"""
Main Execution Script for SSA v4.0 Simulation
"""
from src.simulation import ModelCollapseSimulator, plot_results

def main():
    print("Initializing SSA v4.0 Simulation...")
    sim = ModelCollapseSimulator()
    generations = 15
    
    # Scenario A: Full Collapse (100% Synthetic)
    print("Running Scenario A: Recursive Collapse...")
    res_a = sim.run_experiment(generations=generations, ssa_injection_rate=0.0)
    
    # Scenario B: Baseline Mix (50% Human, Unweighted)
    # Even with 50% human data, if unweighted, it degrades slowly.
    print("Running Scenario B: 50% Mix (Unweighted)...")
    res_b = sim.run_experiment(generations=generations, ssa_injection_rate=0.5, analog_weight=1.0)
    
    # Scenario C: SSA (10% Human, High Analog Weight)
    # 10% data with 1.5x weight (simulating high W(x))
    print("Running Scenario C: SSA 10% (Analog Weighted)...")
    res_c = sim.run_experiment(generations=generations, ssa_injection_rate=0.1, analog_weight=5.0)
    
    # Plot
    results = {
        'collapse': res_a,
        'baseline': res_b,
        'ssa': res_c
    }
    plot_results(results)
    print("Done.")

if __name__ == "__main__":
    main()
