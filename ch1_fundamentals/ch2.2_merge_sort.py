import sys
import random

def main(argv=None):
    """Main entry point"""
    
    if argv is None:
        argv = sys.argv
    
    print(merge_sort([6,3,5,8,2,6,2,5,8,0,5,3,2]))
    # batch_test((selection_sort, insertion_sort), n=100, runs=10)
    
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


def merge_sort(array):
    final_array = sort(array)
    return final_array

def sort(array, verbose=False):
    #If we're down to one element it's already sorted.
    if len(array) == 1:
        return array
        
    mid = int(len(array) / 2)
    print('mid = {}, left = {}, right = {}'.format(mid, array[:mid], array[mid:]))
    
    lista = sort(array[:mid])
    listb = sort(array[mid:])
    result = merge(lista, listb, verbose=True)
    return result

def merge(lista, listb, verbose=False):
    """Merges two lists together"""
    ptra = 0
    ptrb = 0
    
    if verbose: print('\na = {}, b = {}'.format(lista, listb))
    output = list()
    while ptra < len(lista) or ptrb < len(listb):
        if ptra == len(lista):
            output.extend(listb[ptrb:])  
            ptrb = len(listb)
        elif ptrb == len(listb):
            output.extend(lista[ptra:])  
            ptra = len(lista)
        elif lista[ptra] <= listb[ptrb]:
            output.append(lista[ptra])
            ptra += 1
        elif lista[ptra] > listb[ptrb]:
            output.append(listb[ptrb])
            ptrb += 1
        
        if verbose: print('ptra = {}, lista = {}, ptrb = {}, listb = {}, output = {}'.format(ptra, lista, ptrb, listb, output))
    
    if verbose: print('output = {}'.format(output))
    return output
        
    
    
            
if __name__ == "__main__":
    
    sys.exit(main(sys.argv))