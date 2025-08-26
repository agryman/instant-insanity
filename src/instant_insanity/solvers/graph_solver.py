"""
This module implements a backtracking solver on the opposite-face graph.
It is modelled on the Sudoku solver described in "Conceptual Programming with Python", p96.
"""
from instant_insanity.core.cube import FaceName
from instant_insanity.core.puzzle import Puzzle, AxisLabel, PuzzleCubeNumber, FaceColour, AXIS_TO_FACE_NAME_PAIR, \
    FaceNamePair, PuzzleCube, CARTEBLANCHE_PUZZLE, WINNING_MOVES_PUZZLE

type GridRow = FaceName
type GridColumn = PuzzleCubeNumber
type GridKey = tuple[GridRow, GridColumn]
type GridValue = AxisLabel | None

GRID_ROWS: list[GridRow] = [FaceName.FRONT, FaceName.TOP]
GRID_COLUMNS: list[GridColumn] = list(PuzzleCubeNumber)

# a spectrum counts the frequency of all the possible face colours
# a spectrum is the same as the total degree of each node in a subgraph of the opposite-face graph
type Spectrum = dict[FaceColour, int]

def zero_spectrum() -> Spectrum:
    """
    Initialize the spectrum to be all zeroes.

    Returns:
        the initialized spectrum.
    """
    spectrum: Spectrum = {face_colour: 0 for face_colour in FaceColour}
    return spectrum

def is_possible_two_factor_spectrum(spectrum: Spectrum) -> bool:
    """
    Determine if the spectrum is possible for a 2-factor.
    All values of the spectrum MUST be <= 2.

    Args:
        spectrum: the spectrum to be checked.

    Returns:
        True if the spectrum is possible, False otherwise.
    """
    return max(spectrum.values()) <= 2

class GraphSolver:
    puzzle: Puzzle
    colours: list[FaceColour]
    grid: dict[GridKey, GridValue]

    def __init__(self, puzzle: Puzzle) -> None:
        """

        Args:
            puzzle: the puzzle.
        """
        self.puzzle = puzzle
        self.colours = puzzle.get_colours()
        assert len(self.colours) == 4

        self.grid = {(row, column) : None
                     for row in GRID_ROWS
                     for column in GRID_COLUMNS}

    def get_spectrum(self, cube_number: PuzzleCubeNumber, axis_label: AxisLabel) -> Spectrum:
        """
        Get the spectrum for the given cube number and axis label.
        An axis defines an edge of the opposite-face graph.
        The spectrum is the total degree of each colour node.

        Args:
            cube_number: the puzzle cube number.
            axis_label: the axis label.

        Returns:
            the spectrum
        """
        spectrum: Spectrum = zero_spectrum()
        cube: PuzzleCube = self.puzzle.number_to_cube[cube_number]
        face_name_pair: FaceNamePair = AXIS_TO_FACE_NAME_PAIR[axis_label]
        face_name: FaceName
        for face_name in face_name_pair:
            face_colour: FaceColour = cube.name_to_colour[face_name]
            spectrum[face_colour] += 1

        return spectrum

    def get_spectrum_for_key(self, key: GridKey) -> Spectrum:
        """
        Gets the spectrum for a grid key.
        The value at the key represents a subgraph of the opposite-face graph.
        If the value is empty then the subgraph is empty and the spectrum is the zero spectrum.
        If the value contains an axis label then the subgraph is the edge defined by the cube number of the key
        and the axis label.

        Args:
            key: the grid key.

        Returns:
            the spectrum of the grid key.
        """
        value: GridValue = self.grid[key]
        if value is None:
            return zero_spectrum()

        assert isinstance(value, AxisLabel)
        axis_label: AxisLabel = value

        cube_number: GridColumn
        _, cube_number = key

        return self.get_spectrum(cube_number, axis_label)

    def get_spectrum_for_row(self, row: GridRow) -> Spectrum:
        """
        Get the spectrum for a grid row.
        The spectrum for the row is the spectrum for the subgraph defined by all the
        edges in the row. This is the sum of the spectra for each value in the row.

        Args:
            row: the grid row.

        Returns:
            the spectrum.
        """
        spectrum: Spectrum = zero_spectrum()
        for column in GRID_COLUMNS:
            key: GridKey = (row, column)
            if self.grid[key] is None:
                # this is an optimization because rows are filled in from left to right
                break
            key_spectrum: Spectrum = self.get_spectrum_for_key(key)
            for face_colour in spectrum.keys():
                spectrum[face_colour] += key_spectrum[face_colour]

        return spectrum


    def is_possible(self, row: GridRow, column: GridColumn, value: AxisLabel) -> bool:
        """
        Is it possible to put axis_label in the grid at (row, column)?
        Args:
            row: the row.
            column: the column.
            value: the value to check.

        Returns:
            True if it is possible to assign the value to the grid, False otherwise.
        """
        key: GridKey = (row, column)

        # confirm that the grid cell is currently empty
        assert self.grid[key] is None

        # confirm that we are filling the grid in left-to-right, top-to-bottom order
        row_index: int = GRID_ROWS.index(row)
        if row_index > 0:
            assert self.grid[(GRID_ROWS[row_index - 1], column)] is not None
        column_index: int = GRID_COLUMNS.index(column)
        if column_index > 0:
            assert self.grid[(row, GRID_COLUMNS[column_index - 1])] is not None

        message_prefix: str = f'(row={row}, column={column}, value={value}: '

        # it is always possible to put any value, other than z, in the first cell of the grid
        if row == GRID_ROWS[0] and column == GRID_COLUMNS[0]:
            if value == AxisLabel.Z:
                print(f'{message_prefix} value z here would lead to a previously found solution.')
            else:
                print(f'{message_prefix} OK')
            return True

        # the values for cube 1 should be strictly ordered to avoid prior solution
        if row == GRID_ROWS[1] and column == GRID_COLUMNS[0]:
            value_0_0: GridValue = self.grid[(GRID_ROWS[0], GRID_COLUMNS[0])]
            assert isinstance(value_0_0, AxisLabel)
            if value < value_0_0:
                print(f'{message_prefix} value {value} here would lead to a previously found solution.')
                return False

        # it is never possible to put the same value in both rows of a column
        if row == GRID_ROWS[1]:
            if value == self.grid[(GRID_ROWS[0], column)]:
                print(f'{message_prefix} value is already used in column')
                return False

        row_spectrum: Spectrum = self.get_spectrum_for_row(row)
        value_spectrum: Spectrum = self.get_spectrum(column, value)
        face_colour: FaceColour
        total_spectrum: Spectrum = {face_colour: row_spectrum[face_colour] + value_spectrum[face_colour]
                                    for face_colour in FaceColour}
        if not is_possible_two_factor_spectrum(total_spectrum):
            print(f'{message_prefix} exceeds colour limits')
            return False

        print(f'{message_prefix} OK')
        return True

    def print_grid(self):
        for row in GRID_ROWS:
            for column in GRID_COLUMNS:
                value: GridValue = self.grid[(row, column)]
                if value is None:
                    print('.', end=' ')
                else:
                    print(value.value, end=' ')
            print()


    def solve(self) -> None:
        """
        Solve the puzzle.
        """
        for row in GRID_ROWS:
            for column in GRID_COLUMNS:
                if self.grid[(row, column)] is None:
                    for value in AxisLabel:
                        if self.is_possible(row, column, value):
                            self.grid[(row, column)] = value
                            self.solve()
                            print(f'(row={row}, column={column}, value={value}: backtracking')
                            self.grid[(row, column)] = None
                    return
        self.print_grid()

WINNING_MOVES_GRAPH_SOLVER: GraphSolver = GraphSolver(puzzle=WINNING_MOVES_PUZZLE)
CARTEBLANCHE_GRAPH_SOLVER: GraphSolver = GraphSolver(puzzle=CARTEBLANCHE_PUZZLE)

if __name__ == "__main__":
    WINNING_MOVES_GRAPH_SOLVER.solve()
