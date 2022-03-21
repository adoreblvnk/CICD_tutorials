# test_mathEx.py


import os
import sys

# add math package to path from back-folder
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'math'))

import numpy as np
import pytest

from mathEx import stat2Num, div2Num
from mathCy import stat2NumCy

@pytest.mark.pyfile
def test_stat2Num():
    """ Test method for stat2Num """

    assert stat2Num(3, 2) == (5, 2.5)
    assert stat2Num(3, 2.0) == (5, 2.5)
    assert stat2Num(3.5, 2.5) == (6, 3)
    assert stat2Num(3.5, 2.5) == (6.0, 3.0)

@pytest.mark.pyfile
class Test_stat2Num(object):
    """ Test class for stat2Num """

    def test_stat2Num_inputInt(self):
        """ Test with integer inputs """
        assert stat2Num(3, 2) == (5, 2.5)
        assert stat2Num(3, 2) == (5.0, 2.5)

    def test_stat2Num_inputFloat(self):
        """ Test with float inputs """
        assert stat2Num(3, 2) == (5, 2.5)
        assert stat2Num(3, 2) == (5.0, 2.5)

@pytest.mark.cyfile
class Test_stat2NumCy(object):
    """ Test class for stat2NumCy """

    def test_stat2Num_inputInt(self):
        """ Test with integer inputs """
        assert stat2NumCy(3, 2) == (5, 2.5)
        assert stat2NumCy(3, 2) == (5.0, 2.5)

    def test_stat2Num_inputFloat(self):
        """ Test with float inputs """
        assert stat2NumCy(3, 2) == (5, 2.5)
        assert stat2NumCy(3, 2) == (5.0, 2.5)


@pytest.mark.parametrize("x, y", [(3,2), (3, 2.0), (3.5, 2.5)])
def test_stat2Num(x, y):
    """ Parameterized test method for stat2Num """

    assert stat2Num(x, y) == (x+y, (x+y)/2)


@pytest.mark.numpyfile
class Test_numpy(object):
    """ check approximate-equalilty conditions using numpy.testing """

    def test_div2Num_pytest(self):
        # 0.66667 != 0.6666666666666666
        assert div2Num(2, 3) != 0.66667

    def test_dif2Num_numpy_4places(self):
        #  2/3 = 0.6666666666666666 = 0.66667 i.e. equal upto 4 places
        np.testing.assert_approx_equal(div2Num(2, 3), 0.66667, 4)

    def test_dif2Num_numpy_5places(self):
        # 2/3 = 0.6666666666666666 = 0.66667 i.e. equal upto 5 places
        # note that it is round off for last value i.e.
        # 0.6666666666666666 is changed to 0.66667 before comparision
        np.testing.assert_approx_equal(div2Num(2, 3), 0.66667, 5)

    def test_dif2Num_numpy_6places(self):
        # failed because
        # 2/3 = 0.6666666666666666 = 0.666667 != 0.666668 upto 6 places
        np.testing.assert_approx_equal(div2Num(2, 3), 0.666668, 6)