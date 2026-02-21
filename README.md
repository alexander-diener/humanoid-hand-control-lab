# Humanoid Hand Control Lab

A portfolio project tailored to a "Softwareentwickler fuer humanoide Robotik" role.

It demonstrates:
- clean control-stack architecture
- classical control (PID)
- AI-style policy learning (imitation from controller data)
- simulation, metrics, tests, and CI
- ROS2/C++ extension sketch

## Why this project fits the role

The position asks for software architecture in humanoid hand control, simulation, control methods,
and quality/performance work. This repo shows all of that in a compact form and is easy to explain live.

See detailed mapping in `docs/portfolio_mapping.md`.

## Stack

- Python 3.10+
- No heavy external runtime dependencies for core simulation
- Optional ROS2 C++ sketch in `ros2/`

## Project layout

```text
src/hand_control/
  model.py         # dynamic finger model
  controllers.py   # PID controller
  learner.py       # learned linear policy
  simulator.py     # simulation loop
  metrics.py       # RMSE, settling time, max error
scripts/
  run_demo.py      # end-to-end demo + artifact CSV
  benchmark.py     # simple runtime benchmark
tests/
  test_controllers.py
  test_simulation.py
  test_learner.py
ros2/
  finger_controller_node.cpp  # ROS2 C++ extension sketch
```

## Quickstart

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .
pip install pytest
pytest -q
python scripts/run_demo.py
python scripts/benchmark.py
```

## Typical demo output

- `artifacts/demo_results.csv` with trajectories for PID and learned policy
- terminal metrics (RMSE, max error, settling time)

## Interview narrative (3-5 minutes)

1. Explain the architecture and model assumptions (`src/hand_control/model.py`)
2. Show PID behavior and tuning (`src/hand_control/controllers.py`)
3. Show imitation-learning handoff (`src/hand_control/learner.py`)
4. Prove quality with tests and CI (`tests/`, `.github/workflows/ci.yml`)
5. Point to ROS2/C++ extension path (`ros2/finger_controller_node.cpp`)

## Publish to GitHub

```bash
git init
git add .
git commit -m "feat: add humanoid hand control portfolio project"
git branch -M main
git remote add origin https://github.com/alexander-diener/humanoid-hand-control-lab.git
git push -u origin main
```

If the target repository already exists, only run `git remote add origin` and `git push`.

