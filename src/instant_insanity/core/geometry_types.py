"""Geometry type aliases and validation helpers.

This module defines explicit, self-documenting type aliases for polygon geometry
data and related mappings, plus small runtime checkers/converters that you can
reuse across your codebase.

Conventions:
    - Vertex: a single 3D point (float64), shape (3,)
    - VertexPath: ordered polygon boundary vertices, shape (n, 3), start is not repeated
    - PolygonId: opaque unique identifier for a polygon (e.g., 'front_face', 'A12', UUID)
    - PolygonIdToVertexPathMapping: mapping from PolygonId -> VertexPath (data)
    - PolygonIdToPolygonMapping: mapping from PolygonId -> Manim Polygon (object)

Notes:
    - We use NewType for PolygonId to get compile-time separation from plain str and
      other ID types (e.g., FaceId) while keeping zero runtime overhead.

"""
from typing import NewType, TypeAlias, OrderedDict

import numpy as np
from numpy.typing import NDArray

from manim import Polygon

__all__ = [
    'Vector',
    'Vertex',
    'VertexPath',
    'PolygonId',
    'PolygonIdToVertexPathMapping',
    'PolygonIdToPolygonMapping',
    'SortedPolygonIdToVertexPathMapping',
    'SortedPolygonIdToPolygonMapping',
    'is_vertex',
    'is_vertex_path',
    'check_vertex',
    'check_vertex_path',
    'as_vertex',
    'as_vertex_path',
]

# --- Core data types ---
Vector: TypeAlias = NDArray[np.float64]          # shape (3,)
Vertex: TypeAlias = NDArray[np.float64]          # shape (3,)
VertexPath: TypeAlias = NDArray[np.float64]      # shape (n, 3)

# --- Identifiers ---
PolygonId = NewType('PolygonId', str)            # opaque unique ID for a polygon

# --- Mappings ---
PolygonIdToVertexPathMapping: TypeAlias = dict[PolygonId, VertexPath]
PolygonIdToPolygonMapping: TypeAlias = dict[PolygonId, Polygon]

# --- Sorted Mappings ---
SortedPolygonIdToVertexPathMapping: TypeAlias = OrderedDict[PolygonId, VertexPath]
SortedPolygonIdToPolygonMapping: TypeAlias = OrderedDict[PolygonId, Polygon]

# --- Predicates and validators ---

def is_vertex(x: object) -> bool:
    """Return True if ``x`` is a float64 array of shape (3,).

    Args:
        x: Object to test.

    Returns:
        True if ``x`` is a NumPy array with dtype float64 and shape (3,).
    """
    return (
        isinstance(x, np.ndarray)
        and x.dtype == np.float64
        and x.shape == (3,)
    )

def is_vertex_path(x: object) -> bool:
    """Return True if ``x`` is a float64 array of shape (n, 3) with n >= 3.

    A valid VertexPath is an ordered list of vertices defining a polygon boundary,
    with no repeated start/end vertex.

    Args:
        x: Object to test.

    Returns:
        True if ``x`` is a NumPy array with dtype float64, 2D, shape (n, 3), n >= 3.
    """
    return (
        isinstance(x, np.ndarray)
        and x.dtype == np.float64
        and x.ndim == 2
        and x.shape[1] == 3
        and x.shape[0] >= 3
    )

def check_vertex(x: object, *, name: str = 'vertex') -> None:
    """Validate that ``x`` is a float64 array of shape (3,).

    Args:
        x: Value to validate.
        name: Variable name used in error messages.

    Raises:
        TypeError: If ``x`` is not a NumPy ndarray.
        ValueError: If ``x`` does not have dtype float64 or shape (3,).
    """
    if not isinstance(x, np.ndarray):
        raise TypeError(f"{name} must be a NumPy ndarray, got {type(x).__name__}")
    if x.dtype != np.float64:
        raise ValueError(f"{name} must have dtype float64, got {x.dtype}")
    if x.shape != (3,):
        raise ValueError(f"{name} must have shape (3,), got {x.shape}")

def check_vertex_path(x: object, *, name: str = 'vertex_path') -> None:
    """Validate that ``x`` is a float64 array of shape (n, 3) with n >= 3.

    Args:
        x: Value to validate.
        name: Variable name used in error messages.

    Raises:
        TypeError: If ``x`` is not a NumPy ndarray.
        ValueError: If ``x`` does not have dtype float64, is not 2D, does not have 3 columns,
            or has fewer than 3 rows.
    """
    if not isinstance(x, np.ndarray):
        raise TypeError(f"{name} must be a NumPy ndarray, got {type(x).__name__}")
    if x.dtype != np.float64:
        raise ValueError(f"{name} must have dtype float64, got {x.dtype}")
    if x.ndim != 2:
        raise ValueError(f"{name} must be 2D with shape (n, 3), got ndim={x.ndim}")
    if x.shape[1] != 3:
        raise ValueError(f"{name} must have 3 columns (x,y,z), got shape {x.shape}")
    if x.shape[0] < 3:
        raise ValueError(f"{name} must have at least 3 rows (n>=3), got shape {x.shape}")

# --- Converters (convenience) ---

def as_vertex(x: object, *, name: str = 'vertex') -> Vertex:
    """Convert ``x`` to a float64 (3,) array and validate.

    This is a small convenience to accept array-likes while enforcing the
    canonical dtype/shape.

    Args:
        x: Array-like, ideally shape (3,).
        name: Variable name used in error messages.

    Returns:
        A NumPy float64 array of shape (3,).

    Raises:
        TypeError: If ``x`` cannot be coerced to an ndarray.
        ValueError: If the resulting array has the wrong dtype or shape.
    """
    try:
        arr = np.asarray(x, dtype=np.float64)
    except Exception as exc:  # pragma: no cover - defensive
        raise TypeError(f"{name} could not be converted to np.ndarray: {exc}") from exc
    check_vertex(arr, name=name)
    return arr

def as_vertex_path(x: object, *, name: str = 'vertex_path') -> VertexPath:
    """Convert ``x`` to a float64 (n, 3) array and validate.

    This accepts any array-like input and enforces the canonical dtype/shape,
    ensuring n >= 3 and no assumption about repeated start/end vertices.

    Args:
        x: Array-like, ideally shape (n, 3).
        name: Variable name used in error messages.

    Returns:
        A NumPy float64 array of shape (n, 3) with n >= 3.

    Raises:
        TypeError: If ``x`` cannot be coerced to an ndarray.
        ValueError: If the resulting array has the wrong dtype or shape.
    """
    try:
        arr = np.asarray(x, dtype=np.float64)
    except Exception as exc:  # pragma: no cover - defensive
        raise TypeError(f"{name} could not be converted to np.ndarray: {exc}") from exc
    check_vertex_path(arr, name=name)
    return arr
