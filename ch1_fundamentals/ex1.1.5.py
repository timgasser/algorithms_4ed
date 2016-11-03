# Ex 1.1.5:  Write a code fragment that prints true if the double variables 
# x and y are both strictly between 0 and 1 and false otherwise.

def between_zero_and_one(x,y):
    '''
    Prints 'true' if x and y are between 0 and 1, 'false' otherwise
    INPUT: floats x, y
    RETURNS: 'true' or 'false' (for unit testing)
    '''
    if not (type(x) is float and type(y) is float):
        return ArithmeticError
    
    try:
        if (x > 0.0 and x < 1.0) and (y > 0.0 and y < 1.0):
            print('true')
            return True
        else:
            print('false')
            return False
    except Exception as e:
        print('Exception - {}')
        return e
        
if __name__ == '__main__':
    assert between_zero_and_one(0.0, 1.0) == False
    assert between_zero_and_one(0.1, 1.0) == False
    assert between_zero_and_one(0.0, 0.9) == False
    assert between_zero_and_one(0.1, 0.9) == True
    assert between_zero_and_one(0.5, 0.5) == True

    assert between_zero_and_one(0.0, 'a') is ArithmeticError
    assert between_zero_and_one('b', 0.0) is ArithmeticError    
    assert between_zero_and_one('a', 'b') is ArithmeticError    

    print('All tests passed')