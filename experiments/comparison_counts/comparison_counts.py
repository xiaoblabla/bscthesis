import matplotlib.pyplot as plt
import random
from .algorithms_modified import proxy_problem_unoptimized, proxy_problem

def measure_comparisons(algorithm, n, m, weights, distances):
    result, comparison_count = algorithm(n, m, weights, distances)
    return result, comparison_count

def generate_random_data(n):
    distances = [random.randint(1, 100) for _ in range(n)] 
    weights = [random.randint(1, 100) for _ in range(n)]
    return distances, weights

def compare_algorithms():
    n_values = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150]  
    m = 10
    distances, weights = generate_random_data(max(n_values))

    # Define algorithms to compare
    algorithms = [
        ("Unoptimized DP", proxy_problem_unoptimized),
        ("SMAWK with Lookup", proxy_problem)
    ]
    
    comparisons = {name: [] for name, _ in algorithms}
    theoretical_n2m = [n**2 * m for n in n_values]  # Theoretical O(n^2 m)
    theoretical_mn = [m * n for n in n_values]  # Theoretical O(mn)

    for n in n_values:
        results = [] # store results for specific n
        for name, algorithm in algorithms:
            result, comparison_count = measure_comparisons(algorithm, n, m, weights, distances)
            comparisons[name].append(comparison_count)
            results.append(result)
        
        # Ensure algorithms produce the same results
        assert all(r == results[0] for r in results), f"Results mismatch for n={n}"
    
    # Plotting setup
    plt.rcParams["font.family"] = "STIXGeneral" 
    plt.rcParams["legend.fontsize"] = 20        
    plt.rcParams["axes.labelsize"] = 22        
    plt.rcParams["xtick.labelsize"] = 18        
    plt.rcParams["ytick.labelsize"] = 18        

    plt.figure(figsize=(8, 6))  

    plt.plot(n_values, comparisons["Unoptimized DP"], label="Unoptimized DP", color="#333333", marker="o", markersize=6)
    plt.plot(n_values, comparisons["SMAWK with Lookup"], label="DP with SMAWK", color="#007acc", marker="s", markersize=6)
    plt.plot(n_values, theoretical_n2m, label="$\mathcal{O}(m n^2)$", color="red", linestyle="dashed")
    plt.plot(n_values, theoretical_mn, label="$\mathcal{O}(m n)$", color="green", linestyle="dashed")

    plt.xlabel("n (Number of Nodes)")
    plt.ylabel("Comparison Count")

    plt.legend(loc="upper left", fontsize=20, frameon=True)
    plt.grid(color="#808080", linestyle="--", linewidth=0.5)
    plt.tight_layout() 
    plt.savefig("experiments/results/comparison_counts.pdf", dpi=1000, bbox_inches="tight")
    plt.show()

# Run experiment
compare_algorithms()
