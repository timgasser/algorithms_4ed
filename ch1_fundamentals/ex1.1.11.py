# 1.1.11 Write a code fragment that prints the contents of a two-dimensional 
# boolean array, using * to represent true and a space to represent false. 
# Include row and column numbers.

def bool_array_print(bools, true_char='*', false_char=' '):
    '''
    Prints out array of bools using true and false characters
    INPUT: 2-d list of bools, optional true and false characters    
    RETURNS: String of resulting value to print and for unit testing
    '''
    # Early out if the variables aren't sane
    if type(bools) is not list:
        return None
    
    row_idx = 0
    return_str = ''
    
    try:
        # Use first row to get column width
        return_str += 'x '
        for i, ival in enumerate(bools[0]):
            return_str += str(i) + ' '
        return_str += '\n'
        
        for i, ival in enumerate(bools):
            
            return_str += str(i) + ' '
            
            for j, jval in enumerate(bools[i]):
                # print(i,j)
                if jval == True:
                    return_str += true_char + ' '
                else:
                    return_str += false_char + ' '
            
            return_str += '\n'
    except Exception as e:
        return e
        
    return return_str
        


if __name__ == '__main__':
    
    # Create some test matrices to print out
    test_bools_2x2 = [ [True, False], [False, True]]
    test_bools_3x3 = [ [True , False, True ], 
                       [False, True , False], 
                       [True , False, True ]]
    test_bools_4x4 = [ [True , False, True , False], 
                       [False, True , False, True ], 
                       [True , False, True , False],
                       [False, True , False, True ]]

    print(bool_array_print(test_bools_2x2))
    print(bool_array_print(test_bools_3x3))
    print(bool_array_print(test_bools_4x4))

