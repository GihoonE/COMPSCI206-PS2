# Transparent GPU-Hour Allocation

Team A's COMPSCI/ECON 206 project compares two rules for allocating 100 shared GPU-hours among six real project teams:

1. **Random-order FCFS:** full requests are served in arrival order while capacity remains.
2. **Carbon-aware VCG priority mechanism:** teams simultaneously report a private project value; the rule selects the feasible group with the highest total reported value minus a carbon penalty. Winners pay VCG externality prices in priority credits.

## Model

For team *i*:

- GPU request \(d_i\) is observable.
- Value report \(r_i\) is private.
- Estimated emissions are \(e_i = 0.24d_i\) kg CO₂e.
- Selection score is \(r_i - 0.5e_i = r_i - 0.12d_i\).

The solver checks all \(2^6 = 64\) possible groups and selects the feasible subset with the highest total score, subject to \(\sum d_i \leq 100\). More than one team can receive its full request.

## Run

No third-party Python packages are required.

```bash
python run_simulation.py
```

This writes reproducible CSV result tables to `outputs/`. They are saved evidence for the poster and Hugging Face audit, not inputs to the model.

## Files

- `src/gpu_allocation.py` — model, exact subset solver, FCFS baseline, and VCG payments.
- `run_simulation.py` — writes the result tables.
- `notebooks/01_gpu_hour_vcg_allocation.ipynb` — Colab walkthrough.
- `outputs/` — generated allocation-audit CSV files.

## Evidence boundary

VCG is a truthful-reporting benchmark only when priority credits have a meaningful future opportunity cost. The code verifies the announced rule and its execution; it cannot verify a team's true private value.

The 0.24 kg CO₂e per GPU-hour rate and 0.5 carbon-penalty weight are current model assumptions. They need a source and sensitivity justification before the final submission.

## Attribution

Before final submission, this repository will cite Vickrey/VCG theory, the emissions source, course tools, reused code, and AI assistance.
