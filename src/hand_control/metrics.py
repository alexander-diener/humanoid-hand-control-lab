from math import sqrt
from typing import Sequence

from .simulator import SimulationRecord


def rmse(records: Sequence[SimulationRecord]) -> float:
    if not records:
        raise ValueError("records cannot be empty")
    mse = sum(r.error * r.error for r in records) / len(records)
    return sqrt(mse)


def max_abs_error(records: Sequence[SimulationRecord]) -> float:
    if not records:
        raise ValueError("records cannot be empty")
    return max(abs(r.error) for r in records)


def settle_time(records: Sequence[SimulationRecord], tolerance: float = 0.03) -> float | None:
    if not records:
        return None
    window = 25
    if len(records) < window:
        return None
    for idx in range(len(records) - window):
        if all(abs(r.error) <= tolerance for r in records[idx : idx + window]):
            return records[idx].t
    return None

