from random import choice, sample
from pathfinding import pathfinding
from time import perf_counter

class Map:
    @staticmethod
    def map_init(node_row, node_column):
        map = []
        for row in range(node_row):
            new_row = []
            for col in range(node_column):
                if (row == 0) | (row == node_row - 1) | (col == 0) | (col == node_column - 1):
                    new_node = 1
                else:
                    new_node = 0
                new_row.append(new_node)
            map.append(new_row)
        return map

    @staticmethod
    def map_random(map):
        # Tạo map ngẫu nhiên với 0 và 1 (bỏ viền)
        for row in range(1, len(map) - 1):
            for col in range(1, len(map[0]) - 1):
                obstacle = choice((0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0))
                map[row][col] = obstacle

        # Chọn 3 vị trí ngẫu nhiên trong phần không phải viền để gán = 2
        empty = []
        for row in range(1, len(map) - 1):
            for col in range(1, len(map[0]) - 1):
                if map[row][col] != 1:
                    empty.append((row, col))
        goals = sample(empty, 3)
        for i in range(0, len(goals)):
            map[goals[i][0]][goals[i][1]] = 3
        return goals

    @staticmethod
    def print_map(map):
        for row in range(len(map)):
            for col in range(len(map[row])):
                print(f' {map[row][col]} ', end='')
                print(f'({row}, {col})', end='')
            print(f'\n')

    @staticmethod
    def turn2pixel(map, height_half, width_half, row_position, col_position):
        row_segment = len(map) - 1  # Số đoạn theo chiều dọc
        col_segment = len(map[0]) - 1  # Số đoạn theo chiều ngang
        row_distance = 2 * height_half / row_segment  # Chiều cao mỗi ô
        col_distance = 2 * width_half / col_segment  # Chiều rộng mỗi ô
        
        x_pixel = -width_half + col_position * col_distance
        y_pixel = height_half - row_position * row_distance
        return [x_pixel, y_pixel]

    @staticmethod
    def turn2node(map, width_half, height_half, x_pixel, y_pixel):
        row_segment = len(map) - 1
        col_segment = len(map[0]) - 1
        row_distance = 2 * height_half / row_segment
        col_distance = 2 * width_half / col_segment
        
        row_pos = round((height_half - y_pixel) / row_distance)
        col_pos = round((x_pixel + width_half) / col_distance)
        return [row_pos, col_pos]

    @staticmethod
    def random_curpos(map):
        position = []
        for row in range(len(map)):
            for col in range(len(map[0])):
                if map[row][col] == 0:
                    position.append([row, col])
        return choice(position)

    @staticmethod
    def draw_map(map, color, pen, width_half, height_half, start):
        pen.speed(0)
        for row in range(len(map)):
            if row == 0 or row == len(map) - 1:
                pen.color('black')
            else:
                pen.color(color)
            pen.seth(0)
            pen.up()
            pen.goto(Map.turn2pixel(map, height_half, width_half, row, 0))
            pen.down()
            pen.goto(Map.turn2pixel(map, height_half, width_half, row, len(map[row]) - 1))

        for col in range(len(map[0])):
            if col == 0 or col == len(map[0]) - 1:
                pen.color('black')
            else:
                pen.color(color)
            pen.seth(-90)
            pen.up()
            pen.goto(Map.turn2pixel(map, height_half, width_half, 0, col))
            pen.down()
            pen.goto(Map.turn2pixel(map, height_half, width_half, len(map) - 1, col))

        for row in range(len(map)):
            for col in range(len(map[row])):
                pen.color(color)
                if map[row][col] == 1:
                    pen.up()
                    pen.goto(Map.turn2pixel(map, height_half, width_half, row, col))
                    pen.down()
                    pen.dot(5, 'black')
                elif map[row][col] == 3:
                    pen.goto(Map.turn2pixel(map, height_half, width_half, row, col))
                    pen.down()
                    pen.dot(10, 'orange')
                elif [row, col] == start:
                    pen.goto(Map.turn2pixel(map, height_half, width_half, row, col))
                    pen.down()
                    pen.dot(10, 'green')
                    
    """
    @staticmethod
    def draw_amr(map, amr, width_half, height_half, current_ppos):
        amr.up()
        amr.goto(current_ppos)
        current_mpos = Map.turn2node(map, width_half=width_half, height_half=height_half, x_pixel=current_ppos[0], y_pixel=current_ppos[1])
        return current_mpos
    """
    @staticmethod
    def nextorient_set(map, current_node):
        set_result = []
        directions = {
            (1, 0): 270,    # xuống
            (-1, 0): 90,    # lên
            (0, 1): 0,      # phải
            (0, -1): 180    # trái
        }
        x, y = current_node.name
        for (dx, dy), angle in directions.items():
            nx, ny = x + dx, y + dy
            if 0 < nx < len(map) and 0 < ny < len(map[0]):
                if map[nx][ny] != 1:  # đường đi hoặc goal
                    set_result.append(angle)
        return set_result

    @staticmethod
    def run_rule(amr1, amr2, path_a_star, path_bfs, mmap, width_half, height_half):
        global current_mpos_a_star, current_mpos_bfs
        
        amr1.speed(5)
        amr2.speed(5)
        row_segment = len(mmap) - 1
        col_segment = len(mmap[0]) - 1
        row_distance = 2 * height_half / row_segment
        col_distance = 2 * width_half / col_segment
        if not path_a_star or not path_bfs:
            print("Không tìm được đường")
            return False
        if len(path_a_star) >= len(path_bfs):
            max_path = path_a_star
            min_path = path_bfs
            robot1 = amr1
            robot2 = amr2
        else:
            max_path = path_bfs
            min_path = path_a_star
            robot1 = amr2
            robot2 = amr1
            
        for i in range(1, len(max_path)):
            prevmax = max_path[i - 1]
            currmax = max_path[i]
            dxmax, dymax = currmax[0] - prevmax[0], currmax[1] - prevmax[1]
            
            # Robot 1 (đường dài)
            if dxmax == -1: heading = 90
            elif dxmax == 1: heading = 270
            elif dymax == -1: heading = 180
            elif dymax == 1: heading = 0
            
            robot1.setheading(heading)
            robot1.down()
            if heading in [90, 270]:
                robot1.forward(row_distance)
            else:
                robot1.forward(col_distance)

            # Robot 2 (đường ngắn)
            if i < len(min_path):
                premin = min_path[i - 1]
                currmin = min_path[i]
                dxmin, dymin = currmin[0] - premin[0], currmin[1] - premin[1]
                
                if dxmin == -1: heading1 = 90
                elif dxmin == 1: heading1 = 270
                elif dymin == -1: heading1 = 180
                elif dymin == 1: heading1 = 0
                
                robot2.setheading(heading1)
                robot2.down()
                if heading1 in [90, 270]:
                    robot2.forward(row_distance)
                else:
                    robot2.forward(col_distance)
                # Kiểm tra chồng điểm: nếu cùng tọa độ -> đổi màu
                if i < len(min_path) and currmax == currmin:
                    robot1.color('purple')
                    robot2.color('purple')
                else:
                    robot1.color('blue')
                    robot2.color('red')

    @staticmethod
    def run(amr1, amr2, mmap, width_half, height_half, start_node, goal_node):
        global current_mpos_a_star, current_mpos_bfs
        
        amr1.color('blue')
        amr2.color('red')
        current_mpos_a_star = list(start_node)  # Gán vị trí robot hiện tại
        current_mpos_bfs = list(start_node)
        start_pixel = Map.turn2pixel(mmap, height_half, width_half, *start_node)
        amr1.up()
        amr2.up()
        amr1.goto(start_pixel[0], start_pixel[1])
        amr2.goto(start_pixel[0], start_pixel[1])
        amr1.down()
        amr2.down()
        
        goal_distance = []
        list_t_a_star = []
        list_t_bfs = []
        t_a_star = 0
        t_bfs = 0
        
        while goal_node:
            goal_distance = [(g, pathfinding.function_distance(*start_node, *g)) for g in goal_node]
            nearest_goal = min(goal_distance, key=lambda x: x[1])[0]
            
            print("Start:", start_node)
            print("Goal:", nearest_goal)
            
            t0 = perf_counter()
            path_a_star = pathfinding.astar(mmap, start_node, nearest_goal)
            t0 = perf_counter()-t0
            list_t_a_star.append(t0)
            t_a_star +=t0
            
            t1 = perf_counter()
            path_bfs = pathfinding.bfs(mmap, start_node, nearest_goal)
            t1 = perf_counter() - t1
            list_t_bfs.append(t1)
            t_bfs +=t1
            if not path_a_star and not path_bfs:
                print("Không tìm được đường")
                return False 
            else:
                Map.run_rule(amr1, amr2, path_a_star, path_bfs, mmap, width_half, height_half)
            
            mmap[nearest_goal[0]][nearest_goal[1]] = 0
            start_node = nearest_goal
            goal_node.remove(nearest_goal)
        print("Thời gian giải a*: ", list_t_a_star)
        print("Thời gian giải BFS: ", list_t_bfs)
        return t_a_star, t_bfs
