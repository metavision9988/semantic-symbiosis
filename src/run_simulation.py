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
