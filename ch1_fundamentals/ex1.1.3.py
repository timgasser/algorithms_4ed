# 1.1.3 Write a program that takes three integer command-line arguments and 
# prints equal if all three are equal, and not equal otherwise.

# Needed to get command line arguments
import sys 

def check_args(args):
    ''' 
    Checks the arguments passed into program
    INPUT: List of arguments
    RETURNS: Boolean showing if arguments are good
    '''
    if (len(args) != 3):
        return False

    return True

def convert_args(args):
    '''
    Convert all entries in list to integer
    INPUT: List of arguments
    RETURN: List of integers (if they can be converted)
    '''
    try:
        arg_ints = [int(arg) for arg in args]
    except:
        print('Error converting {} to integer'.format(args))
        return [None]
        
    return arg_ints


def check_equal(vals):
    '''
    Checks if all the values are equal
    INPUT: List of integer values
    RETURNS: Boolean when all values are equal
    '''
    
    int_vals = convert_args(vals)
    
    first_val = int_vals[0]
    if first_val is None:
        return False
    
    for val in int_vals:
        if first_val != val:
            return False
            
    return True

if __name__ == '__main__':
    args = sys.argv[1:]
    
    if not check_args(args):
        print('Error - need 3 integer arguments, got {}'.format(args))
    
    else:
        if check_equal(args):
            print('equal')
        else:
            print('not equal')
    
    