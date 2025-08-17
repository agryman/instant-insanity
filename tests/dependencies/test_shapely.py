import math
from typing import Tuple

import pytest


def _parse_version(v: str) -> Tuple[int, int, int]:
    """Parse a semantic version string into a comparable (major, minor, patch) tuple.

    This is intentionally minimal to avoid adding a dependency on `packaging`.

    Args:
        v: Version string like '2.0.6' (extra suffixes are ignored).

    Returns:
        A (major, minor, patch) tuple of integers.
    """
    core = v.split('+', 1)[0].split('-', 1)[0]
    parts = (core.split('.') + ['0', '0', '0'])[:3]
    major, minor, patch = (int(p) for p in parts)
    return major, minor, patch


def test_shapely_import_and_version() -> None:
    """Import Shapely and assert we didn't accidentally install the wrong package.

    Verifies:
      * Module name is exactly 'shapely' (not 'shapley').
      * Version is >= 2.0.0 (Shapely 2+).
    """
    import shapely  # type: ignore[import-not-found]

    assert shapely.__name__ == 'shapely', 'Imported the wrong package (did you install shapley by mistake?)'
    assert hasattr(shapely, '__version__'), 'Shapely is missing a __version__ attribute'
    assert _parse_version(shapely.__version__) >= (2, 0, 0), (
        f'Expected Shapely >= 2.0.0, found {shapely.__version__}'
    )


def test_unit_disk_area_via_buffer() -> None:
    """Basic geometry sanity check using a 1-unit disk buffered from a point.

    Creates Point(0, 0).buffer(1) and checks area ≈ π. A higher resolution
    yields a smoother approximation without being slow.
    """
    from shapely.geometry import Point, Polygon  # type: ignore[import-not-found]

    disk = Point(0.0, 0.0).buffer(1.0, resolution=256)
    assert isinstance(disk, Polygon)
    assert disk.is_valid
    assert disk.area == pytest.approx(math.pi, rel=1e-3)


def test_union_and_intersection_consistency() -> None:
    """Two overlapping unit disks should satisfy inclusion–exclusion approximately.

    Places two unit disks with centers 1 unit apart. Checks:
      union.area ≈ a1 + a2 − inter.area, and
      inter.area < a1 (strict overlap).
    """
    from shapely.geometry import Point  # type: ignore[import-not-found]

    a = Point(0.0, 0.0).buffer(1.0, resolution=256)
    b = Point(1.0, 0.0).buffer(1.0, resolution=256)

    a1 = a.area
    a2 = b.area
    inter = a.intersection(b)
    uni = a.union(b)

    # Inclusion–exclusion
    assert uni.area == pytest.approx(a1 + a2 - inter.area, rel=1e-6, abs=1e-9)
    # Strict overlap
    assert inter.area < a1
