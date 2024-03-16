"""
Unit testing
"""
# standard imports
import os
from unittest.mock import patch
import sys
import pytest
from sympy import Matrix


# local importi
from calc import create_matrix, add_subtract_matrix, dot_product_matrix

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# passing the mocked input in the decorator itself to define second matrix
@pytest.mark.parametrize("test_input,expected",
                         [(["1","2","2","3","3","4","3","2","1","2","2","3","3","4"],
                           [Matrix([[1,2], [2,3], [3,4]]), Matrix([[1,2], [2,3], [3,4]])])])
def test_create_matrix(test_input, expected):
    """
    Unit testing creating_matrix
    """
    with patch("builtins.input", side_effect=test_input):
        assert create_matrix(2, 3, 2) == expected

@pytest.mark.parametrize("test_input,expected",
                         [(["1","3","4","2","2","2","1","4","5","2","2","0","1"],
                           Matrix([[17,11],[13,19]]))])
def test_dot_product_matrix(test_input,expected):
    """
    Unit testing of dot_product_matrix
    """
    with patch("builtins.input", side_effect=test_input):
        matrix = create_matrix(2,2,2)
        assert dot_product_matrix(matrix) == expected

@pytest.mark.parametrize("test_input,expected",
                         [(["1","2","3","4","5","6","2","3","1","2","3",
                            "4","5","6","2","0","1","A"],
                                                  (Matrix([[2,4,6],[8,10,12]]),
                                                   [Matrix([[1,2,3],[4,5,6]]), "+",
                                                    Matrix([[1,2,3],[4,5,6]])]))])
def test_add_subtract_matrix(test_input,expected):
    """
    Unit testing of add subtract matrix
    """
    with patch("builtins.input", side_effect=test_input):
        matrix = create_matrix(2,2,3)
        assert add_subtract_matrix(matrix) == expected
