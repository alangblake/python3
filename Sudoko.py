import tkinter as tk
from tkinter import messagebox

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.cells = {}
        self.original_numbers = set()  # To track initial numbers
        self.solving = False  # Flag to prevent multiple solves
        self.create_board()
        self.create_buttons()

    def create_board(self):
        # Create main frame for the board
        main_frame = tk.Frame(self.root, bg='black')
        main_frame.grid(row=0, column=0, padx=10, pady=10)
        
        # Create 3x3 section frames
        section_frames = []
        for i in range(3):
            row_frames = []
            for j in range(3):
                frame = tk.Frame(main_frame, bg='black', padx=1, pady=1)
                frame.grid(row=i, column=j, padx=2, pady=2)
                row_frames.append(frame)
            section_frames.append(row_frames)

        # Create 9x9 grid of entry widgets
        for i in range(9):
            for j in range(9):
                # Calculate which section frame to use
                section_i, section_j = i // 3, j // 3
                cell_i, cell_j = i % 3, j % 3
                
                # Create a frame for each cell with light grey border
                cell_frame = tk.Frame(section_frames[section_i][section_j], bg='lightgrey')
                cell_frame.grid(row=cell_i, column=cell_j, padx=1, pady=1)
                
                # Create the entry widget
                cell = tk.Entry(cell_frame, width=2, font=('Arial', 18), justify='center')
                cell.pack(padx=1, pady=1)
                cell.insert(0, "")
                cell.bind('<KeyRelease>', lambda e, row=i, col=j: self.validate_input(e, row, col))
                self.cells[(i, j)] = cell

    def create_buttons(self):
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=1, column=0, pady=10)
        
        solve_button = tk.Button(button_frame, text="Solve", command=self.solve)
        solve_button.pack(side=tk.LEFT, padx=5)
        
        clear_button = tk.Button(button_frame, text="Clear", command=self.clear_board)
        clear_button.pack(side=tk.LEFT, padx=5)

    def validate_input(self, event, row, col):
        cell = self.cells[(row, col)]
        value = cell.get()
        
        # Clear cell if input is empty
        if value == "":
            return True
            
        # Validate input is a single digit
        if (not value.isdigit() or len(value) > 1 or int(value) < 1 or int(value) > 9):
            cell.delete(0, tk.END)
            return False
            
        return True

    def get_board(self):
        board = []
        self.original_numbers.clear()  # Reset original numbers
        for i in range(9):
            row = []
            for j in range(9):
                value = self.cells[(i, j)].get()
                if value.isdigit():
                    self.original_numbers.add((i, j))  # Track initial positions
                    row.append(int(value))
                else:
                    row.append(0)
            board.append(row)
        return board

    def set_board(self, board):
        for i in range(9):
            for j in range(9):
                self.cells[(i, j)].delete(0, tk.END)
                if board[i][j] != 0:
                    self.cells[(i, j)].insert(0, str(board[i][j]))
                    # Set color based on whether it's an original number
                    if (i, j) in self.original_numbers:
                        self.cells[(i, j)].config(fg='black')
                    else:
                        self.cells[(i, j)].config(fg='blue')

    def clear_board(self):
        for cell in self.cells.values():
            cell.delete(0, tk.END)
            cell.config(fg='black')  # Reset text color
        self.original_numbers.clear()
        self.solving = False

    def is_valid(self, board, row, col, num):
        # Check row
        for x in range(9):
            if board[row][x] == num:
                return False

        # Check column
        for x in range(9):
            if board[x][col] == num:
                return False

        # Check 3x3 box
        start_row = row - row % 3
        start_col = col - col % 3
        for i in range(3):
            for j in range(3):
                if board[i + start_row][j + start_col] == num:
                    return False

        return True

    def solve_sudoku(self, board):
        empty = self.find_empty(board)
        if not empty:
            return True

        row, col = empty
        for num in range(1, 10):
            if self.is_valid(board, row, col, num):
                board[row][col] = num
                # Only store solution steps for non-original numbers
                if (row, col) not in self.original_numbers:
                    self.solution.append((row, col, num))
                if self.solve_sudoku(board):
                    return True
                board[row][col] = 0
                if (row, col) not in self.original_numbers:
                    self.solution.pop()  # Remove failed attempt

        return False

    def find_empty(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return (i, j)
        return None

    def solve(self):
        if self.solving:
            return
        self.solving = True
        board = self.get_board()
        self.solution = []  # Store solution steps
        self.current_solution_step = 0  # Track current solution step
        if self.solve_sudoku(board):
            self.animate_solution(0)  # Start animation
        else:
            messagebox.showerror("Error", "No solution exists for this puzzle!")
            self.solving = False

    def animate_solution(self, step):
        if step < len(self.solution):
            i, j, final_num = self.solution[step]
            self.animate_number(i, j, 1, final_num)
        else:
            self.solving = False  # Reset solving flag when done
            
    def animate_number(self, i, j, current, final_num):
        cell = self.cells[(i, j)]
        cell.delete(0, tk.END)
        cell.insert(0, str(current))
        cell.config(fg='blue')
        
        if current < final_num:
            # Continue counting up
            self.root.after(333, self.animate_number, i, j, current + 1, final_num)
        else:
            # Move to next solution number
            self.root.after(333, self.animate_solution, self.current_solution_step + 1)
            self.current_solution_step += 1

def main():
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
