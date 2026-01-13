"""
Model Collapse Simulator
Reproduces the experiment in Section 4.2 of the SSA v4.0 paper.
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import entropy

class ModelCollapseSimulator:
    def __init__(self, vocab_size=2000, zipf_param=1.5):
        self.vocab_size = vocab_size
        # Generate Ground Truth (Human) Distribution using Zipf's Law
        ranks = np.arange(1, vocab_size + 1)
        weights = 1.0 / (ranks ** zipf_param)
        self.human_dist = weights / weights.sum()
        self.current_dist = self.human_dist.copy()
        
    def step(self, sample_size=3000, smoothing=0.01):
        """Simulate one generation of AI training on its own output."""
        # 1. Generate synthetic data from current distribution
        samples = np.random.choice(
            self.vocab_size, size=sample_size, p=self.current_dist
        )
        
        # 2. Train new model (Estimate new distribution)
        counts = np.bincount(samples, minlength=self.vocab_size)
        counts = counts + smoothing # Laplace smoothing
        self.current_dist = counts / counts.sum()
        
        return self.current_dist

    def run_experiment(self, generations=15, ssa_injection_rate=0.0, analog_weight=1.0):
        """
        Run the recursive training loop.
        
        Args:
            ssa_injection_rate: Percentage of fresh human data (0.0 - 1.0)
            analog_weight: Weight multiplier for human data (W(x) influence)
        """
        self.current_dist = self.human_dist.copy()
        diversity_history = [entropy(self.current_dist, base=2)]
        
        for _ in range(generations):
            # AI learns from previous generation
            ai_dist = self.step()
            
            # SSA Logic: Injection of Analog-Weighted Human Data
            if ssa_injection_rate > 0:
                effective_weight = ssa_injection_rate * analog_weight
                # Mix AI data with weighted Human data
                # Note: Simplified mixing logic for simulation
                mixed_dist = (
                    (1 - effective_weight) * ai_dist + 
                    effective_weight * self.human_dist
                )
                # Re-normalize
                mixed_dist /= mixed_dist.sum()
                self.current_dist = mixed_dist
            else:
                self.current_dist = ai_dist
                
            diversity_history.append(entropy(self.current_dist, base=2))
            
        return diversity_history

def plot_results(results_dict):
    """Generates the plot style matching the paper."""
    plt.figure(figsize=(10, 6))
    
    gens = range(len(results_dict['collapse']))
    
    plt.plot(gens, results_dict['collapse'], 'r--o', label='Scenario A: Collapse (Synthetic Only)')
    plt.plot(gens, results_dict['baseline'], 'b-^', label='Scenario B: 50% Human (Unweighted)')
    plt.plot(gens, results_dict['ssa'], 'g-s', linewidth=2, label='Scenario C: SSA 10% (Analog Weighted)')
    
    plt.title('SSA v4.0 Experimental Results: Prevention of Model Collapse')
    plt.xlabel('Training Generation')
    plt.ylabel('Semantic Diversity (Shannon Entropy)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.savefig('model_collapse_results.png')
    print("Graph saved as 'model_collapse_results.png'")
