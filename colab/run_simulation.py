"""Run Team A's six-team FCFS-versus-VCG GPU allocation example."""

from __future__ import annotations

import csv
from pathlib import Path

from src.gpu_allocation import (
    CAPACITY_GPU_HOURS,
    default_example,
    fcfs_all_orders,
    fcfs_allocation,
    misreport_sweep,
    outcome_metrics,
    summarize_fcfs_orders,
    team_rows,
    vcg_allocation,
)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    teams, arrival_order = default_example()
    fcfs = fcfs_allocation(teams, arrival_order, CAPACITY_GPU_HOURS)
    vcg = vcg_allocation(teams, CAPACITY_GPU_HOURS)

    output_directory = Path(__file__).resolve().parent / "outputs"
    write_csv(output_directory / "fcfs_team_results.csv", team_rows(teams, fcfs))
    write_csv(output_directory / "vcg_team_results.csv", team_rows(teams, vcg))
    summary = [outcome_metrics(teams, fcfs), outcome_metrics(teams, vcg)]
    write_csv(output_directory / "summary.csv", summary)

    # Random-order FCFS over every possible arrival order (720), not just one draw.
    all_orders = fcfs_all_orders(teams, CAPACITY_GPU_HOURS)
    write_csv(output_directory / "fcfs_all_orders.csv", all_orders)

    # DSIC check: each team's utility for reports 0, 0.5, ..., 10 with rivals fixed.
    reports = [step / 2 for step in range(21)]
    sweep = [row for index in range(len(teams)) for row in misreport_sweep(teams, index, reports)]
    write_csv(output_directory / "truthfulness_check.csv", sweep)

    print("FCFS arrival order:", " -> ".join(teams[index].name for index in arrival_order))
    for result in summary:
        print("\n" + str(result["mechanism"]))
        for key, value in result.items():
            if key != "mechanism":
                print(f"  {key}: {value}")

    order_summary = summarize_fcfs_orders(teams, all_orders)
    print(f"\nRandom-order FCFS over all {order_summary['orders']} arrival orders")
    for key, value in order_summary.items():
        if key != "orders":
            print(f"  {key}: {value}")

    print("\nTruthfulness check (utility counts own carbon penalty)")
    for team in teams:
        rows = [row for row in sweep if row["team"] == team.name]
        truthful = next(row for row in rows if row["truthful"])["utility_score_units"]
        best = max(row["utility_score_units"] for row in rows)
        print(f"  {team.name}: truthful utility {truthful}, best over all reports {best}"
              f" -> {'PASS' if best <= truthful + 1e-9 else 'FAIL'}")
