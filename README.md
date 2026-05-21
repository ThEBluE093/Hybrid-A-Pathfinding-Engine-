# A* Pathfinding with Cost Grids 🗺️

High-performance implementation of the A* (A-Star) pathfinding algorithm written in C++, utilizing cost-weighted grids. The project includes a Python integration for automated execution and data visualization using Matplotlib.

## 🚀 Features
* **Core Algorithm (C++)**: Optimized A* implementation utilizing `std::priority_queue` and efficient memory handling to quickly process large grids.
* **Cost-Weighted Navigation**: Calculates optimal paths not just by distance, but by evaluating the traversal cost of each node/terrain.
* **Python Visualization**: Wraps the compiled C++ binary in a Python script, automatically reading the resulting path and generating a clear Matplotlib plot over the original grid.

## 🛠️ Tech Stack
* **C++** (Core logic, standard library, performance)
* **Python 3** (Scripting, automation)
* **Pandas & Matplotlib** (Data processing and visualization)

## 📂 Project Structure
* `/astar` - C++ and Python source code for the algorithm.
* `benchmarks` - data for algorithm testing

## ⚙️ Build & Run Instructions

**1. Compile the C++ code:**
Using `g++` (Linux/Ubuntu) or any modern C++ compiler:
```bash
cd astar/cpp
g++ -O3 simulation.py
OR
cd astar/python
python3 simulation.py
