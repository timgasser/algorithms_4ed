import sys
import random

def main(argv=None):
    """Main entry point"""
    
    if argv is None:
        argv = sys.argv
    
    # small_array = [4, 2, 3, 5, 1]
    # print(shell_sort(small_array, verbose=True))
    
    batch_test((selection_sort, insertion_sort), n=100, runs=10)
    
    return 0

def batch_test(algos, n, runs, max=None):
    
    if max is None:
        max = n * 10
    
    for algo in algos:
        for _ in range(runs):
            print('Checking algo {} with {} integers'.format(algo, n))
            arr = random.sample(range(1, max), n)
            assert sorted(arr) == algo(arr)
    return

def swap(array, x, y):
    temp = array[x]
    array[x] = array[y]
    array[y] = temp
    return array

def selection_sort(array):

    for i in range(len(array)):
        min_idx = i
        min_val = array[i]
        
        for j in range(i+1, len(array)):
            if array[j] < min_val:
                min_val = array[j]
                min_idx = j
        array = swap(array, i, min_idx)
    return array


def insertion_sort(array):

    for i in range(len(array)-1):
        j = i + 1 
        
        for j in range(i+1, 0, -1):
            if j == 0:
                array = swap(array, 0, 1)
            elif array[j] < array[j-1]:
                array = swap(array, j, j-1)
            else:
                continue
    
    return array

def shell_sort(array, verbose=False):

    # Need to compute the largest h value to run with first
    N = len(array)
    h = 1
    while h < N / 3.0:
        h = 3 * h + 1
    if verbose: print('H is {}'.format(h))
    
    # Now do insertion sort, jumping by h instead of 1
    while h >= 1:
        for i in range(1, N, h):
            if array[i] < array[i-1]:
                array = swap(array, i, i-1)
            
        h = h / 3
    return array     
    
    

            
if __name__ == "__main__":
    
    sys.exit(main(sys.argv))