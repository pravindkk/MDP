import tkinter as tk

from AlgoTask1 import AlgoFunctions


class GridSimulator:
    def __init__(self, root, rows, cols):
        self.rows = rows
        self.cols = cols
        self.cells = [[None] * cols for _ in range(rows)]
        self.steps = [] # List to store simulation steps
        self.current_step = 0 # Index of the current step
        self.obstacles = []
        self.create_input_boxes(root)
        self.create_grid(root)
        self.set_initial_colors()
        self.path = []

    def create_input_boxes(self, root):
        input_frame = tk.Frame(root)
        input_frame.grid(row=0, column=3, padx=10)

        # Entry for row input
        self.row_entry = tk.Entry(input_frame, width=5)
        self.row_entry.grid(row=0, column=3, padx=5, pady=5)
        tk.Label(input_frame, text="Row:").grid(row=0, column=2, padx=5, pady=5)

        # Entry for column input
        self.col_entry = tk.Entry(input_frame, width=5)
        self.col_entry.grid(row=1, column=3, padx=5, pady=5)
        tk.Label(input_frame, text="Column:").grid(row=1, column=2, padx=5, pady=5)
        
        # Entry for Obstacle direction input
        self.dir_entry = tk.Entry(input_frame, width=5)
        self.dir_entry.grid(row=2, column=3, padx=5, pady=5)
        tk.Label(input_frame, text="Direction:").grid(row=2, column=2, padx=5, pady=5)

        # Button to add a new obstacle based on input
        tk.Button(input_frame, text="Add Obstacle", command=self.add_obstacle).grid(row=3, column=2, columnspan=2, pady=5)
        
        # Button to reset obstacles
        tk.Button(input_frame, text="Reset Obstacles", command=self.reset_obstacles).grid(row=4, column=2, columnspan=2, pady=5)

        # Button to run the simulation
        tk.Button(input_frame, text="Run Simulation", command=self.run_simulation).grid(row=5, column=2, columnspan=2, pady=5)

        # Button to go Next Step
        tk.Button(input_frame, text="Next Step", command=self.next_step).grid(row=6, column=4, columnspan=2, pady=5)
        
        # Label to show the number of steps
        self.steps_label = tk.Label(input_frame, text="Steps: 0")
        self.steps_label.grid(row=6, column=2, columnspan=2, padx=5, pady=5)
        
        # Button to go Previous Step
        tk.Button(input_frame, text="Previous Step", command=self.previous_step).grid(row=6, column=0, columnspan=2, pady=5)

    def create_grid(self, root):
        grid_frame = tk.Frame(root)
        grid_frame.grid(row=0, column=0)

        for row in range(self.rows):
            for col in range(self.cols):
                cell = tk.Canvas(grid_frame, width=20, height=20, borderwidth=1, relief="solid")
                cell.grid(row=row, column=col, padx=1, pady=1)
                self.cells[row][col] = cell

    def set_initial_colors(self):
        # Set the bottom-left 3x3 of the grid to green
        for row in range(self.rows - 3, self.rows):
            for col in range(3):
                self.cells[row][col].config(bg="green")

        # Set the middle of the top row to red
        self.cells[17][1].config(bg="red")

    def add_obstacle(self):
        try:
            new_row = int(self.row_entry.get())
            new_col = int(self.col_entry.get())
            direction = self.dir_entry.get()

            if 0 <= new_row < self.rows and 0 <= new_col < self.cols and direction in ["n", "s", "e", "w", "N", "S", "E", "W"]:
                current_color = self.cells[new_row][new_col].cget("bg")
                if current_color not in ["red", "green"]:
                    print(f"Adding Obstacle at: ({new_row}, {new_col}), Direction: {direction}")
                    self.cells[new_row][new_col].config(bg="blue")
                    self.add_text_to_cell(new_row, new_col, direction.upper())
                    self.obstacles.append((new_row, new_col, direction.upper()))

                else:
                    print("Cannot add obstacle to a red or green cell.")
                
            else:
                print("Invalid row or column values.")
                
        except ValueError:
            print("Invalid input. Please enter integer values for row and column.")

    def add_text_to_cell(self, row, col, text):
        # Clear existing text in the cell
        self.cells[row][col].delete("all")
        # Add new text to the cell
        self.cells[row][col].create_text(13, 13, text=text, anchor="center")

    def reset_obstacles(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.cells[row][col].config(bg="white") # Reset the color to white
                self.add_text_to_cell(row, col, "") # Remove text
        self.set_initial_colors()
        self.obstacles = []
        self.steps = []  # Reset the steps list as well
        self.path = []
        self.run_simulation()
        self.update_steps_label()

    def save_obstacles_to_data(self):
        data = {
            'obstacles': [
                {
                    'x': obstacle[0],
                    'y': obstacle[1],
                    'id': index +  1,  # Assuming 'id' starts from  1
                    'd': obstacle[2]   # Direction is still stored as 'N','S','E','W' (Have to change to numerical but we have to see how the algo is implemented first)
                }
                for index, obstacle in enumerate(self.obstacles)
            ]
        }
        return data

    def run_simulation(self):
        print("Running simulation...")
        if(self.obstacles != []):
            #("Obstacles: ", self.obstacles)
            data = self.save_obstacles_to_data()
            print("Data: ", data)
            self.path, self.final_grid = AlgoFunctions.NearestNeighbourSearch(data)
            # Run below code if obstacles are list of tuples
            #self.path, self.final_grid = AlgoFunctions.NearestNeighbourSearch(self.obstacles)
        print("Ended Simulation")
        self.steps = self.path
        self.steps_fatten = [item for sub_list in self.path for item in sub_list]
        #print("All Path Movements:", self.steps_fatten)
        self.update_steps_label()

    def next_step(self):
        if self.current_step < len(self.steps_fatten) - 1:
            self.current_step += 1
        else:
            self.current_step = 0  # Loop back to the beginning if reached the end
        self.update_grid()
        self.update_steps_label()

    def previous_step(self):
        if self.current_step > 0:
            self.current_step -= 1
        else:
            self.current_step = len(self.steps_fatten) - 1  # Loop back to the end if reached the beginning
        self.update_grid()
        self.update_steps_label()

    def update_steps_label(self):
        total_steps = len(self.steps_fatten)
        current_step_number = self.current_step + 1
        self.steps_label.config(text=f"Step: {current_step_number}/{total_steps}")

    def update_grid(self):
        # Clear the grid by setting all cells to white
        for row in range(self.rows):
            for col in range(self.cols):
                current_color = self.cells[row][col].cget("bg")
                if current_color not in ["blue"]:
                    self.cells[row][col].config(bg="white")
                    self.add_text_to_cell(row, col, "")

        # Get the current position from the flattened steps list
        current_position = self.steps_fatten[self.current_step]

        #print("Current Position : ", current_position)

        # Update the grid to reflect the current position of the robot
        #self.cells[current_position[0]][current_position[1]].config(bg="red")
        self.colour_car_position(current_position[0], current_position[1], current_position[2])

        # Update the labels to show the current step number
        self.update_steps_label()

    def print_grid(self):
        print(self.path)

    def colour_car_position(self, row, col, direction):

        if(direction == 'N'):
            position_center_x = row+1
            position_center_y = col
        elif(direction == 'S'):
            position_center_x = row-1
            position_center_y = col
        elif(direction == 'E'):
            position_center_x = row
            position_center_y = col-1
        elif(direction == 'W'):
            position_center_x = row
            position_center_y = col+1
        else:
            position_center_x = row
            position_center_y = col
        
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                self.cells[position_center_x + dx][position_center_y + dy].config(bg="green")

        self.cells[row][col].config(bg="red")

        return None


def main():
    root = tk.Tk()
    root.title("Grid Simulator")

    rows, cols = 20, 20
    simulator = GridSimulator(root, rows, cols)

    root.mainloop()

if __name__ == "__main__":
    main()
