from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

from hand_control.controllers import PIDController
from hand_control.learner import LinearPolicy, TrainingSample
from hand_control.metrics import max_abs_error, rmse, settle_time
from hand_control.model import FingerPlant
from hand_control.simulator import SimulationRecord, simulate


def target_fn(t: float) -> float:
    return 0.0 if t < 0.2 else 0.8


def to_samples(records: list[SimulationRecord]) -> list[TrainingSample]:
    return [
        TrainingSample(error=r.error, velocity=r.omega, target_torque=r.torque)
        for r in records
    ]


def run_controller(name: str) -> list[SimulationRecord]:
    plant = FingerPlant(dt=0.01)
    if name == "pid":
        controller = PIDController(kp=3.8, ki=1.6, kd=0.12, dt=plant.dt)
    elif name == "linear_policy":
        teacher_plant = FingerPlant(dt=0.01)
        teacher = PIDController(kp=3.8, ki=1.6, kd=0.12, dt=teacher_plant.dt)
        teacher_records = simulate(teacher, target_fn, duration_s=4.0, plant=teacher_plant)
        policy = LinearPolicy(output_limit=2.0)
        policy.fit(to_samples(teacher_records), lr=0.003, epochs=220)
        controller = policy
    else:
        raise ValueError(f"Unknown controller {name}")
    return simulate(controller, target_fn, duration_s=4.0, plant=plant)


def save_tracking_plot(pid_records: list[SimulationRecord], learned_records: list[SimulationRecord], out_path: Path) -> None:
    t = [r.t for r in pid_records]
    target = [r.target for r in pid_records]
    pid_theta = [r.theta for r in pid_records]
    learned_theta = [r.theta for r in learned_records]

    plt.figure(figsize=(10, 5))
    plt.plot(
        t,
        target,
        "--",
        linewidth=2.2,
        color="#2f2f2f",
        label="Reference command: desired joint angle (step from 0.0 to 0.8 rad)",
    )
    plt.plot(
        t,
        pid_theta,
        linewidth=2.0,
        color="#1f77b4",
        label="PID baseline: hand-tuned feedback controller output",
    )
    plt.plot(
        t,
        learned_theta,
        linewidth=2.0,
        color="#ff7f0e",
        label="Learned policy: linear model trained to imitate PID torque",
    )
    plt.axvline(
        0.2,
        color="#7f7f7f",
        linestyle=":",
        linewidth=1.2,
        label="Command change event at t = 0.2 s",
    )
    plt.xlabel("Time [s]")
    plt.ylabel("Joint angle [rad]")
    plt.title("Finger Tracking Response")
    plt.grid(alpha=0.3)
    plt.legend(title="How to read this plot", loc="lower right", framealpha=0.95)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()


def save_metrics_plot(pid_records: list[SimulationRecord], learned_records: list[SimulationRecord], out_path: Path) -> None:
    pid_settle = settle_time(pid_records)
    learned_settle = settle_time(learned_records)
    names = ["RMSE", "Max Abs Error", "Settle Time [s]"]
    pid_values = [rmse(pid_records), max_abs_error(pid_records), pid_settle if pid_settle else 4.0]
    learned_values = [
        rmse(learned_records),
        max_abs_error(learned_records),
        learned_settle if learned_settle else 4.0,
    ]

    x = range(len(names))
    width = 0.38

    pid_color = "#1f77b4"
    learned_color = "#ff7f0e"

    plt.figure(figsize=(10, 5))
    plt.bar([i - width / 2 for i in x], pid_values, width=width, color=pid_color)
    plt.bar([i + width / 2 for i in x], learned_values, width=width, color=learned_color)
    plt.xticks(list(x), names)
    plt.ylabel("Value")
    plt.title("Controller Comparison")
    plt.grid(axis="y", alpha=0.25)
    plt.legend(
        handles=[
            Patch(facecolor=pid_color, label="PID baseline (hand-tuned gains)"),
            Patch(facecolor=learned_color, label="Learned policy (supervised imitation from PID)"),
            Line2D([], [], linestyle="none", label="Interpretation: lower is better for all bars"),
            Line2D([], [], linestyle="none", label="Settle Time is clipped to 4.0 s when not settled"),
        ],
        title="How to read this plot",
        loc="upper right",
        framealpha=0.95,
    )
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()


def main() -> None:
    out_dir = Path("assets/plots")
    out_dir.mkdir(parents=True, exist_ok=True)

    pid_records = run_controller("pid")
    learned_records = run_controller("linear_policy")

    save_tracking_plot(pid_records, learned_records, out_dir / "tracking_response.png")
    save_metrics_plot(pid_records, learned_records, out_dir / "controller_metrics.png")
    print(f"Wrote plots to: {out_dir}")


if __name__ == "__main__":
    main()
