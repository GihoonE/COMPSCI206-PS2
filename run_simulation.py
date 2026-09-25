"""Run Team A's six-team FCFS-versus-VCG GPU allocation example."""

from __future__ import annotations

import csv
from pathlib import Path

from src.gpu_allocation import (
    CAPACITY_GPU_HOURS,
    default_example,
    fcfs_allocation,
    outcome_metrics,
    team_rows,
    vcg_allocation,
)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    teams, arrival_order = default_example()
    fcfs = fcfs_allocation(teams, arrival_order, CAPACITY_GPU_HOURS)
    vcg = vcg_allocation(teams, CAPACITY_GPU_HOURS)

    output_directory = Path("outputs")
    write_csv(output_directory / "fcfs_team_results.csv", team_rows(teams, fcfs))
    write_csv(output_directory / "vcg_team_results.csv", team_rows(teams, vcg))
    summary = [outcome_metrics(teams, fcfs), outcome_metrics(teams, vcg)]
    write_csv(output_directory / "summary.csv", summary)

    print("FCFS arrival order:", " -> ".join(teams[index].name for index in arrival_order))
    for result in summary:
        print("\n" + str(result["mechanism"]))
        for key, value in result.items():
            if key != "mechanism":
                print(f"  {key}: {value}")
