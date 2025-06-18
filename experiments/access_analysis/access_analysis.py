from .algorithms_modified import proxy_problem_with_access_tracking
import matplotlib.pyplot as plt
import numpy as np
import random

def generate_random_data(n):
    distances = [random.randint(1, 100) for _ in range(n)] 
    weights = [random.randint(1, 100) for _ in range(n)]
    return distances, weights

def compare_access_patterns():
    n_values = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150]  
    m = 10
    distances, weights = generate_random_data(max(n_values))

    full_sizes = [] # Theoretical full matrix size: O(mn^2) 
    unique_accesses = [] # Number of unique entries accessed across all DP matrices
    total_accesses = [] # Total number of lookup operations performed

    for n in n_values:
        d_sub = distances[:n]
        w_sub = weights[:n]

        unique_count, total_count = proxy_problem_with_access_tracking(n, m, w_sub, d_sub)
        full_count = m* (n + 2) * (n + 1)

        unique_accesses.append(unique_count)
        total_accesses.append(total_count)
        full_sizes.append(full_count)

    # Plotting setup
    plt.rcParams["font.family"] = "STIXGeneral"
    plt.rcParams["legend.fontsize"] = 20
    plt.rcParams["axes.labelsize"] = 22
    plt.rcParams["xtick.labelsize"] = 18
    plt.rcParams["ytick.labelsize"] = 18

    plt.figure(figsize=(8, 6))
    plt.plot(n_values, unique_accesses, label="Unique Accessed Entries", color="#007acc", marker="s", markersize=6)
    plt.plot(n_values, total_accesses, label="Total Lookup Operations", color="#333333", marker="o", markersize=6)
    plt.plot(n_values, full_sizes, label="Full Matrix Size", color="red", linestyle="dashed")

    plt.xlabel("n (Number of Nodes)")
    plt.ylabel("Matrix Entries")
    plt.legend(loc="upper left",fontsize = 20, frameon=True)
    plt.grid(color="#808080", linestyle="--", linewidth=0.5)
    plt.tight_layout()

    plt.savefig("experiments/results/access_analysis.pdf", dpi=1000, bbox_inches="tight")
    plt.show()

# Run experiment
compare_access_patterns()