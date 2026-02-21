from __future__ import annotations

import time

from hand_control.controllers import PIDController
from hand_control.model import FingerPlant
from hand_control.simulator import simulate


def target_fn(t: float) -> float:
    return 0.0 if t < 0.2 else 0.8


def main() -> None:
    episodes = 250
    duration_s = 3.0
    start = time.perf_counter()
    total_steps = 0
    for _ in range(episodes):
        plant = FingerPlant(dt=0.01)
        pid = PIDController(kp=3.8, ki=1.6, kd=0.12, dt=plant.dt)
        records = simulate(pid, target_fn, duration_s=duration_s, plant=plant)
        total_steps += len(records)
    elapsed = time.perf_counter() - start

    print(f"Episodes: {episodes}")
    print(f"Total simulation steps: {total_steps}")
    print(f"Total runtime: {elapsed:.4f}s")
    print(f"Average step runtime: {(elapsed / total_steps) * 1e6:.2f}us")


if __name__ == "__main__":
    main()
