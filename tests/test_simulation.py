from hand_control.controllers import PIDController
from hand_control.metrics import rmse
from hand_control.model import FingerPlant
from hand_control.simulator import simulate


def target_fn(t: float) -> float:
    return 0.0 if t < 0.2 else 0.8


def test_pid_tracking_converges() -> None:
    plant = FingerPlant(dt=0.01)
    pid = PIDController(kp=3.8, ki=1.6, kd=0.12, dt=plant.dt)
    records = simulate(pid, target_fn, duration_s=4.0, plant=plant)

    assert abs(records[-1].error) < 0.08
    assert rmse(records) < 0.35
