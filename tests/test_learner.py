from hand_control.controllers import PIDController
from hand_control.learner import LinearPolicy, TrainingSample
from hand_control.metrics import rmse
from hand_control.model import FingerPlant
from hand_control.simulator import SimulationRecord, simulate


def target_fn(t: float) -> float:
    return 0.0 if t < 0.2 else 0.8


def to_training_data(records: list[SimulationRecord]) -> list[TrainingSample]:
    return [
        TrainingSample(error=record.error, velocity=record.omega, target_torque=record.torque)
        for record in records
    ]


def test_linear_policy_learns_from_pid_data() -> None:
    teacher_plant = FingerPlant(dt=0.01)
    teacher = PIDController(kp=3.8, ki=1.6, kd=0.12, dt=teacher_plant.dt)
    teacher_records = simulate(teacher, target_fn, duration_s=4.0, plant=teacher_plant)

    policy = LinearPolicy(output_limit=2.0)
    policy.fit(to_training_data(teacher_records), lr=0.003, epochs=220)

    student_plant = FingerPlant(dt=0.01)
    student_records = simulate(policy, target_fn, duration_s=4.0, plant=student_plant)

    assert rmse(student_records) < 0.45
