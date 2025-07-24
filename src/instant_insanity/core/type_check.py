import numpy as np

def _check_array(x, name, ndim, components):
    """Validate that x is a NumPy array with specified shape and dtype float64.

    Args:
        x (Any): The object to check.
        name (str): Name of the variable (used in error messages).
        ndim (int): Expected number of dimensions.
        components (int): Expected size of the last dimension.

    Raises:
        TypeError: If x is not a NumPy array or does not have dtype float64.
        ValueError: If x does not have the expected number of dimensions
            or the last dimension is not equal to `components`.
    """
    if not isinstance(x, np.ndarray):
        raise TypeError(f"{name} must be a NumPy array.")
    if x.dtype != np.float64:
        raise TypeError(f"{name} must have dtype float64.")
    if x.ndim != ndim:
        raise ValueError(f"{name} must be {ndim}-dimensional.")
    if x.shape[-1] != components:
        raise ValueError(f"{name} must have {components} components in the last dimension.")

def check_vector3_float64(v):
    """Validate that v is a 1D NumPy array of 3 float64 elements.

    Args:
        v (np.ndarray): Input array to validate.

    Raises:
        TypeError: If v is not a NumPy array or has incorrect dtype.
        ValueError: If v is not 1-dimensional or does not contain exactly 3 elements.
    """
    _check_array(v, "v", ndim=1, components=3)

def check_matrix_nx3_float64(m):
    """Validate that m is a 2D NumPy array with shape (n, 3) and dtype float64.

    Args:
        m (np.ndarray): Input array to validate.

    Raises:
        TypeError: If m is not a NumPy array or has incorrect dtype.
        ValueError: If m is not 2-dimensional or does not have exactly 3 columns.
    """
    _check_array(m, "m", ndim=2, components=3)
