from typing import TypeAlias

from manim import Dot

from instant_insanity.core.cube import FaceName
from instant_insanity.core.puzzle import FaceColour, Puzzle, FaceColourPair, PuzzleCube, AXIS_TO_FACE_NAME_PAIR, \
    CARTEBLANCHE_PUZZLE, WINNING_MOVES_PUZZLE, CubeAxis
from instant_insanity.scenes.graph_theory.labelled_edge import LabelledEdge
from instant_insanity.scenes.graph_theory.quadrant import Quadrant

ColourToNodeMapping: TypeAlias = dict[FaceColour, Quadrant]
NodeToColourMapping: TypeAlias = dict[Quadrant, FaceColour]


def mk_colour_to_node(puzzle: Puzzle) -> ColourToNodeMapping:
    """
    Make the mapping of face colours to quadrants.
    The colours are sorted and then assigned to the quadrants to minimize diagonal crossovers.

    Args:
        puzzle: the puzzle

    Returns:
        a mapping of the face colours to quadrants as a dict.

    """
    # make the set of strictly increasing colour pairs
    colours: set[FaceColour] = puzzle.mk_colours()
    sorted_colours: list[FaceColour] = sorted(colours)
    colour_pairs: set[FaceColourPair] = {
        (colour_1, colour_2)
        for colour_1 in sorted_colours
        for colour_2 in sorted_colours
        if colour_1 < colour_2
    }

    # initialize the pair counts to 0
    colour_pair_to_count: dict[FaceColourPair, int] = {
        key: 0 for key in colour_pairs
    }

    # add the pair counts for the puzzle
    cube: PuzzleCube
    for cube in puzzle.number_to_cube.values():
        # add the pair counts for the cube
        name_1: FaceName
        name_2: FaceName
        for (name_1, name_2) in AXIS_TO_FACE_NAME_PAIR.values():
            # add the counts for the axis
            colour_1: FaceColour = cube.name_to_colour[name_1]
            colour_2: FaceColour = cube.name_to_colour[name_2]
            # ignore loops
            if colour_1 == colour_2:
                continue
            colour_min: FaceColour = min(colour_1, colour_2)
            colour_max: FaceColour = max(colour_1, colour_2)
            colour_pair_to_count[(colour_min, colour_max)] += 1

    # always assign sorted_colours[0] to quadrant I
    # compute the crossover counts when sorted_colours[i] is in quadrant III for i in 1, 2, 3

    # define short variable names for the sorted colours
    c0: FaceColour
    c1: FaceColour
    c2: FaceColour
    c3: FaceColour
    c0, c1, c2, c3 = tuple(sorted_colours)

    # define short variable names for the edge counts
    c01: int = colour_pair_to_count[(c0, c1)]
    c02: int = colour_pair_to_count[(c0, c2)]
    c03: int = colour_pair_to_count[(c0, c3)]
    c12: int = colour_pair_to_count[(c1, c2)]
    c13: int = colour_pair_to_count[(c1, c3)]
    c23: int = colour_pair_to_count[(c2, c3)]

    # define short variable names for the crossover counts
    cc1: int = c01 * c23
    cc2: int = c02 * c13
    cc3: int = c03 * c12

    # use the layout that has the minimum crossover count
    cc_min: int = min(cc1, cc2, cc3)
    node_layout: ColourToNodeMapping
    if cc1 == cc_min:
        node_layout = {
            c0: Quadrant.I,
            c1: Quadrant.III,
            c2: Quadrant.II,
            c3: Quadrant.IV
        }
    elif cc2 == cc_min:
        node_layout = {
            c0: Quadrant.I,
            c2: Quadrant.III,
            c1: Quadrant.II,
            c3: Quadrant.IV
        }
    else:
        assert cc3 == cc_min
        node_layout = {
            c0: Quadrant.I,
            c3: Quadrant.III,
            c1: Quadrant.II,
            c2: Quadrant.IV
        }

    return node_layout


CARTEBLANCHE_NODE_MAPPING: ColourToNodeMapping = mk_colour_to_node(CARTEBLANCHE_PUZZLE)
WINNING_MOVES_NODE_MAPPING: ColourToNodeMapping = mk_colour_to_node(WINNING_MOVES_PUZZLE)
NodeToMobjectMapping: TypeAlias = dict[Quadrant, Dot]
EdgeToMobjectMapping: TypeAlias = dict[CubeAxis, LabelledEdge]
EdgeToSubgraphMapping: TypeAlias = dict[CubeAxis, bool]
