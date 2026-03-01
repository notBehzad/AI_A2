# Dynamic Pathfinding Agent

This project is a grid-based visualizer for Informed Search Algorithms, specifically **A* Search** and **Greedy Best-First Search (GBFS)**. It features an interactive map editor, random maze generation, real-time metrics, and a "Dynamic Mode" where obstacles spawn randomly while the algorithm calculates the path, forcing it to adapt and re-plan.

## Features
* **Algorithms:** A* Search and Greedy Best-First Search (GBFS).
* **Heuristics:** Manhattan Distance and Euclidean Distance.
* **Dynamic Environment:** Option to enable random obstacle spawning during the search phase to test real-time re-planning.
* **Interactive GUI:** Draw custom mazes, place start/goal nodes, and visualize the algorithms exploring the grid.
* **Real-Time Metrics:** Tracks Execution Time (ms), Nodes Visited, and Final Path Cost.

## Prerequisites

To run this project, you will need **Python 3.x** installed on your computer, along with the `pygame` library which handles the graphical user interface.

## Installation

1. Open your terminal or command prompt.
2. Install the required dependency by running the following command:
   ```bash
   pip install pygame
