"""This file defines some useful functions for performing calculations
with Matrices.
"""

import vmath
from matrix import Matrix, DimensionError
from vector import Vector


def transpose(A):
    """Calculates the transpose of Matrix A.
    """
    return Matrix(A.columns)


def trace(A):
    """Calculates the sum of the leading diagonal of Matrix A.
    """
    return sum(A[i][i] for i in range(min(A.dim)))


def augment(A, B):
    """Augments Matrix A with Matrix or Vector B.
    """
    if isinstance(B, Vector):
        return Matrix(*A.columns, B, columns=True)
    else:
        return Matrix(*A.columns, *B.columns, columns=True)


def deaugment(A, n):
    """Splits the last n columns off of A. Returns the resulting Matrices or
    Matrix and Vector if n is 1.
    """
    if n == 1:
        return Matrix(A.columns[:-1], columns=True), A.columns[-1]
    return Matrix(A.columns[:-n], columns=True), Matrix(A.columns[-n:], columns=True)


def factorize(A):
    """Performs QR factorization on invertible Matrix A. Returns (Q, R).
    """
    if A.dim.rows != A.dim.columns:
        raise DimensionError("Matrix A must be square.")

    # Use Gram-Schidt to calculate orthogonal Matrix Q from columns of A
    Q = Matrix(vmath.gs(A.columns), columns=True)

    # If A is not invertible, vmath.gs will not return a square matrix
    if A.dim != Q.dim:
        raise DimensionError("Matrix A must be invertible.")

    # Upper triangular Matrix R = (Q^T)A
    R = transpose(Q) * A

    return Q, R


def row_swap(A, row1, row2):
    """Swaps row1 with row2 and returns a new Matrix.
    """
    rows = list(A.rows)
    rows[row1], rows[row2] = rows[row2], rows[row1]
    return Matrix(rows)


def row_add(A, row1, row2):
    """Adds row1 to row2 and returns a new Matrix.
    """
    rows = list(A.rows)
    rows[row2] = rows[row1] + rows[row2]
    return Matrix(rows)


def row_multiply(A, row, k):
    """Multiplies row by scalar k and returns a new Matrix.
    """
    rows = list(A.rows)
    rows[row] = k * rows[row]
    return Matrix(rows)
