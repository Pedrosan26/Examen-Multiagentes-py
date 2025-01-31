import heapq
import agentpy as ap
import json

class Agente(ap.Agent):
    def setup(self):
        self.actions = {'arriba': (-1,0), 'abajo': (1, 0), 
                       'izquierda': (0, -1), 'derecha': (0, 1)}
        self.env = self.model.env
        self.path = None
        self.path_index = 0
        self.total_cost = 0
        self.simulation_data = {
            "map": {},
            "path": [],
            "metadata": {}
        }

    def get_position(self):
        return self.env.positions[self]

    def manhattan_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def get_neighbors(self, pos):
        neighbors = []
        for dx, dy in self.actions.values():
            new_pos = (pos[0] + dx, pos[1] + dy)
            if self.is_valid_move(new_pos):
                neighbors.append(new_pos)
        return neighbors

    def is_valid_move(self, pos):
        n, m = self.env.p.streets.shape
        x, y = pos
        if not (0 <= x < n and 0 <= y < m):
            return False
        if (x, y) == self.model.p.goal:
            return True
        return self.env.p.streets[x, y] > 0

    def get_movement_cost(self, pos):
        if pos == self.model.p.goal:
            return 1.0
        return float(self.env.p.streets[pos])

    def get_terrain_type(self, pos):
        if pos == self.model.p.goal:
            return 'goal'
        value = int(self.env.p.streets[pos])
        terrain_map = {
            1: 'asphalt',
            2: 'dirt',
            4: 'cracks',
            5: 'potholes',
            -1: 'wall'
        }
        return terrain_map.get(value, 'unknown')

    def initialize_simulation_data(self):
        self.simulation_data["map"] = {
            "dimensions": self.env.p.streets.shape,
            "start": self.model.p.start,
            "goal": self.model.p.goal,
            "terrain_grid": [
                [self.get_terrain_type((x, y)) 
                 for y in range(self.env.p.streets.shape[1])]
                for x in range(self.env.p.streets.shape[0])
            ]
        }
        
    def record_path_step(self, position, cost, step_type):
        self.simulation_data["path"].append({
            "step": len(self.simulation_data["path"]) + 1,
            "position": list(position),
            "terrain": self.get_terrain_type(position),
            "cost": round(cost, 2),
            "type": step_type
        })

    def find_path_to_goal(self, start, goal):
        self.initialize_simulation_data()
        
        frontier = []
        heapq.heappush(frontier, (0, start))
        came_from = {start: None}
        cost_so_far = {start: 0}

        while frontier:
            current = heapq.heappop(frontier)[1]

            if current == goal:
                break

            for next_pos in self.get_neighbors(current):
                movement_cost = self.get_movement_cost(next_pos)
                new_cost = cost_so_far[current] + movement_cost

                if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                    cost_so_far[next_pos] = new_cost
                    priority = new_cost + self.manhattan_distance(goal, next_pos)
                    heapq.heappush(frontier, (priority, next_pos))
                    came_from[next_pos] = current

        if goal not in came_from:
            return None, 0

        current = goal
        path = []
        while current is not None:
            path.append(current)
            current = came_from.get(current)
        path.reverse()

        for idx, pos in enumerate(path):
            cost = self.get_movement_cost(pos)
            step_type = 'start' if idx == 0 else 'goal' if pos == goal else 'path'
            self.record_path_step(pos, cost, step_type)

        self.total_cost = sum(self.get_movement_cost(pos) for pos in path[1:-1]) + 1.0
        self.simulation_data["metadata"] = {
            "total_cost": round(self.total_cost, 2),
            "path_length": len(path),
            "algorithm": "A*"
        }

        return path, self.total_cost

    def save_simulation_data(self):
        with open('simulation_data.json', 'w') as f:
            json.dump(self.simulation_data, f, indent=2)
        print("Datos de simulación guardados en simulation_data.json")

    def execute(self):
        if self.path is None:
            self.path, self.total_cost = self.find_path_to_goal(self.get_position(), self.model.p.goal)
            if self.path is None:
                self.model.stop()
                return None
            self.save_simulation_data()
            return self.path

        if self.path_index >= len(self.path) - 1:
            self.model.stop()
            return None

        next_pos = self.path[self.path_index + 1]
        self.path_index += 1
        self.env.move_to(self, next_pos)
        return next_pos