import pygame
import math
import heapq
import random
import time

pygame.font.init()

WIDTH = 600
DASHBOARD_HEIGHT = 120
WIN = pygame.display.set_mode((WIDTH, WIDTH + DASHBOARD_HEIGHT))
pygame.display.set_caption("Dynamic Pathfinding Agent")

RED = (255, 99, 71)        # Visited
GREEN = (46, 204, 113)     # Path
YELLOW = (241, 196, 15)    # Frontier
WHITE = (255, 255, 255)    # Empty
BLACK = (44, 62, 80)       # Wall
PURPLE = (155, 89, 182)    # Start
ORANGE = (230, 126, 34)    # Goal
GREY = (189, 195, 199)     # Grid lines
DARK_GREY = (52, 73, 94)   # Dashboard background

FONT = pygame.font.SysFont('Arial', 18, bold=True)

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        self.parent = None
        self.g = float('inf')
        self.h = float('inf')
        self.f = float('inf')

    def get_pos(self): return self.row, self.col
    def is_wall(self): return self.color == BLACK
    def reset(self): self.color = WHITE
    def make_start(self): self.color = PURPLE
    def make_wall(self): self.color = BLACK
    def make_goal(self): self.color = ORANGE
    def make_visited(self): self.color = RED
    def make_frontier(self): self.color = YELLOW
    def make_path(self): self.color = GREEN
    def draw(self, win): pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_wall(): # Down
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_wall(): # Up
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_wall(): # Right
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].is_wall(): # Left
            self.neighbors.append(grid[self.row][self.col - 1])

def h_manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def h_euclidean(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def reconstruct_path(current_node, draw_func):
    path = []
    while current_node.parent:
        path.append(current_node)
        current_node = current_node.parent
        if current_node.color != PURPLE:
            current_node.make_path()
        draw_func()
    return path[::-1]

def search_algorithm(draw, grid, start, goal, algo_type, heuristic_type, dynamic_mode):
    count = 0
    open_set = []
    heapq.heappush(open_set, (0, count, start))
    start.g = 0
    start.h = h_manhattan(start.get_pos(), goal.get_pos()) if heuristic_type == "MANHATTAN" else h_euclidean(start.get_pos(), goal.get_pos())
    start.f = start.h if algo_type == "GBFS" else start.g + start.h
    
    open_set_hash = {start}
    nodes_visited = 0

    while open_set:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = heapq.heappop(open_set)[2]
        open_set_hash.remove(current)

        if current == goal:
            path = reconstruct_path(goal, draw)
            return True, nodes_visited, len(path), path

        if dynamic_mode and random.random() < 0.05: 
            rand_row = random.randint(0, len(grid) - 1)
            rand_col = random.randint(0, len(grid) - 1)
            rand_node = grid[rand_row][rand_col]
            
            if rand_node.color == WHITE and rand_node != start and rand_node != goal:
                rand_node.make_wall()

        current.update_neighbors(grid)

        for neighbor in current.neighbors:
            temp_g = current.g + 1
            if temp_g < neighbor.g:
                neighbor.parent = current
                neighbor.g = temp_g
                neighbor.h = h_manhattan(neighbor.get_pos(), goal.get_pos()) if heuristic_type == "MANHATTAN" else h_euclidean(neighbor.get_pos(), goal.get_pos())
                neighbor.f = neighbor.h if algo_type == "GBFS" else neighbor.g + neighbor.h 

                if neighbor not in open_set_hash:
                    count += 1
                    heapq.heappush(open_set, (neighbor.f, count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_frontier()

        if current != start:
            current.make_visited()
            nodes_visited += 1

        draw() 
        
    return False, nodes_visited, 0, []

def make_grid(rows, width):
    gap = width // rows
    return [[Node(i, j, gap, rows) for j in range(rows)] for i in range(rows)]

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw_dashboard(win, algo, heur, mode, time_ms, nodes, cost):
    pygame.draw.rect(win, DARK_GREY, (0, WIDTH, WIDTH, DASHBOARD_HEIGHT))
    texts = [
        f"Algorithm: {algo} (Press A to toggle)",
        f"Heuristic: {heur} (Press H to toggle)",
        f"Mode: {'DYNAMIC' if mode else 'STATIC'} (Press D to toggle)",
        f"Time: {time_ms:.2f} ms | Visited: {nodes} | Cost: {cost}",
        "Controls: Left Click=Draw | Right Click=Erase | SPACE=Start | C=Clear | M=Maze",
        "Keys 1, 2, 3: Gen Map (10%, 30%, 50%)"
    ]
    
    for i, text in enumerate(texts):
        render = FONT.render(text, True, WHITE)
        win.blit(render, (10, WIDTH + 10 + (i * 18)))

def draw(win, grid, rows, width, algo, heur, mode, time_ms=0, nodes=0, cost=0):
    win.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(win)
    draw_grid(win, rows, width)
    draw_dashboard(win, algo, heur, mode, time_ms, nodes, cost)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    if x > WIDTH: return None
    return y // gap, x // gap

def generate_maze(grid, start, goal, density=0.3):
    for row in grid:
        for node in row:
            if node != start and node != goal:
                if random.random() < density:
                    node.make_wall()
                else:
                    node.reset()

def generate_random_map(grid, start, goal, density):
    for row in grid:
        for node in row:
            if node != start and node != goal:
                node.reset() 
                
                if random.random() < density:
                    node.make_wall()

def main():
    ROWS = 30 
    grid = make_grid(ROWS, WIDTH)
    start, goal = None, None
    run = True

    algo_type = "A_STAR"
    heuristic_type = "MANHATTAN"
    dynamic_mode = False
    
    metrics_time, metrics_nodes, metrics_cost = 0, 0, 0

    while run:
        draw(WIN, grid, ROWS, WIDTH, algo_type, heuristic_type, dynamic_mode, metrics_time, metrics_nodes, metrics_cost)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                coords = get_clicked_pos(pos, ROWS, WIDTH)
                if coords:
                    row, col = coords
                    node = grid[row][col]
                    if not start and node != goal:
                        start = node
                        start.make_start()
                    elif not goal and node != start:
                        goal = node
                        goal.make_goal()
                    elif node != start and node != goal:
                        node.make_wall()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                coords = get_clicked_pos(pos, ROWS, WIDTH)
                if coords:
                    row, col = coords
                    node = grid[row][col]
                    node.reset()
                    if node == start: start = None
                    if node == goal: goal = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    algo_type = "GBFS" if algo_type == "A_STAR" else "A_STAR"
                if event.key == pygame.K_h:
                    heuristic_type = "EUCLIDEAN" if heuristic_type == "MANHATTAN" else "MANHATTAN"
                if event.key == pygame.K_d:
                    dynamic_mode = not dynamic_mode
                if event.key == pygame.K_m and start and goal:
                    generate_maze(grid, start, goal)
                if event.key == pygame.K_c:
                    start, goal = None, None
                    grid = make_grid(ROWS, WIDTH)
                    metrics_time, metrics_nodes, metrics_cost = 0, 0, 0
                if event.key == pygame.K_1 and start and goal:
                    generate_random_map(grid, start, goal, 0.1)
                if event.key == pygame.K_2 and start and goal:
                    generate_random_map(grid, start, goal, 0.3)
                if event.key == pygame.K_3 and start and goal:
                    generate_random_map(grid, start, goal, 0.5)

                if event.key == pygame.K_SPACE and start and goal:
                    for row in grid:
                        for node in row:
                            if node.color in [RED, GREEN, YELLOW]: 
                                node.reset()
                            node.g, node.h, node.f = float('inf'), float('inf'), float('inf')
                            node.parent = None

                    start_time = time.time()
                    
                    success, metrics_nodes, metrics_cost, path = search_algorithm(
                        lambda: draw(WIN, grid, ROWS, WIDTH, algo_type, heuristic_type, dynamic_mode, metrics_time, metrics_nodes, metrics_cost), 
                        grid, start, goal, algo_type, heuristic_type, dynamic_mode
                    )
                    
                    metrics_time = (time.time() - start_time) * 1000
                    
                    if not success:
                        print("No path found! The target was blocked.")

    pygame.quit()

if __name__ == "__main__":
    main()
