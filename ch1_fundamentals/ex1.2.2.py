# 1.2.1 Write a Point2D client that takes an integer value N from the 
# command line, generates N random points in the unit square, and computes 
# the distance separating the closest pair of points.

from math import hypot, atan2, fabs
from random import random
import sys

def main(argv=None):
    '''
    Function called to run main script including unit tests
    INPUT: List of arguments from the command line
    RETURNS: Exit code to be passed to sys.exit():
        -1: Invalid input
         0: Script completed successfully
    '''
    
    if argv is None:
        argv = sys.argv
    
    options = argv[1:]
    
    if (len(options) != 1):
        print('Error - expected single integer option, got {}'.format(options))
        return -1
        
    N = int(argv[1])
    line = sys.stdin.readline()
    line = line.split(' ')
    values = [float(word) for word in line]
    print('Read {}'.format(values))
    
    ptr = 0
    intervals = list()
    while ptr < len(values):
        intervals.append(Interval1D(values[ptr], values[ptr+1]))
        ptr += 2
    print('Read {}'.format(intervals))
   
    pair_count = 0
    aptr = 0
    bptr = 0
    
    while aptr < len(intervals):
        bptr = aptr + 1
        
        while bptr < len(intervals):
            # print('debug: a = {}, b = {}'.format(aptr, bptr))
            if intervals[aptr].intersects(intervals[bptr]):
                print('Incrementing pair_count, a = {}, b = {}'.format(intervals[aptr], intervals[bptr]))
                pair_count += 1
            bptr += 1

        aptr += 1
    
    print('Pair count is {}'.format(pair_count))
    
    return 0
    
class Interval1D:
    '''
    Class representing a 1D interval
    '''
    def __init__(self, left, right):
        '''
        Create a new Point2D using cartesian co-ordinates
        '''
        assert right > left, 'Error - right has to be greater than left'
        self.left = left
        self.right = right
    
    def __repr__(self):
        description = 'Interval1D: left = {}, right = {}'.format(self.left, self.right)
        return description
    
    def length(self):
        return self.right - self.left
    
    def contains(self, x):
        contained = (x <= self.right) and (x >= self.left)
        return contained

    def intersects(self, interval):
        inter = ((interval.left <= self.right) and (interval.left >= self.left) \
             or  (interval.right >= self.left) and (interval.right <= self.right))
        
        print('Checking intersect: self {} interval {}, result {}'.format(self, interval, inter))
        return inter  # Add this in later
        
def float_equal(a,b, epsilon = 1e-6):
    '''
    Checks for equality of two floats, using epsilon tolerance
    INPUT: floats: a, b
           float: epsilon tolerance limit
    RETURN: bool showing if the two floats are equal
    '''
    equal = fabs(a-b) < epsilon
    return equal

if __name__ == '__main__':
    
    # Unit tests    
    test_interval = Interval1D(1.5, 3.8)

    assert float_equal(test_interval.left, 1.5)
    assert float_equal(test_interval.right, 3.8)
    assert float_equal(test_interval.length(), 3.8 - 1.5)
    assert test_interval.contains(1.5)
    assert test_interval.contains(3.8)
    assert test_interval.contains(2.0)
    assert not test_interval.contains(1.0)
    assert not test_interval.contains(-1.0)
    assert not test_interval.contains(100.0)
    assert test_interval.intersects(Interval1D(2.0, 3.0))
    assert test_interval.intersects(Interval1D(2.0, 4.0))
    assert test_interval.intersects(Interval1D(1.0, 2.0))

    sys.exit(main())
    