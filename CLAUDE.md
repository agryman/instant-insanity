# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This project creates animations showing how to solve the Instant Insanity puzzle using Graph Theory. 
It uses Manim Community Edition to create mathematical animations
It includes Python packages for cube geometry, puzzle solving, and visualization.

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
make-greyscale input.png         # Make a greyscale copy of an image for annotation
```

Scripts are located in `src/instant_insanity_core/scripts/` and configured as entry points in `pyproject.toml`.

An editable install keeps source changes live, but it does **not** pick up new
`[project.scripts]` entries. The wrapper executables in `venv/bin/` are generated only
when pip installs the package, so a newly added command will be missing from the venv
until you reinstall:
```bash
pip install -e . --no-deps  # --no-deps skips re-resolving the dependency tree
```
Rerun this whenever an entry in `[project.scripts]` is added or renamed.

### Running Manim Animations
Manim scenes are located throughout the codebase. To run a specific scene:
```bash
manim src/path/to/scene.py SceneName
```

Key scene directories:
- `src/instant_insanity_scenes/scenes/graph_theory/` - Main puzzle visualization scenes
- `src/instant_insanity_core/demos/` - Demo scenes for components
- `src/manim_examples/` - General Manim learning examples

Each scene directory may have its own `manim.cfg` configuration file.

## Changing Files

Do not modify any file in this repository without Arthur's explicit confirmation for
that specific change. This applies to source, tests, and configuration alike. Running
`mypy` or `pytest` and finding a problem is not confirmation to fix it, and neither is
Arthur stating an expectation such as "everything should typecheck". Report what is
wrong, propose a fix, and wait.

To propose a change, write the modified copy to the scratchpad directory (never over the
original) and open it in a PyCharm diff window against the real file:

```bash
PYCHARM="$HOME/Library/Application Support/JetBrains/Toolbox/scripts/pycharm2"
"$PYCHARM" diff /abs/path/to/original.py /abs/path/to/scratchpad/original.proposed.py
```

Both paths must be absolute. Keep the `.py` suffix on the proposed copy so PyCharm
applies syntax highlighting. Arthur reviews the diff and can accept it directly in that
window; only apply the change to the real file once he says so.

Exceptions, which still need the change itself to be asked for: files Arthur explicitly
names as the target of the request, and throwaway files inside the scratchpad directory.

## Refactoring

Arthur performs all Python refactorings himself in PyCharm. This covers renaming and
moving packages, modules, classes, functions and variables, extracting code, and
changing signatures. Do not carry these out with `sed`, file moves, or a search and
replace sweep, and do not offer to.

PyCharm updates every reference in one safe operation. A hand-rolled sweep silently
misses references in strings, docstrings and configuration, and a name that is a prefix
of another name, such as `instant_insanity_scenes` and `instant_insanity_core`, will be
corrupted by a careless pattern.

Instead, describe the refactoring precisely enough for Arthur to run it: which PyCharm
action to invoke, on what, and what the result should be. Then do the work PyCharm does
not do. It only updates Python references, so the follow-up usually includes
`pyproject.toml` entry points and `package-data` keys, `manim.cfg` files, the mirrored
directories under `tests/`, and the prose in `CLAUDE.md` and the Makefile. Reinstall with
`pip install -e . --no-deps` when an entry point moved, then verify with `mypy src` and
`pytest`.

## Git

Arthur performs all git operations himself using GitHub Desktop. Do not run any git
command unless he explicitly asks for it in that request. This includes, but is not
limited to, `git commit`, `git add`, `git mv`, `git rm`, `git checkout`, `git branch`,
`git merge`, `git push`, and `git pull`. Do not offer to run them either.

When a change would normally involve git, such as renaming or deleting a file, make the
change with ordinary file operations and let Arthur stage and commit it in GitHub Desktop.
Describe what changed in terms of files rather than suggesting git commands to run.

Read-only inspection is fine, such as `git status`, `git diff`, and `git log`, when it
helps answer a question or verify work.

## Architecture

### Core Structure
- **`src/instant_insanity_scenes/core/`** - Fundamental geometry and puzzle logic
  - `cube.py` - Cube face/vertex definitions using standard 3D coordinate system
  - `puzzle.py` - Instant Insanity puzzle representation with Carteblanche 1947 notation
  - `geometry.py` - 3D geometric operations and transformations
  - `projection.py` - Orthographic projection for simulating 3D in 2D scenes
  
- **`src/instant_insanity_core/solvers/`** - Puzzle solving algorithms
  - `graph_solver.py` - Backtracking solver using opposite-face graph theory

- **`src/instant_insanity_core/mobjects/`** - Custom Manim objects
  - `puzzle_3d.py` - 3D puzzle visualization mobjects
  - `opposite_face_graph.py` - Graph theory visualization objects

- **`src/instant_insanity_core/animorphs/`** - Custom animation systems
  - `animorph.py` - Morphing animations between geometric shapes
  - `cube_animorphs.py` - Cube-specific animation behaviors

### Coordinate System
Uses standard 3D coordinate system where:
- x-axis: horizontal, increasing from left to right
- y-axis: vertical, increasing from bottom to top  
- z-axis: perpendicular to screen, increasing from back to front
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
- **Project contributions**: Place under appropriate `src/instant_insanity_scenes/` subdirectory based on function
- Use `test_*.py` naming convention for all test files

### Project Structure
- Test files follow `test_*.py` naming convention in `tests/` directory
- MyPy configuration excludes examples directories but checks main source code

## Important Notes

- Python 3.12+ required (Google Colab compatibility)
- Avoid directory names conflicting with package names (especially `manim`)
- Use Cairo renderer for 2D scenes
- Do not use Cairo or OpenGL renderer for 3D scenes
- Cairo 3D has rendering bugs
- Always use Cairo 2D scenes since the code is stable
- Use custom `core.depth_sort.py` and `core.projection.py` modules to render 3D scenes in 2D Cairo
- Voiceover text is stored in `notebooks/voiceovers/` subdirectories

## Development Environment

The project is set up to work in PyCharm and Google Colab. 
Google Colab was used in the initial stages of development for sharing content with Will but
is now no longer needed since I am working alone and using manim.

As of 2026-07-10, Google Colab uses Python 3.12 as the default version.
Try to avoid features that do not work in Python 3.12.
However, Colab compatibility is not a hard requirement anymore.
It may be useful later in the project if I made any Jupyter notebooks publicly available.


Manim configuration files are distributed throughout scene directories to customize rendering settings per use case.