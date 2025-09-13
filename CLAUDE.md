# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This project creates animations showing how to solve the Instant Insanity puzzle using Graph Theory. It uses Manim Community Edition for mathematical animations and includes multiple Python packages for cube geometry, puzzle solving, and visualization.

## Development Commands

### Installation
```bash
pip install -e .
```

For updates when PyCharm doesn't pick up changes:
```bash
pip install -U -e .
```

### Testing
```bash
pytest
mypy src
```

### Utility Scripts
After installation, utility commands are available:
```bash
make-background-linen input.png  # Convert white backgrounds to LINEN color
```

Scripts are located in `src/instant_insanity/scripts/` and configured as entry points in `pyproject.toml`.

### Running Manim Animations
Manim scenes are located throughout the codebase. To run a specific scene:
```bash
manim src/path/to/scene.py SceneName
```

Key scene directories:
- `src/instant_insanity/scenes/graph_theory/` - Main puzzle visualization scenes
- `src/instant_insanity/scenes/demos/` - Demo scenes for components
- `src/manim_examples/` - General Manim learning examples

Each scene directory may have its own `manim.cfg` configuration file.

## Architecture

### Core Structure
- **`src/instant_insanity/core/`** - Fundamental geometry and puzzle logic
  - `cube.py` - Cube face/vertex definitions using standard 3D coordinate system
  - `puzzle.py` - Instant Insanity puzzle representation with Carteblanche 1947 notation
  - `geometry.py` - 3D geometric operations and transformations
  - `projection.py` - Orthographic projection for simulating 3D in 2D scenes
  
- **`src/instant_insanity/solvers/`** - Puzzle solving algorithms
  - `graph_solver.py` - Backtracking solver using opposite-face graph theory

- **`src/instant_insanity/mobjects/`** - Custom Manim objects
  - `puzzle_3d.py` - 3D puzzle visualization mobjects
  - `opposite_face_graph.py` - Graph theory visualization objects

- **`src/instant_insanity/animators/`** - Custom animation systems
  - `animorph.py` - Morphing animations between geometric shapes
  - `cube_animators.py` - Cube-specific animation behaviors

### Coordinate System
Uses standard 3D coordinate system where:
- x-axis: horizontal, left to right
- y-axis: vertical, bottom to top  
- z-axis: perpendicular to screen, back to front
- Standard cube occupies `[-1,1]³`

### Graph Theory Approach
The puzzle is solved using an "opposite-face graph" where each cube contributes edges between opposite face pairs. Solutions correspond to finding two independent 2-factors in this graph.

## Key Dependencies

**Core:**
- `manim` - Animation framework
- `numpy` - Numerical computations
- `networkx` - Graph algorithms
- `shapely` - Geometric operations

**Audio/Video:**
- `manim-voiceover[azure,gtts]` - Voiceover generation
- `ffmpeg` - Video processing

**Development:**
- `pytest` - Testing
- `mypy` - Type checking

## File Conventions

### Claude-Generated Code
- **General/one-off code**: Place in `src/claude/` directory
- **Tests for Claude code**: Place in `tests/claude/` directory, mirror the `src/claude/` structure
- **Project contributions**: Place under appropriate `src/instant_insanity/` subdirectory based on function
- Use `test_*.py` naming convention for all test files

### Project Structure
- Test files follow `test_*.py` naming convention in `tests/` directory
- MyPy configuration excludes examples directories but checks main source code

## Important Notes

- Python 3.11.11+ required (Google Colab compatibility)
- Avoid directory names conflicting with package names (especially `manim`)
- Use Cairo renderer for 2D scenes, OpenGL for 3D scenes (due to Cairo 3D rendering bugs)
- Voiceover text stored in `notebooks/voiceovers/` subdirectories

## Development Environment

The project is set up to work in PyCharm and Google Colab. Manim configuration files are distributed throughout scene directories to customize rendering settings per use case.