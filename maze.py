"""Implemention of the Maze ADT using a 2-D array."""
from arrays import Array2D
from lliststack import Stack


class Maze:
    """Define constants to represent contents of the maze cells."""
    MAZE_WALL = "*"
    PATH_TOKEN = "x"
    TRIED_TOKEN = "o"

    def __init__(self, num_rows, num_cols):
        """Creates a maze object with all cells marked as open."""
        self._maze_cells = Array2D(num_rows, num_cols)
        self._start_cell = None
        self._exit_cell = None

    def num_rows(self):
        """Returns the number of rows in the maze."""
        return self._maze_cells.num_rows()

    def num_cols(self):
        """Returns the number of columns in the maze."""
        return self._maze_cells.num_cols()

    def set_wall(self, row, col):
        """Fills the indicated cell with a "wall" marker."""
        assert row >= 0 and row < self.num_rows() and \
            col >= 0 and col < self.num_cols(), "Cell index out of range."
        self._maze_cells[row, col] = self.MAZE_WALL

    def set_start(self, row, col):
        """Sets the starting cell position."""
        assert row >= 0 and row < self.num_rows() and \
            col >= 0 and col < self.num_cols(), "Cell index out of range."
        self._start_cell = _CellPosition(row, col)

    def set_exit(self, row, col):
        """Sets the exit cell position."""
        assert row >= 0 and row < self.num_rows() and \
            col >= 0 and col < self.num_cols(), "Cell index out of range."
        self._exit_cell = _CellPosition(row, col)

    def find_path(self):
        """
        Attempts to solve the maze by finding a path from the starting cell
        to the exit. Returns True if a path is found and False otherwise.
        """
        self._maze_cells[self._start_cell.row,
                         self._start_cell.col] = self.PATH_TOKEN
        stack = Stack()
        stack.push((self._start_cell.row, self._start_cell.col))
        way = [(-1,0), (0, 1), (1, 0), (0, -1)]
        while not stack.is_empty() and stack.peek() != (self._exit_cell.row, self._exit_cell.col) :
            flag = False
            for row_index, col_index in way:
                try:
                    current_cell = stack.peek()
                    # assert isinstance(current_cell, Maze)
                    if self._maze_cells[current_cell[0] +\
                                            row_index, current_cell[1] + \
                                                col_index] not in ['*', 'o', 'x']:
                        self._maze_cells[current_cell[0] + row_index,
                                            current_cell[1] + col_index] = self.PATH_TOKEN
                        stack.push(
                            (current_cell[0] + row_index, current_cell[1] + col_index))
                        flag = True
                        break
                except AssertionError:
                    pass
                except IndexError:
                    pass
            if not flag:
                trial_cell = stack.pop()
                self._maze_cells[trial_cell[0],
                                 trial_cell[1]] = self.TRIED_TOKEN
                # print(maze)
        if stack.is_empty():
            return False
        return True

    def reset(self):
        """Resets the maze by removing all "path" and "tried" tokens."""
        for i in range(self.num_rows()):
            for j in range(self.num_cols()):
                self._maze_cells[i, j] = self.MAZE_WALL \
                    if self._maze_cells[i, j] == self.MAZE_WALL else None

    def __str__(self):
        """Returns a text-based representation of the maze."""
        maze_line = ''
        for i in range(self.num_rows()):
            for j in range(self.num_cols()):
                maze_line += self._maze_cells[i, j] + ' ' \
                    if self._maze_cells[i, j] is not None else '_ '
            maze_line = maze_line + '\n'
        return maze_line[:-1]

    def _valid_move(self, row, col):
        """Returns True if the given cell position is a valid move."""
        return row >= 0 and row < self.num_rows() \
            and col >= 0 and col < self.num_cols() \
            and self._maze_cells[row, col] is None

    def _exit_found(self, row, col):
        """Helper method to determine if the exit was found."""
        return row == self._exit_cell.row and col == self._exit_cell.col

    def _mark_tried(self, row, col):
        """Drops a "tried" token at the given cell."""
        self._maze_cells[row, col] = self.TRIED_TOKEN

    def _mark_path(self, row, col):
        """Drops a "path" token at the given cell."""
        self._maze_cells[row, col] = self.PATH_TOKEN


class _CellPosition(object):
    """Private storage class for holding a cell position."""

    def __init__(self, row, col):
        self.row = row
        self.col = col


def build_maze(path):
    """_summary_

    Args:
        path (_type_): _description_

    Returns:
        _type_: _description_
    >>> 1 == 1
    True
    """
    with open(path, 'r', encoding='utf-8') as file:
        lines = file.read().split('\n')
    num_rows = [int(value) for value in lines[0].split()][0]
    num_cols = [int(value) for value in lines[0].split()][1]

    in_cell_row = [int(value) for value in lines[1].split()][0]
    in_cell_col = [int(value) for value in lines[1].split()][1]

    out_cell_row = [int(value) for value in lines[2].split()][0]
    out_cell_col = [int(value) for value in lines[2].split()][1]

    maze = Maze(num_cols=num_cols, num_rows=num_rows)
    maze.set_start(col=in_cell_col, row=in_cell_row)
    maze.set_exit(col=out_cell_col, row=out_cell_row)

    for idx, line in enumerate(lines[3:-1]):
        while len(line) < num_cols:
            line += ' '
        line = line.replace(' ', '_ ')
        lines[idx+3] = line.replace('*', '* ')[:-1]
        for symbol_idx, symbol in enumerate(lines[idx+3].split(' ')):
            maze._maze_cells[idx, symbol_idx] = symbol.strip()
    return maze


maze = build_maze('mazefile.txt')
print(maze)
print(maze.find_path())
print(maze)
maze.reset()
print(maze)
