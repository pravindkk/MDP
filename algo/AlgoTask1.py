import heapq
import json
import time


class Object3x3:
    def __init__(self, center_x, center_y):
        self.center_x = center_x
        self.center_y = center_y

    def get_positions(self):
        return [(self.center_x - 1, self.center_y - 1),
                (self.center_x - 1, self.center_y),
                (self.center_x - 1, self.center_y + 1),
                (self.center_x, self.center_y - 1),
                (self.center_x, self.center_y),
                (self.center_x, self.center_y + 1),
                (self.center_x + 1, self.center_y - 1),
                (self.center_x + 1, self.center_y),
                (self.center_x + 1, self.center_y + 1)]


class AlgoFunctions():
    @staticmethod
    def calculateDistancebtwnCoordinates(x1, y1, x2, y2):
        x_dist = x2 - x1
        y_dist = y2 - y1
        return abs(x_dist) + abs(y_dist)

    @staticmethod
    def print_grid(path, reference_obstacles):
        # Mark the path on the grid
        for movement in path:
            for position in movement:

                # Initialize a 20x20 grid with all zeros
                grid = [[' '] * 20 for _ in range(20)]

                # Mark obstacles on the grid
                for obstacle in reference_obstacles:
                    x, y, direction = obstacle
                    # Marking obstacle at the specified position
                    grid[x][y] = obstacle[2].upper()

                print("Position", position)

                if (position[2] == 'N'):
                    position_center_x = position[0]+1
                    position_center_y = position[1]
                elif (position[2] == 'S'):
                    position_center_x = position[0]-1
                    position_center_y = position[1]
                elif (position[2] == 'E'):
                    position_center_x = position[0]
                    position_center_y = position[1]-1
                elif (position[2] == 'W'):
                    position_center_x = position[0]
                    position_center_y = position[1]+1
                else:
                    position_center_x = position[0]
                    position_center_y = position[1]

                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        grid[position_center_x + dx][position_center_y + dy] = 'C'

                grid[position[0]][position[1]] = 'X'

                # Display the grid (optional, for visualization purposes)
                for row in grid:
                    print(row)
        return None

    @staticmethod
    def count_repeated_commands(action): 
        # Initialize an empty list to store the modified action      
        modified_action = [] 
        # Initialize the previous command and its count 
        prev_command = None 
        count = 0 
 
        # Iterate over the action list 
        for command in action:    
            # If the current command is the same as the previous one, increment the count 
            if command in ['FW', 'BW'] and command == prev_command: 
                count += 1 
            else: 
                # If the previous command is not None and not 'SNAP' or 'STOP', append it with its count to the modified action 
                if prev_command is not None and prev_command != 'STOP' and not prev_command.startswith('SNAP'): 
                    # Append the count to the command and pad with a zero at the end if it's a single digit 
                    # For 'FR', 'FL', 'BL', and 'BR', the count is always '00' 
                    if prev_command in ['FR', 'FL', 'BL', 'BR']: 
                        modified_action.append(f"{prev_command}00") 
                    else: 
                        if (count >= 10): 
                            # Append the first part of the count with  10 to the command 
                            modified_action.append(f"{prev_command}90") 
                            # Append the second part of the count with the remainder to the command 
                            modified_action.append( 
                                f"{prev_command}{count -  9}0") 
                        else: 
                            modified_action.append( 
                                f"{prev_command}{count}{'0' if count < 10 else ''}") 
                # If the previous command is 'SNAP' or 'STOP', append it without a count 
                elif prev_command is not None and (prev_command == 'STOP' or prev_command.startswith('SNAP')): 
                    modified_action.append(prev_command) 
                # Reset the count and set the current command as the previous command 
                count = 1 
                prev_command = command 
 
        # Append the last command with its count to the modified action 
        if prev_command is not None and prev_command != 'STOP' and not prev_command.startswith('SNAP'): 
            # Append the count to the command and pad with a zero at the end if it's a single digit 
            # For 'FR', 'FL', 'BL', and 'BR', the count is always '00' 
            if prev_command in ['FR', 'FL', 'BL', 'BR']: 
                modified_action.append(f"{prev_command}00") 
            else: 
                if (count >= 10): 
                    # Append the first part of the count with  10 to the command 
                    modified_action.append(f"{prev_command}90") 
                    # Append the second part of the count with the remainder to the command 
                    modified_action.append(f"{prev_command}{count -  9}0") 
                else: 
                    modified_action.append( 
                        f"{prev_command}{count}{'0' if count < 10 else ''}") 
        elif prev_command is not None and (prev_command == 'STOP' or prev_command.startswith('SNAP')): 
            modified_action.append(prev_command) 
 
        return modified_action

    @staticmethod
    def NearestNeighbourSearch(data):

        # print("Checking Output Data:", data)

        obstacles = [(obstacle['x'], obstacle['y'], obstacle['d'],
                      obstacle['id']) for obstacle in data]

        print("Checking Output Obstacles:", obstacles)

        if not obstacles:
            print("No obstacles found.")
            return []
        dist = 999
        starting_coordinates = (17, 1, 'N')
        reference_obstacles = obstacles.copy()
        path = []
        action = []
        fail = None

        # Initialize a 20x20 grid with all zeros
        grid = [[' '] * 20 for _ in range(20)]

        temp = []

        # Mark obstacles on the grid
        for obstacle in obstacles:

            obstacle = list(obstacle)
            obstacle[1] = 19 - obstacle[1]
            x, y, direction, id = obstacle

            if (obstacle[2] == 0):
                # grid[x][y] = obstacle[2].upper()  # Marking obstacle at the specified position
                obstacle[2] = 'N'
            elif (obstacle[2] == 2):
                obstacle[2] = 'E'
            elif (obstacle[2] == 4):
                obstacle[2] = 'S'
            else:
                obstacle[2] = 'W'
            

            grid[y][x] = obstacle[2]

            obstacle = tuple(obstacle)

            temp.append((y, x, obstacle[2], id))

        obstacles = temp

        print("Fucking chibai kia ", obstacles)

        # Create an Object3x3 instance from within the function
        object_instance = Object3x3(center_x=18, center_y=1)

        # Use the Object3x3 instance to mark the object on the grid
        for x, y in object_instance.get_positions():
            if (x, y) == (object_instance.center_x-1, object_instance.center_y):  # Top middle position
                grid[x][y] = 'C'
            else:
                grid[x][y] = 'X'

        # Display the grid (optional, for visualization purposes)
        for row in grid:
            print(row)

        # find nearest neighbours
        while (len(obstacles) == 1 and fail is None) or len(obstacles) > 1:
            for i in range(len(obstacles)):
                if fail is None:
                    if (AlgoFunctions.calculateDistancebtwnCoordinates(starting_coordinates[0], starting_coordinates[1], obstacles[i][0], obstacles[i][1]) < dist):
                        dist = AlgoFunctions.calculateDistancebtwnCoordinates(
                            starting_coordinates[0], starting_coordinates[1], obstacles[i][0], obstacles[i][1])
                        shortestNode = obstacles[i]
                elif fail != obstacles[i]:
                    if (AlgoFunctions.calculateDistancebtwnCoordinates(starting_coordinates[0], starting_coordinates[1], obstacles[i][0], obstacles[i][1]) < dist):
                        dist = AlgoFunctions.calculateDistancebtwnCoordinates(
                            starting_coordinates[0], starting_coordinates[1], obstacles[i][0], obstacles[i][1])
                        shortestNode = obstacles[i]
            # print("startingNode", starting_coordinates)
            print("ShortestNode", shortestNode)
            start = starting_coordinates
            if shortestNode[2].upper() == 'N':
                starting_coordinates = (
                    shortestNode[0] - 3, shortestNode[1], 'S')
                target = (shortestNode[0] - 3, shortestNode[1], 'S')
            elif shortestNode[2].upper() == 'S':
                starting_coordinates = (
                    shortestNode[0] + 3, shortestNode[1], 'N')
                target = (shortestNode[0] + 3, shortestNode[1], 'N')
            elif shortestNode[2].upper() == 'E':
                starting_coordinates = (
                    shortestNode[0], shortestNode[1] + 3, 'W')
                target = (shortestNode[0], shortestNode[1] + 3, 'W')
            elif shortestNode[2].upper() == 'W':
                starting_coordinates = (
                    shortestNode[0], shortestNode[1] - 3, 'E')
                target = (shortestNode[0], shortestNode[1] - 3, 'E')
            # print("targetNode", target)
            path_result, action_result = AlgoFunctions.AStarSearch(
                grid, start, target, object_instance.get_positions(), shortestNode[3])
            if path_result:
                path.append((path_result, shortestNode[3]))  # ?
                # print("Output Path:", path)
                obstacles.remove(shortestNode)
                fail = None
            else:
                starting_coordinates = start
                fail = shortestNode
            # for row in grid:
            #     print(row)
            if action_result:
                # print('What is action_result: ', action_result)
                action.append(action_result)
                # print("Action: ", action)

            dist = 999
            shortestNode = []

            new_action = [j for sub in action for j in sub]

        new_action.append('STOP')

        modified_action = AlgoFunctions.count_repeated_commands(new_action)

        json_action = {"data": {'path': path, 'distance': 0,
                                'commands': modified_action}}

        print("Checking Json:", json_action)

        # AlgoFunctions.print_grid(path, reference_obstacles)

        ########################################################################
        ########################################################################
        ########################################################################
        ########################################################################
        ########################################################################

        # Run this return to return json of commands instead of path & grid

        return json_action

        # Make sure to command out the below return path, even though redundant

        ########################################################################
        ########################################################################
        ########################################################################
        ########################################################################
        ########################################################################

        return path, grid

    @staticmethod
    def AStarSearch(grid, start, target, object_positions, obs_id, timeout=60):
        
        def move_front(new_x, new_y, orientation):
            if orientation == 'N':
                new_x -= 1
            elif orientation == 'S':
                new_x += 1
            elif orientation == 'E':
                new_y += 1
            elif orientation == 'W':
                new_y -= 1
            return new_x, new_y, orientation
        
        def move_back(new_x, new_y, orientation):
            if orientation == 'N':
                new_x += 1
            elif orientation == 'S':
                new_x -= 1
            elif orientation == 'E':
                new_y -= 1
            elif orientation == 'W':
                new_y += 1
            return new_x, new_y, orientation

        def rotate_ccw(new_x, new_y, orientation):
            # Rotate counterclockwise
            if orientation == 'N':
                new_x, new_y = new_x + 1, new_y - 1
                orientation = 'W'
            elif orientation == 'S':
                new_x, new_y = new_x - 1, new_y + 1
                orientation = 'E'
            elif orientation == 'E':
                new_x, new_y = new_x - 1, new_y - 1
                orientation = 'N'
            elif orientation == 'W':
                new_x, new_y = new_x + 1, new_y + 1
                orientation = 'S'            
            return new_x, new_y, orientation
        
        def rotate_cw(new_x, new_y, orientation):
            if orientation == 'N':
                new_x, new_y = new_x + 1, new_y + 1
                orientation = 'E'
            elif orientation == 'S':
                new_x, new_y = new_x - 1, new_y - 1
                orientation = 'W'
            elif orientation == 'E':
                new_x, new_y = new_x + 1, new_y - 1
                orientation = 'S'
            elif orientation == 'W':
                new_x, new_y = new_x - 1, new_y + 1
                orientation = 'N'
            return new_x, new_y, orientation        

        def is_valid_move(x, y, direction, orientation, grid):
            # Forward movement
            if direction == 'FW':
                if orientation == 'N' and (x-1 >= 0) and (0 < y <= 18) and all(grid[x-1][i] in (' ', 'C') for i in range(y - 1, y + 2)):
                    return True
                elif orientation == 'S' and (x+1 < 20) and (0 < y <= 18) and all(grid[x+1][i] in (' ', 'C') for i in range(y - 1, y + 2)):
                    return True
                elif orientation == 'E' and (y+1 < 20) and (0 < x <= 18) and all(grid[j][y+1] in (' ', 'C') for j in range(x - 1, x + 2)):
                    return True
                elif orientation == 'W' and (y-1 >= 0) and (0 < x <= 18) and all(grid[j][y-1] in (' ', 'C') for j in range(x - 1, x + 2)):
                    return True
            # Backward movement
            elif direction == 'BW':
                if orientation == 'N' and (x+3 < 20) and (0 < y <= 18) and all(grid[x+3][i] in (' ', 'C') for i in range(y - 1, y + 2)):
                    return True
                elif orientation == 'S' and (x-3 >= 0) and (0 < y <= 18) and all(grid[x-3][i] in (' ', 'C') for i in range(y - 1, y + 2)):
                    return True
                elif orientation == 'E' and (y-3 >= 0) and (0 < x <= 18) and all(grid[j][y-3] in (' ', 'C') for j in range(x - 1, x + 2)):
                    return True
                elif orientation == 'W' and (y+3 < 20) and (0 < x <= 18) and all(grid[j][y+3] in (' ', 'C') for j in range(x - 1, x + 2)):
                    return True
            return False

        def is_valid_front_turn(x, y, direction, orientation):
            new_x = x
            new_y = y
            # Check if the turn is valid
            if direction == 'L':
                # Move up by 1
                if not is_valid_move(new_x, new_y, 'FW', orientation, grid):
                    return False
                new_x, new_y, orientation = move_front(new_x, new_y, orientation)

                # Rotate counterclockwise
                new_x, new_y, orientation = rotate_ccw(new_x, new_y, orientation)

                # Move up by 1
                if not is_valid_move(new_x, new_y, 'FW', orientation, grid):
                    return False
                new_x, new_y, orientation = move_front(new_x, new_y, orientation)
                    
                # Rotate clockwise
                new_x, new_y, orientation = rotate_cw(new_x, new_y, orientation)
                
                # Move up by 1
                if not is_valid_move(new_x, new_y, 'FW', orientation, grid):
                    return False
                new_x, new_y, orientation = move_front(new_x, new_y, orientation)

                # Rotate counterclockwise
                new_x, new_y, orientation = rotate_ccw(new_x, new_y, orientation)

                # Move forward by 3 cells
                for i in range(3):
                    if not is_valid_move(new_x, new_y, 'FW', orientation, grid):
                        return False
                    new_x, new_y, orientation = move_front(new_x, new_y, orientation)

                return True

            elif direction == 'R':
                # Move up by 1  
                if not is_valid_move(new_x, new_y, 'FW', orientation, grid):
                    return False
                new_x, new_y, orientation = move_front(new_x, new_y, orientation)
                
                # Rotate clockwise
                new_x, new_y, orientation = rotate_cw(new_x, new_y, orientation)
                
                if not is_valid_move(new_x, new_y, 'FW', orientation, grid):
                    return False
                new_x, new_y, orientation = move_front(new_x, new_y, orientation)  
                
                # Rotate counterclockwise
                new_x, new_y, orientation = rotate_ccw(new_x, new_y, orientation)     
                
                if not is_valid_move(new_x, new_y, 'FW', orientation, grid):
                    return False
                new_x, new_y, orientation = move_front(new_x, new_y, orientation)
                
                # Rotate clockwise
                new_x, new_y, orientation = rotate_cw(new_x, new_y, orientation)            
                
                # Move forward by 3 cells
                for i in range(3):
                    if not is_valid_move(new_x, new_y, 'FW', orientation, grid):
                        return False
                    new_x, new_y, orientation = move_front(new_x, new_y, orientation)
                return True
            return False
        
        def is_valid_back_turn(x, y, direction, orientation):
            new_x = x
            new_y = y
            # Check if the turn is valid
            if direction == 'R':
                # Move backward by 3 cells
                if not is_valid_move(new_x, new_y, 'FW', orientation, grid):
                    return False
                for i in range(2):
                    if not is_valid_move(new_x, new_y, 'BW', orientation, grid):
                        return False
                    new_x, new_y, orientation = move_back(new_x, new_y, orientation)
                    
                # Rotate counterclockwise
                new_x, new_y, orientation = rotate_ccw(new_x, new_y, orientation)

                if not is_valid_move(new_x, new_y, 'BW', orientation, grid):
                    return False
                new_x, new_y, orientation = move_back(new_x, new_y, orientation)

                # Rotate clockwise
                new_x, new_y, orientation = rotate_cw(new_x, new_y, orientation)

                # Move back by 1
                if not is_valid_move(new_x, new_y, 'BW', orientation, grid):
                    return False
                new_x, new_y, orientation = move_back(new_x, new_y, orientation)

                # Rotate counterclockwise
                new_x, new_y, orientation = rotate_ccw(new_x, new_y, orientation)

                if not is_valid_move(new_x, new_y, 'BW', orientation, grid):
                    return False
                new_x, new_y, orientation = move_back(new_x, new_y, orientation)
                
                return True

            elif direction == 'L':
                if not is_valid_move(new_x, new_y, 'FW', orientation, grid):
                    return False
                # Move backwards by 2 cells
                for i in range(2):
                    if not is_valid_move(new_x, new_y, 'BW', orientation, grid):
                        return False
                    new_x, new_y, orientation = move_back(new_x, new_y, orientation)

                # Rotate clockwise
                if orientation == 'N':
                    new_x, new_y = new_x + 1, new_y + 1
                    orientation = 'E'
                elif orientation == 'S':
                    new_x, new_y = new_x - 1, new_y - 1
                    orientation = 'W'
                elif orientation == 'E':
                    new_x, new_y = new_x + 1, new_y - 1
                    orientation = 'S'
                elif orientation == 'W':
                    new_x, new_y = new_x - 1, new_y + 1
                    orientation = 'N'
                
                if not is_valid_move(new_x, new_y, 'BW', orientation, grid):
                    return False
                new_x, new_y, orientation = move_back(new_x, new_y, orientation)

                # Rotate counterclockwise
                new_x, new_y, orientation = rotate_ccw(new_x, new_y, orientation)
                
                # Move back by 1
                if not is_valid_move(new_x, new_y, 'BW', orientation, grid):
                    return False
                new_x, new_y, orientation = move_back(new_x, new_y, orientation)
                
                # Rotate clockwise
                new_x, new_y, orientation = rotate_cw(new_x, new_y, orientation)
                
                if not is_valid_move(new_x, new_y, 'BW', orientation, grid):
                    return False
                new_x, new_y, orientation = move_back(new_x, new_y, orientation)
                
                return True
            return False
        
        class State:
            def __init__(self, x, y, direction, action=None, parent=None):
                self.x = x
                self.y = y
                self.direction = direction
                self.coordinate = (x, y, direction)
                self.action = action
                self.parent = parent

            def __eq__(self, other):
                return self.x == other.x and self.y == other.y and self.direction == other.direction

            def __hash__(self):
                return hash((self.x, self.y, self.direction))

        class Node:
            def __init__(self, state, parent=None, action=None, cost=0, heuristic=0):
                self.state = state
                self.parent = parent
                self.coordinate = state.coordinate
                self.action = action
                self.cost = cost
                self.heuristic = heuristic
                self.repeated_move = False  # Flag to indicate repeated moves

            def total_cost(self):
                return self.cost + self.heuristic

            def __lt__(self, other):
                return self.total_cost() < other.total_cost()

        def get_successors(state, object_positions):
            successors = []

            # Check for valid forward moves
            if state.direction == 'N':
                if is_valid_move(state.x, state.y, 'FW', state.direction, grid):
                    successors.append(
                        State(state.x - 1, state.y, state.direction, 'FW', state))
            elif state.direction == 'S':
                if is_valid_move(state.x, state.y, 'FW', state.direction, grid):
                    successors.append(
                        State(state.x + 1, state.y, state.direction, 'FW', state))
            elif state.direction == 'E':
                if is_valid_move(state.x, state.y, 'FW', state.direction, grid):
                    successors.append(
                        State(state.x, state.y + 1, state.direction, 'FW', state))
            elif state.direction == 'W':
                if is_valid_move(state.x, state.y, 'FW', state.direction, grid):
                    successors.append(
                        State(state.x, state.y - 1, state.direction, 'FW', state))

            # Check for valid backward moves
            if state.direction == 'N':
                if is_valid_move(state.x, state.y, 'BW', state.direction, grid):
                    successors.append(
                        State(state.x + 1, state.y, state.direction, 'BW', state))
            elif state.direction == 'S':
                if is_valid_move(state.x, state.y, 'BW', state.direction, grid):
                    successors.append(
                        State(state.x - 1, state.y, state.direction, 'BW', state))
            elif state.direction == 'E':
                if is_valid_move(state.x, state.y, 'BW', state.direction, grid):
                    successors.append(
                        State(state.x, state.y - 1, state.direction, 'BW', state))
            elif state.direction == 'W':
                if is_valid_move(state.x, state.y, 'BW', state.direction, grid):
                    successors.append(
                        State(state.x, state.y + 1, state.direction, 'BW', state))
            # Check for valid left turns
            if is_valid_front_turn(state.x, state.y, 'L', state.direction):
                if state.direction == 'N':
                    successors.append(State(state.x-1, state.y-4, get_new_direction(state.direction, 'L', 'FW'), 'FL', state))
                elif state.direction == 'S':
                    successors.append(State(state.x+1, state.y+4, get_new_direction(state.direction, 'L', 'FW'), 'FL', state))
                elif state.direction == 'E':
                    successors.append(State(state.x-4, state.y+1, get_new_direction(state.direction, 'L', 'FW'), 'FL', state))
                elif state.direction == 'W':
                    successors.append(State(state.x+4, state.y-1, get_new_direction(state.direction, 'L', 'FW'), 'FL', state))

            # Check for valid right turns
            if is_valid_front_turn(state.x, state.y, 'R', state.direction):
                if state.direction == 'N':
                    successors.append(State(state.x-1, state.y+4, get_new_direction(state.direction, 'R', 'FW'), 'FR', state))
                elif state.direction == 'S':
                    successors.append(State(state.x+1, state.y-4, get_new_direction(state.direction, 'R', 'FW'), 'FR', state))
                elif state.direction == 'E':
                    successors.append(State(state.x+4, state.y+1, get_new_direction(state.direction, 'R', 'FW'), 'FR', state))
                elif state.direction == 'W':
                    successors.append(State(state.x-4, state.y-1, get_new_direction(state.direction, 'R', 'FW'), 'FR', state))
            
            # Check for valid left turns
            if is_valid_back_turn(state.x, state.y, 'L', state.direction):
                if state.direction == 'N':
                    successors.append(State(state.x+4, state.y-1, get_new_direction(state.direction, 'L', 'BW'), 'BL', state))
                elif state.direction == 'S':
                    successors.append(State(state.x-4, state.y+1, get_new_direction(state.direction, 'L', 'BW'), 'BL', state))
                elif state.direction == 'E':
                    successors.append(State(state.x-1, state.y-4, get_new_direction(state.direction, 'L', 'BW'), 'BL', state))
                elif state.direction == 'W':
                    successors.append(State(state.x+1, state.y+4, get_new_direction(state.direction, 'L', 'BW'), 'BL', state))

            # Check for valid right turns
            if is_valid_back_turn(state.x, state.y, 'R', state.direction):
                if state.direction == 'N':
                    successors.append(State(state.x+4, state.y+1, get_new_direction(state.direction, 'R', 'BW'), 'BR', state))
                elif state.direction == 'S':
                    successors.append(State(state.x-4, state.y-1, get_new_direction(state.direction, 'R', 'BW'), 'BR', state))
                elif state.direction == 'E':
                    successors.append(State(state.x+1, state.y-4, get_new_direction(state.direction, 'R', 'BW'), 'BR', state))
                elif state.direction == 'W':
                    successors.append(State(state.x-1, state.y+4, get_new_direction(state.direction, 'R', 'BW'), 'BR', state))
            return successors
        
        def get_new_direction(current_direction, turn_direction, move_direction):
            # Function to calculate the new direction after a turn
            directions = ['N', 'E', 'S', 'W']
            current_index = directions.index(current_direction)

            if move_direction == 'FW':
                if turn_direction == 'L':
                    new_index = (current_index - 1) % 4
                elif turn_direction == 'R':
                    new_index = (current_index + 1) % 4
                else:
                    raise ValueError("Invalid turn direction")
            elif move_direction == 'BW':
                if turn_direction == 'R':
                    new_index = (current_index - 1) % 4
                elif turn_direction == 'L':
                    new_index = (current_index + 1) % 4
                else:
                    raise ValueError("Invalid turn direction")
            return directions[new_index]

        def heuristic(current, state, target):
            turn_penalty = 35  # You can adjust this value based on how much you want to penalize turning
            forward_penalty = -15
            backwards_penalty = 15
            # Calculate Manhattan distance between current state and target
            distance = abs(state.x - target.x) + abs(state.y - target.y)

            if state.action == 'FW':
                if current is not None and current.action == 'BW':
                    return distance + 1000
                return distance + forward_penalty
            if state.action == 'BW':
                if current is not None and current.action == 'FW':
                    return distance + 1000
                return distance + backwards_penalty
            if state.action == 'BR':
                if current is not None and current.action == 'FR':
                    return distance + 1000
                return distance+turn_penalty
            if state.action == 'BL':
                if current is not None and current.action == 'FL':
                    return distance + 1000
                return distance+turn_penalty
            if state.action == 'FR':
                if current is not None and current.action == 'BR':
                    return distance + 1000
                return distance+turn_penalty
            if state.action == 'FL':
                if current is not None and current.action == 'BL':
                    return distance + 1000
                return distance+turn_penalty
            return distance
        
        
        # Use the Object3x3 instance to mark the object on the grid
        for x, y in object_positions:
            # print("Middle: ", object_positions[4])
            if (start[2] == 'N'):
                if (x, y) == (object_positions[4][0] - 1, object_positions[4][1]):
                    grid[x][y] = 'C'
            elif (start[2] == 'S'):
                if (x, y) == (object_positions[4][0] + 1, object_positions[4][1]):
                    grid[x][y] = 'C'
            elif (start[2] == 'E'):
                if (x, y) == (object_positions[4][0], object_positions[4][1] + 1):
                    grid[x][y] = 'C'
            elif (start[2] == 'W'):
                if (x, y) == (object_positions[4][0], object_positions[4][1] - 1):
                    grid[x][y] = 'C'
            else:
                grid[x][y] = 'X'

        start_time = time.time()

        start_state = State(start[0], start[1], start[2])
        target_state = State(target[0], target[1], target[2])

        start_node = Node(start_state, None, None, 0,
                          heuristic(None, start_state, target_state))
        priority_queue = [start_node]

        while priority_queue:
            current_node = heapq.heappop(priority_queue)
            eclipsed_time = time.time() - start_time
            if eclipsed_time > timeout:
                print("Timeout, Stopped Algo")
                path = []
                action = ['S']
                while current_node:
                    path.insert(0, current_node.coordinate)
                    current_node = current_node.parent
                return None, None
            if current_node.state == target_state:
                path = []
                #action = []
                temp = str("SNAP" + str(obs_id) + "_C")
                action = [temp]
                if current_node.parent:
                    parent_state = current_node.parent
                    target_state = current_node

                    # Dictionary to map relative positions and directions to actions
                    action_mapping = {
                        ((1, 0), 'N', 'N'): 'BW', ((-1, 0), 'S', 'S'): 'BW',
                        ((0, -1), 'E', 'E'): 'BW', ((0, 1), 'W', 'W' ): 'BW',
                        ((-1, 0), 'N', 'N'): 'FW', ((1, 0), 'S', 'S'): 'FW',
                        ((0, 1), 'E', 'E'): 'FW', ((0, -1), 'W', 'W'): 'FW',
                        ((1, 4), 'N', 'E'): 'FR', ((-1, -4), 'S', 'W'): 'FR',
                        ((4, 1), 'E', 'S'): 'FR', ((-4, -1), 'W', 'N'): 'FR',
                        ((-1, -4), 'N', 'W'): 'FL', ((1, 4), 'S', 'E'): 'FL',
                        ((-4, 1), 'E', 'N'): 'FL', ((4, -1), 'W', 'S'): 'FL',
                        ((4, 1), 'N', 'W'): 'BR', ((-4, -1), 'S', 'E'): 'BR',
                        ((1, -4), 'E', 'N'): 'BR', ((-1, 4), 'W', 'S'): 'BR',
                        ((4, -1), 'N', 'E'): 'BL', ((-4, 1), 'S', 'W'): 'BL',
                        ((-1, -4), 'E', 'S'): 'BL', ((1, 4), 'W', 'N'): 'BL',
                    }

                    # Determine the action based on the relative position and direction
                    relative_position = (
                        target_state.coordinate[0] - parent_state.coordinate[0], target_state.coordinate[1] - parent_state.coordinate[1])
                    relative_directions = parent_state.coordinate[2]
                    current_node.action = action_mapping.get(
                        (relative_position, relative_directions, target_state.coordinate[2]), 'S')
                while current_node:
                    if current_node.action is not None:
                        action.insert(0, current_node.action)
                    path.insert(0, current_node.coordinate)
                    current_node = current_node.parent
                    #print("My Path:", path)
                return path, action

            successors = get_successors(current_node.state, object_positions)
            if successors is None:
                return None

            for successor_state in successors:
                successor_node = Node(successor_state, current_node.state, successor_state.action, current_node.cost + 1,
                                      heuristic(current_node.state, successor_state, target_state))
                successor_node.action = (
                    successor_state.x, successor_state.y, successor_state.direction)

                # Set repeated_move flag
                if current_node.parent and current_node.parent.action == 'FW' and successor_node.action == 'BW':
                    successor_node.repeated_move = True
                elif current_node.parent and current_node.parent.action == 'BW' and successor_node.action == 'FW':
                    successor_node.repeated_move = True

                heapq.heappush(priority_queue, successor_node)

        return None
