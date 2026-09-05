"""
This module checks the dependency direction between the top-level packages
under src/.

The reusable code is being refactored into separate public repos in the
kwargs-xyz organisation. That refactoring happens inside this repo, because
PyCharm cannot rename or move code across repo boundaries. The cost of sharing
one source tree is that nothing stops a package from importing one that is meant
to sit above it: in separate repos an upward import fails immediately, because
the package is simply not installed, but here it succeeds and the mistake only
surfaces when the packages are pulled apart.

These tests restore that constraint. ALLOWED_IMPORTS records which top-level
packages each package may import, and a package that does not exist yet is
skipped, so this file can be added before the refactoring starts.
"""

import ast
from pathlib import Path

SRC_DIR: Path = Path(__file__).parent.parent / 'src'

# For each top-level package under src/, the other top-level packages it is
# allowed to import. Read the table as layers, lowest first:
#
#   manim_cairo3d      generic Cairo 3D rendering, depends on nothing of ours
#   kwargs_xyz_core    generic manim infrastructure, depends on nothing of ours
#   kwargs_xyz_studio  kwargs.xyz identity, built on core
#   instant_insanity_core
#                      puzzle logic, built on the generic layers
#   instant_insanity_scenes   the private film: scenes and resources, may use anything
ALLOWED_IMPORTS: dict[str, frozenset[str]] = {
    'manim_cairo3d': frozenset(),
    'kwargs_xyz_core': frozenset(),
    'kwargs_xyz_studio': frozenset({'kwargs_xyz_core'}),
    'instant_insanity_core': frozenset({'kwargs_xyz_core', 'manim_cairo3d'}),
    'instant_insanity_scenes': frozenset({
        'kwargs_xyz_core',
        'kwargs_xyz_studio',
        'instant_insanity_core',
        'manim_cairo3d'
    })
}


def get_imported_top_level_packages(module_path: Path) -> set[str]:
    """Finds the top-level packages that a module imports.

    Only the packages named in ALLOWED_IMPORTS are reported, since third-party
    and standard library imports are not constrained.

    Args:
        module_path: The Python source file to scan.

    Returns:
        The names of the constrained top-level packages that the module imports.
    """
    tree: ast.Module = ast.parse(module_path.read_text(), filename=str(module_path))
    imported: set[str] = set()

    node: ast.AST
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported.add(alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            # node.module is None for a relative import, which stays inside the
            # package and so can never cross a boundary.
            if node.level == 0 and node.module is not None:
                imported.add(node.module.split('.')[0])

    return imported & ALLOWED_IMPORTS.keys()


def get_modules(package: str) -> list[Path]:
    """Finds the Python source files of a top-level package under src/.

    Args:
        package: The name of the top-level package.

    Returns:
        The source files, or an empty list if the package does not exist yet.
    """
    package_dir: Path = SRC_DIR / package
    if not package_dir.is_dir():
        return []

    return sorted(package_dir.rglob('*.py'))


def test_packages_only_import_lower_layers() -> None:
    """Checks that no package imports one that sits above it."""
    violations: list[str] = []

    package: str
    allowed: frozenset[str]
    for package, allowed in ALLOWED_IMPORTS.items():
        permitted: frozenset[str] = allowed | {package}

        module_path: Path
        for module_path in get_modules(package):
            forbidden: set[str] = get_imported_top_level_packages(module_path) - permitted
            if forbidden:
                relative: Path = module_path.relative_to(SRC_DIR)
                violations.append(f'{relative} imports {sorted(forbidden)}')

    assert not violations, 'Forbidden imports:\n' + '\n'.join(violations)


def test_allowed_imports_are_themselves_known_packages() -> None:
    """Checks that ALLOWED_IMPORTS does not name a package it does not define."""
    package: str
    allowed: frozenset[str]
    for package, allowed in ALLOWED_IMPORTS.items():
        unknown: set[str] = allowed - ALLOWED_IMPORTS.keys()
        assert not unknown, f'{package} is allowed to import unknown packages: {sorted(unknown)}'
