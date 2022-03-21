# mathCy.pyx

import pyximport
pyximport.install()

cpdef (double, double) stat2NumCy(double x, double y):
    """ Sum and mean value of two numbers

    Parameters
    ----------
    x : double
        first number to be added

    y : double
        second number two be added

    Returns
    -------
    x+y: double
        sum of two numbers
    (x+y)/2 : double
        mean of two numbers
    """
    return(x+y, (x+y)/2)