# 1.1.13 Write a code fragment to print the transposition 
# (rows and columns changed) of a two-dimensional array with 
# M rows and N columns

def transpose(matrix):
    '''
    Transposes a 2-d array of lists 
    INPUT: 2-d list of any values
    RETURNS: Transposed 2-d list of values
    '''
    
    num_rows = len(matrix)
    num_cols = len(matrix[0])
    
    output_matrix = list()
    
    for j in range(num_cols):
        new_row = list()
        
        for i in range(num_rows):
            new_row.append(matrix[i][j])
        
        output_matrix.append(new_row)
    
    return output_matrix


if __name__ == '__main__':
    
    # Create some test matrices to print out
    test_matrix_2x2 = [ [1, 2], [3, 4]]
    test_matrix_3x3 = [ [1, 2, 3 ], 
                        [4, 5 ,6], 
                        [7, 8, 9 ]]
    test_matrix_4x4 = [ [1 , 2, 3 , 4], 
                        [5, 6 , 7, 8 ], 
                        [9 , 10, 11, 12],
                        [13, 14, 15, 16 ]]

    print(transpose(test_matrix_2x2))
    print(transpose(test_matrix_3x3))
    print(transpose(test_matrix_4x4))

