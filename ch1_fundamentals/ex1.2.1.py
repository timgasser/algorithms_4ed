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
    
    points = [UnitRandomPoint2D() for _ in range(N)]
    # print(*points, sep='\n')
    
    min_dist = sys.float_info.max # Infinity ?!
    
    for a_idx, a_val in enumerate(points):
        for b_idx, b_val in enumerate(points):
            
            if a_idx == b_idx:
                continue
            
            distance = a_val.distance_to(b_val)
            if distance < min_dist:
                min_dist = distance
    
    print('Minimum distance is {}'.format(min_dist))
    return 0

class Point2D:
    '''
    Class representing a 2D point
    '''
    def __init__(self, x, y):
        '''
        Create a new Point2D using cartesian co-ordinates
        '''
        self.x = x
        self.y = y
    
    def __repr__(self):
        description = 'Point2D: x = {}, y = {}'.format(self.x, self.y)
        return description
    
    def r(self):
        mag = hypot(self.x, self.y)
        return mag
        
    def theta(self):
        angle = atan2(self.y, self.x)
        return angle
        
    def distance_to(self, point):
        dx = self.x - point.x
        dy = self.y - point.y
        return hypot(dx, dy)

class UnitRandomPoint2D(Point2D):
    '''
    Subclass of Point2D, creates random Point2D
    '''
    def __init__(self):
        self.x = random()
        self.y = random()

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
    test_point = Point2D(1, 2)
    print(test_point)
    
    assert test_point.x == 1
    assert test_point.y == 2
    assert float_equal(test_point.r(), 2.2360679774997896964091736687313)
    assert float_equal(test_point.theta(), 1.1071487177940905030170654601785)
    
    random_point = UnitRandomPoint2D()
    print(random_point)
    
    assert random_point.x >= 0.0 and random_point.x <= 1.0
    assert random_point.y >= 0.0 and random_point.y <= 1.0

    sys.exit(main())
    