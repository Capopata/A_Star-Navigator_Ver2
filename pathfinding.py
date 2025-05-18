from heapq import heappush, heappop
from collections import deque

# Định nghĩa lớp Node đại diện cho một trạng thái/node trong thuật toán A*
class Node:
    def __init__(self, name, g=0, h=0, parent=None):
        if isinstance(name, list):
            name = tuple(name)
        self.name = name
        self.g = g
        self.h = h
        self.parent = parent

    def __lt__(self, other):
        return (self.g + self.h) < (other.g + other.h)

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return f"Node({self.name}, g={self.g}, h={self.h})"

class pathfinding:
    @staticmethod
    def get_path(current_node):
        path = []
        while current_node:
            path.append(current_node.name)
            current_node = current_node.parent
        return path[::-1]

    @staticmethod
    def next_node(mmap, current_node):
        neighbor_node = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        x, y = current_node.name
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(mmap) and 0 <= ny < len(mmap[0]) and mmap[nx][ny] != 1:
                neighbor_node.append((nx, ny))
        return neighbor_node

    @staticmethod
    def function_distance(x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2)

    @staticmethod
    def astar(mmap, start_node, goal_node):
        open_set = []
        closed_set = set()

        start = Node(start_node, g=0, h=pathfinding.function_distance(*start_node, *goal_node))
        heappush(open_set, start)

        while open_set:
            current_node = heappop(open_set)

            if current_node.name == goal_node:
                path = pathfinding.get_path(current_node)
                print("A* Success! Path:", ' -> '.join(map(str, path)))
                print("Cost:", current_node.g)
                return path

            closed_set.add(current_node.name)

            neighbors = pathfinding.next_node(mmap, current_node)

            for npos in neighbors:
                if npos in closed_set:
                    continue

                g_new = current_node.g + pathfinding.function_distance(*current_node.name, *npos)
                h_new = pathfinding.function_distance(*npos, *goal_node)
                neighbor = Node(npos, g=g_new, h=h_new, parent=current_node)

                skip = False
                for node in open_set:
                    if node.name == neighbor.name and (neighbor.g + neighbor.h) >= (node.g + node.h):
                        skip = True
                        break
                if skip:
                    continue

                heappush(open_set, neighbor)

        print('A* Tìm kiếm thất bại')
        return None
    @staticmethod
    def bfs(mmap, start_node, goal_node):
        open_set = deque()
        close_set = set()
        
        start = Node(start_node)
        open_set.append(start)
    
        while  open_set:
            current_node = open_set.popleft()
            
            if current_node.name == goal_node:
                path = pathfinding.get_path(current_node)
                print("BFS Success! Path:", ' -> '.join(map(str, path)))
                print("Cost:", len(path)-1)
                return path
            
            close_set.add(current_node.name)
            neighbors = pathfinding.next_node(mmap, current_node)
            
            for npos in neighbors:
                if npos in close_set:
                    continue
                if any(i.name == npos for i in open_set):
                    continue
                open_set.append(Node(npos, parent=current_node))
        print(open_set)
        print("BFS Tìm kiếm thất bại")
        return None
            