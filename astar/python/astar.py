import heapq
import time 
import math
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

MAX_STEP_SIZE = 1.5 #Cell size (1) and diameter 1.41

def read_csv(file_name):
    """ Reads points from csv file and returns an array """
    df = pd.read_csv(file_name)
    points_with_cost = df[['x', 'y', 'cost']].to_numpy()
    return points_with_cost

def distance_between_points(point1, point2) -> float:   #point1 start (current), points2 dest (neighbor)
    """ Calculates the Euclidean distance between 2 points """
    #return np.linalg.norm(np.array(point1) - np.array(point2))
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) #math.sqrt was faster than numpy 


def pathfinding(start, goal, points_with_cost) -> tuple[tuple[float, float]]:
    """
    A* pathfinding algorithm implementation.
    last_heading: direction to which the ASV should turn at the end of the path.

    g_score : the euclidean distance (cost) from the start node to the current node + cost of the current node
    h_score : the euclidean distance (cost) from the current node to the goal node 
    f_score : g_score + h_score
    
    return : the last point reached AND the path as a list of HNEDPosition.
    """

    open_list = []          # Store points to be evaluated
    closed_list = set()     # Store points already evaluated
    came_from = {}          

    costs_dict = {tuple(point[:2]): point[2] for point in points_with_cost} #a dictionary to quickly access the cost of a point based on its coordinates

    g_score = {tuple(point[:2]): float('inf') for point in points_with_cost}
    g_score[tuple(start)] = 0

    f_score = {tuple(point[:2]): float('inf') for point in points_with_cost}
    f_score[tuple(start)] = distance_between_points(start, goal)

    heapq.heappush(open_list, (f_score[tuple(start)], tuple(start)))

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    while open_list:
        # Get the point in open list with the lowest f score
        _, current = heapq.heappop(open_list)

        if current in closed_list:
            continue

        # If the goal is reached, reconstruct the path
        if np.array_equal(current, goal):

            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)

            # Reverse the path to get the correct order from start to goal
            path = path[::-1] 
            
            return goal, path #[::2]  
        
        closed_list.add(current)

        # Check only the neighbors.   
        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)
            neighbor_tuple = tuple(neighbor)

            if neighbor_tuple not in costs_dict: 
                continue

            if neighbor_tuple in closed_list:
                continue #
    
            step_cost = distance_between_points(current, neighbor_tuple)
            if step_cost > MAX_STEP_SIZE:
                continue

            neighbor_cost = costs_dict[neighbor_tuple]
            
            tentative_g_score = g_score[tuple(current)] + neighbor_cost + step_cost
            #tentative_g_score = np.sum([g_score[tuple(current)], neighbor_cost, step_cost]) 

            # Check if there is better path to neighbor
            if tentative_g_score < g_score[neighbor_tuple]:
                came_from[neighbor_tuple] = current
                g_score[neighbor_tuple] = tentative_g_score

                #f_score[neighbor_tuple] = np.sum([g_score[neighbor_tuple], distance_between_points(neighbor, goal)])
                f_score[neighbor_tuple] = g_score[neighbor_tuple] + distance_between_points(neighbor, goal)

                if neighbor_tuple in closed_list:
                    closed_list.remove(neighbor_tuple)

                heapq.heappush(open_list, (f_score[neighbor_tuple], neighbor_tuple))
    return None, []