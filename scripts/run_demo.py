from __future__ import annotations

import argparse
import csv
from pathlib import Path

from hand_control.controllers import PIDController
from hand_control.learner import LinearPolicy, TrainingSample
from hand_control.metrics import max_abs_error, rmse, settle_time
from hand_control.model import FingerPlant
from hand_control.simulator import SimulationRecord, simulate


def step_target(t: float, target_value: float) -> float:
    return 0.0 if t < 0.2 else target_value


def to_samples(records: list[SimulationRecord]) -> list[TrainingSample]:
    return [
        TrainingSample(error=record.error, velocity=record.omega, target_torque=record.torque)
        for record in records
    ]


def write_csv(path: Path, controller_name: str, records: list[SimulationRecord]) -> None:
    with path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for r in records:
            writer.writerow([controller_name, r.t, r.target, r.theta, r.omega, r.torque, r.error])


def print_summary(name: str, records: list[SimulationRecord]) -> None:
    print(
        f"{name}: RMSE={rmse(records):.4f}, MaxAbsErr={max_abs_error(records):.4f}, "
        f"SettleTime={settle_time(records)}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Run finger-control demo with PID and learned policy.")
    parser.add_argument("--duration", type=float, default=4.0)
    parser.add_argument("--target", type=float, default=0.8)
    parser.add_argument("--artifacts-dir", type=Path, default=Path("artifacts"))
    args = parser.parse_args()

    args.artifacts_dir.mkdir(parents=True, exist_ok=True)
    out_csv = args.artifacts_dir / "demo_results.csv"
    out_csv.write_text("controller,t,target,theta,omega,torque,error\n", encoding="utf-8")

    base_plant = FingerPlant(dt=0.01)
    pid = PIDController(kp=3.8, ki=1.6, kd=0.12, dt=base_plant.dt)
    pid_records = simulate(
        controller=pid,
        target_fn=lambda t: step_target(t, args.target),
        duration_s=args.duration,
        plant=base_plant,
    )

    learner = LinearPolicy(output_limit=2.0)
    learner.fit(to_samples(pid_records), lr=0.003, epochs=220)

    learned_plant = FingerPlant(dt=0.01)
    learned_records = simulate(
        controller=learner,
        target_fn=lambda t: step_target(t, args.target),
        duration_s=args.duration,
        plant=learned_plant,
    )

    write_csv(out_csv, "pid", pid_records)
    write_csv(out_csv, "linear_policy", learned_records)
    print_summary("PID", pid_records)
    print_summary("LinearPolicy", learned_records)
    print(f"Wrote: {out_csv}")


if __name__ == "__main__":
    main()
