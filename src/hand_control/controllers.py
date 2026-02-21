from dataclasses import dataclass


@dataclass
class PIDController:
    kp: float
    ki: float
    kd: float
    dt: float
    integral_limit: float = 1.0
    output_limit: float = 2.0
    _integral: float = 0.0
    _last_error: float = 0.0

    def reset(self) -> None:
        self._integral = 0.0
        self._last_error = 0.0

    def compute(self, setpoint: float, measurement: float, velocity: float = 0.0) -> float:
        error = setpoint - measurement
        self._integral += error * self.dt
        self._integral = max(-self.integral_limit, min(self.integral_limit, self._integral))
        derivative = (error - self._last_error) / self.dt
        self._last_error = error

        output = self.kp * error + self.ki * self._integral + self.kd * derivative
        return max(-self.output_limit, min(self.output_limit, output))

