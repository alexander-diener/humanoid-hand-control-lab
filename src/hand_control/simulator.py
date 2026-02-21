from dataclasses import dataclass
from typing import Callable

from .model import FingerPlant


@dataclass(frozen=True)
class SimulationRecord:
    t: float
    target: float
    theta: float
    omega: float
    torque: float
    error: float


def simulate(
    controller: object,
    target_fn: Callable[[float], float],
    duration_s: float,
    plant: FingerPlant,
) -> list[SimulationRecord]:
    if duration_s <= 0:
        raise ValueError("duration_s must be > 0")

    steps = int(duration_s / plant.dt)
    if steps < 1:
        steps = 1

    records: list[SimulationRecord] = []
    for step in range(steps):
        t = step * plant.dt
        target = target_fn(t)
        torque = controller.compute(target, plant.theta, plant.omega)
        theta, omega = plant.step(torque)
        records.append(
            SimulationRecord(
                t=t,
                target=target,
                theta=theta,
                omega=omega,
                torque=torque,
                error=target - theta,
            )
        )
    return records

