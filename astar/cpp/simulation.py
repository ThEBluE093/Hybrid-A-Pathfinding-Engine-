import matplotlib.pyplot as plt
import pandas as pd
import subprocess
import sys
from pathlib import Path
modul = Path(__file__).parent / ".."
sys.path.append(str(modul.resolve()))
from dane import COST_GRID_SIZE, CSV

RESULT = "path_output.csv"

def read_csv(file_name):
    """ Reads points from csv file and returns an array """
    df = pd.read_csv(file_name)
    points_with_cost = df[['x', 'y', 'cost']].to_numpy()
    return points_with_cost

def read_result(file_name):
    """ Reads points from csv file and returns an array """
    df = pd.read_csv(file_name)
    path = df[['x', 'y']].to_numpy()
    return path

if __name__ == "__main__":

    subprocess.run(["./astar.exe", str(CSV), str(COST_GRID_SIZE)])

    start = (0,COST_GRID_SIZE - 1)
    goal = (COST_GRID_SIZE - 1,0)
    points_with_cost = read_csv(CSV)
    path = read_result(RESULT)

    if path is not None:

        x_coords = [p[0] for p in path]
        y_coords = [p[1] for p in path]
        
        plt.figure(figsize=(10, 8))
        plt.title("CPP")

        plt.scatter(points_with_cost[:, 0], points_with_cost[:, 1], 
                    c=points_with_cost[:, 2], cmap='magma', marker='s', s=15)
        
        plt.colorbar(label='Cost')

        plt.plot(x_coords, y_coords, color='cyan', linestyle='-', linewidth=2, label='A* Path')

        plt.plot(start[0], start[1], marker='o', color='lime', markersize=10, label='Start')
        plt.plot(goal[0], goal[1], marker='o', color='red', markersize=10, label='Goal')

        plt.gca().set_aspect('equal', adjustable='box')

        plt.show()