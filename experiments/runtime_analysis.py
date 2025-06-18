from proxy_problem.proxy_unoptimized import proxy_problem_unoptimized
from proxy_problem.proxy_smawk_with_lookup import proxy_problem
from proxy_problem.proxy_explicit_matrix import proxy_problem_explicit_matrix
import time
import matplotlib.pyplot as plt
import random
import numpy as np

def measure_runtime(algorithm, n, m, weights, distances):
    start_time = time.time()
    result = algorithm(n, m, weights, distances)
    end_time = time.time()
    return end_time - start_time, result

def generate_random_data(n):
    distances = [random.randint(1, 100) for _ in range(n)] 
    weights = [random.randint(1, 100) for _ in range(n)]
    return distances, weights

def compare_algorithms():
    n_values = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150])
    m = 10
    distances, weights = generate_random_data(max(n_values))

    # Define algorithms to compare
    algorithms = [
        ("Unoptimized DP", proxy_problem_unoptimized),
        ("SMAWK with Lookup", proxy_problem),
        ("Explicit-Matrix SMAWK", proxy_problem_explicit_matrix)
    ]

    times = {name: [] for name, _ in algorithms} # Dictionary to store measured runtimes per algorithm

    for n in n_values:
        results = []  # store results for specific n (for consistency check)
        for name, algorithm in algorithms:
            runtime, result = measure_runtime(algorithm, n, m, weights, distances)
            times[name].append(runtime)
            results.append(result)
        
        # Ensure algorithms produce the same results
        assert all(r == results[0] for r in results), f"Results mismatch for n={n}" 
    
    # Extract runtimes as arrays
    times_unoptimized = np.array(times["Unoptimized DP"])
    times_smawk = np.array(times["SMAWK with Lookup"])

    # Use runtime at largest tested intput as reference for scaling
    ref_index = -1 # n=150
    c1 = times_unoptimized[ref_index] / (n_values[ref_index]**2 * m)  
    c2 = times_smawk[ref_index] / (n_values[ref_index] * m) 

    # Scale theoretical curves to match with empirical curves at n=150
    theoretical_n2m = c1 * n_values**2 * m  # O(n^2 m)
    theoretical_mn = c2 * n_values * m  # O(mn)

    # Plotting setup
    plt.rcParams["font.family"] = "STIXGeneral" 
    plt.rcParams["legend.fontsize"] = 20        
    plt.rcParams["axes.labelsize"] = 22        
    plt.rcParams["xtick.labelsize"] = 18        
    plt.rcParams["ytick.labelsize"] = 18        

    plt.figure(figsize=(8, 6))  

    plt.plot(n_values, times["Unoptimized DP"], label="Unoptimized DP", color="#333333", marker="o", markersize=6)
    plt.plot(n_values, times["SMAWK with Lookup"], label="SMAWK with Lookup", color="#007acc", marker="s", markersize=6)
    plt.plot(n_values, times["Explicit-Matrix SMAWK"], label="Explicit-Matrix SMAWK", color="#1f4e79", marker="D", markersize=6)

    plt.plot(n_values, theoretical_n2m, label="$\mathcal{O}(m n^2)$", color="red", linestyle="dashed")
    plt.plot(n_values, theoretical_mn, label="$\mathcal{O}(m n)$", color="green", linestyle="dashed")

    plt.xlabel("n (Number of Nodes)")
    plt.ylabel("Runtime (Seconds)")

    plt.legend(loc="upper left", fontsize=20, frameon=True)
    plt.grid(color="#808080", linestyle="--", linewidth=0.5)
    plt.tight_layout() 
    plt.savefig("experiments/results/runtime_analysis.pdf", dpi=1000, bbox_inches="tight")

    plt.show()

# Run experiment
compare_algorithms()
