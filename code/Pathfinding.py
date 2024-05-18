import heapq
import numpy as np

class Pathfinding:
    @staticmethod
    def a_star_search(maze, start, goal):
        def heuristic(a, b):
            return np.linalg.norm(np.array(a) - np.array(b))
        
        def get_neighbors(pos):
            neighbors = []
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for dx, dy in directions:
                x2, y2 = pos[0] + dx, pos[1] + dy
                if 0 <= x2 < maze.height and 0 <= y2 < maze.width and maze.is_valid_position(x2, y2):
                    neighbors.append((x2, y2))
            return neighbors

        open_list = []
        heapq.heappush(open_list, (0, start))
        came_from = {start: None}
        cost_so_far = {start: 0}
        
        while open_list:
            _, current = heapq.heappop(open_list)
            
            if current == goal:
                break
            
            for neighbor in get_neighbors(current):
                new_cost = cost_so_far[current] + 1
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + heuristic(goal, neighbor)
                    heapq.heappush(open_list, (priority, neighbor))
                    came_from[neighbor] = current

        path = []
        current = goal
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start)
        path.reverse()
        return path
