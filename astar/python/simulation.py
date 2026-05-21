import matplotlib.pyplot as plt
import time
from astar import pathfinding, read_csv
import sys
from pathlib import Path
modul = Path(__file__).parent / ".."
sys.path.append(str(modul.resolve()))
from dane import COST_GRID_SIZE, CSV


if __name__ == "__main__":
    csv = CSV
    start = (0,COST_GRID_SIZE - 1)
    goal = (COST_GRID_SIZE - 1,0)
    points_with_cost = read_csv(csv)

    startTime = time.perf_counter()

    print(f"started pathfinding in Python")
    reachedGoal, path = pathfinding(start, goal, points_with_cost)

    endTime = time.perf_counter()

    if reachedGoal is not None:

        print(f"Reached goal in {endTime - startTime} seconds")

        x_coords = [p[0] for p in path]
        y_coords = [p[1] for p in path]

        plt.figure(figsize=(10, 8))
        plt.title("Python")

        plt.scatter(points_with_cost[:, 0], points_with_cost[:, 1], 
                    c=points_with_cost[:, 2], cmap='magma', marker='s', s=15)
        
        plt.colorbar(label='Cost')

        plt.plot(x_coords, y_coords, color='cyan', linestyle='-', linewidth=2, label='A* Path')

        plt.plot(start[0], start[1], marker='o', color='lime', markersize=10, label='Start')
        plt.plot(goal[0], goal[1], marker='o', color='red', markersize=10, label='Goal')

        plt.gca().set_aspect('equal', adjustable='box')

        plt.show()