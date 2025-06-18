# SMAWK

This repository contains an experimental implementation of the **SMAWK algorithm**, used as part of a Bachelor's thesis.

## Requirements
- Python 3.x
- matplotlib
- numpy

## How to run Experiments
To run the experiments, use the following commands:

```bash
# Run runtime analysis
python3 -m experiments.runtime_analysis

# Run access pattern analysis
python3 -m experiments.access_analysis.access_analysis

# Run comparison counts analysis
python3 -m experiments.comparison_counts.comparison_counts
```
All plots will be saved to the `experiments/results/` directory.


## Example Inputs
Each module includes example inputs that can be tested directly by running the corresponding script:

```bash
python3 -m proxy_problem.proxy_unoptimized
python3 -m proxy_problem.proxy_smawk_with_lookup
python3 -m proxy_problem.proxy_explicit_matrix
python3 -m smawk.smawk_explicit_matrix
python3 -m smawk.smawk_with_lookup
```