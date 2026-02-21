# Portfolio Mapping to Job Requirements

This file maps project artifacts to the job profile "Softwareentwickler fuer humanoide Robotik".

## Core mapping

- Software architecture for robot hand control:
  - `src/hand_control/model.py`
  - `src/hand_control/simulator.py`
  - `src/hand_control/controllers.py`

- Classical control algorithms:
  - `src/hand_control/controllers.py` (`PIDController`)

- AI-based algorithm:
  - `src/hand_control/learner.py` (`LinearPolicy` trained by supervised fitting)

- Simulation model and validation:
  - `src/hand_control/model.py`
  - `scripts/run_demo.py`
  - `tests/test_simulation.py`

- Test strategy and quality focus:
  - `tests/`
  - `.github/workflows/ci.yml`

- C++ / ROS2 extension path:
  - `ros2/finger_controller_node.cpp`

