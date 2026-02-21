from dataclasses import dataclass


@dataclass
class FingerPlant:
    """
    Minimal 1-DOF finger dynamics:
        I * theta_ddot + b * theta_dot + k * theta = torque
    """

    inertia: float = 0.05
    damping: float = 0.12
    stiffness: float = 0.65
    dt: float = 0.01
    torque_limit: float = 2.0
    theta: float = 0.0
    omega: float = 0.0

    def reset(self, theta: float = 0.0, omega: float = 0.0) -> None:
        self.theta = theta
        self.omega = omega

    def step(self, torque: float) -> tuple[float, float]:
        torque = max(-self.torque_limit, min(self.torque_limit, torque))
        alpha = (torque - self.damping * self.omega - self.stiffness * self.theta) / self.inertia
        self.omega += alpha * self.dt
        self.theta += self.omega * self.dt
        return self.theta, self.omega

