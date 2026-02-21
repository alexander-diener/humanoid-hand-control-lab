"""Control and simulation primitives for a humanoid finger demo."""

from .controllers import PIDController
from .learner import LinearPolicy, TrainingSample
from .metrics import max_abs_error, rmse, settle_time
from .model import FingerPlant
from .simulator import SimulationRecord, simulate

__all__ = [
    "FingerPlant",
    "LinearPolicy",
    "PIDController",
    "SimulationRecord",
    "TrainingSample",
    "max_abs_error",
    "rmse",
    "settle_time",
    "simulate",
]

