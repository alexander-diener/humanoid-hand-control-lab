from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class TrainingSample:
    error: float
    velocity: float
    target_torque: float


class LinearPolicy:
    """
    Tiny learned policy used as an "AI-based" controller example.
    torque = w0 + w1 * error + w2 * velocity
    """

    def __init__(self, output_limit: float = 2.0) -> None:
        self.w0 = 0.0
        self.w1 = 0.0
        self.w2 = 0.0
        self.output_limit = output_limit

    def reset(self) -> None:
        return None

    def compute(self, setpoint: float, measurement: float, velocity: float = 0.0) -> float:
        return self.predict(setpoint - measurement, velocity)

    def predict(self, error: float, velocity: float) -> float:
        output = self.w0 + self.w1 * error + self.w2 * velocity
        return max(-self.output_limit, min(self.output_limit, output))

    def fit(self, data: Sequence[TrainingSample], lr: float = 0.01, epochs: int = 120) -> None:
        if not data:
            raise ValueError("Training data cannot be empty.")

        for _ in range(epochs):
            for sample in data:
                pred = self.w0 + self.w1 * sample.error + self.w2 * sample.velocity
                diff = pred - sample.target_torque
                self.w0 -= 2.0 * lr * diff
                self.w1 -= 2.0 * lr * diff * sample.error
                self.w2 -= 2.0 * lr * diff * sample.velocity

