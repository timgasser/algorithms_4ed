# 1.1.3 Write a program that takes three integer command-line arguments and 
# prints equal if all three are equal, and not equal otherwise.

# Needed to get command line arguments
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
    
    return check_and_compare_opts(options)

def check_and_compare_opts(options):
    '''
    Checks options are integers, and compares them if so.
    INPUT: List of options
    RETURNS: None if options aren't 3 integers, 
             False/True otherwise depending on comparison
    '''
    
    int_options = convert_args(options)

    if int_options is None or len(int_options) != 3:
        print('Error - need 3 integer arguments, got {}'.format(options))
        return -1
    
    if check_equal(int_options):
        print('equal')
        return 0
    else:
        print('not equal')
        return 0

def list_contains_ints(vals):
    '''
    Checks if all elements in a list contains ints
    INPUT: list of arbitrary lengths
    RETURNS: bool showing whether all values are ints
    '''
    for val in vals:
        if type(val) is not int:
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
        # print('Error converting {} to integer'.format(args))
        return None
    
    return arg_ints

def check_equal(vals):
    '''
    Checks if all the values are equal (assumes list of ints)
    INPUT: List of integer values
    RETURNS: Boolean when all values are equal
    '''
    first_val = vals[0]
    
    for val in vals:
        if first_val != val:
            return False
        
    return True

if __name__ == '__main__':
    sys.exit(main())
    