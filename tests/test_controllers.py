from hand_control.controllers import PIDController


def test_pid_moves_toward_positive_setpoint() -> None:
    pid = PIDController(kp=2.0, ki=0.0, kd=0.0, dt=0.01)
    output = pid.compute(setpoint=1.0, measurement=0.0, velocity=0.0)
    assert output > 0.0


def test_pid_output_is_clamped() -> None:
    pid = PIDController(kp=100.0, ki=20.0, kd=5.0, dt=0.01, output_limit=1.5)
    output = pid.compute(setpoint=2.0, measurement=0.0, velocity=0.0)
    assert output == 1.5

