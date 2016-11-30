# Chapter 1.5: Union-Find

# Needed to get command line arguments
import sys 

import timeit

# Constants
DATA_DIR = 'data'


class UnionFind(object):
    ''' Abstract type for Union Find applications '''
    def __init__(self, N):
        '''
        Initializes Union Find structure with N entries
        '''
        raise NotImplementedError()
        
    def union(self, p, q):
        '''
        Merge components if two sites are in different components
        INPUT: Site identifiers p and q
        RETURNS: None
        '''
        raise NotImplementedError()
        
    def find(self, p):
        '''
        Component identifier for p
        INPUT: Site p
        RETURNS: Component ID
        '''
        raise NotImplementedError()
    
    def connected(self, p, q):
        '''
        Returns True if p and q are in the same component
        INPUT: Nodes p and q
        RETURNS: Boolean showing if the nodes are connected
        '''
        raise NotImplementedError()

    def count(self):
        '''
        Returns number of components (not sites)
        INPUT: 
        RETURNS: Integer with number of components
        '''
        raise NotImplementedError()
        
class NaiveUnionFind(UnionFind):
    '''
    My first stab at this, without checking the book implementations.
    Uses a 2-level list structure for components -> sites
    '''
    def __init__(self, N):
        ''' Pseudocode
        - Create a list of N sets, all initially empty
        '''
        # print('Creating Union Find with {} entries'.format(N))
        self.components = list()

    def __repr__(self):
        rep = 'Printing Union Find with {} components:\n'.format(len(self.components))
        for idx, comp in enumerate(self.components):
            rep += 'Component: {}\n'.format(comp)
            # for site in comp:
            #     rep += ' -> {}\n'.format(site)
        return rep

    def union(self, p, q):
        ''' Pseudocode
        - Find component `a` containing site `p`, and `b` with site `q`
        - If a == b then early out
        - Combine component b to component a (set union)
        - Remove component b from the list of components
        '''
        # print('Union of sites {} and {}'.format(p, q))
        comp_p = self.find(p)
        comp_q = self.find(q)
        
        if comp_p is not None:
            comp_p_idx = self.components.index(comp_p)
        
        if comp_q is not None:
            comp_q_idx = self.components.index(comp_q)

        if comp_p is None and comp_q is None:
            # print('Creating new component for sites {}, {}'.format(p, q))
            self.components.append([p, q])
            return
            
        if comp_p is None: # comp_q is not None, add p to q's component
            self.components[comp_q_idx].append(p)
            # print('Adding {} to {}\'s component -> {}'.format(p, q, self.components[comp_q_idx]))
            return
        
        if comp_q is None: # comp_p is not None, add q to p's component
            self.components[comp_p_idx].append(q)
            # print('Adding {} to {}\'s component -> {}'.format(q, p, self.components[comp_p_idx]))
            return

        if comp_p == comp_q:
            # print('Skipping - {} and {} already in same component {}'.format(p, q, comp_p))
            return
        
        # Collapse the two components into one (p for consistency)
        # print('Combining {} and {}'.format(self.components[comp_p_idx], self.components[comp_q_idx]))
        self.components[comp_p_idx].extend(self.components[comp_q_idx])
        del self.components[comp_q_idx]
        return

    def find(self, p):
        ''' Pseudocode
        - For each component in component list:
          - If component set contains p, return component
          
        - Return error (site not found)
        '''
        # print('Find of site {}'.format(p))

        for comp in self.components:
            if p in comp:
                print('Found! In {}'.format(comp))
                return comp
        
        # print('Not Found!')
        return None

    def connected(self, p, q):
        ''' Pseudocode
        - If find (p) == find(q)
            - return True
        return False
        '''
        # print('Connected for sites {} and {}'.format(p, q))
        if self.find(p) == self.find(q):
            return True
        
        return False

    def count(self):
        ''' Pseudocode
        return length of Component list
        ''' 
        # print('Count called')
        return len(self.components)


def test_naive_union_find(filename=None):
    
    if filename is None:
        filename = DATA_DIR + '/tinyUF.txt'
    
    
    line_count = 0
    with open(filename, 'r') as f:
        for line in f:
            line_count += 1
            
            # Create new Union-Find using N on first line of file
            if line_count == 1:
                N = int(line)
                print('Read init line to create {} sites'.format(N))
                union_find = NaiveUnionFind(N)
            else:
                # Read in the line, strip space and convert to integer 
                print('Read Line #{} with sites: {}'.format(line_count, line))
                sites = line.split(' ')
                sites = [int(site.strip()) for site in sites]
                union_find.union(sites[0], sites[1])
                print(union_find)

    print(union_find)
    
def main(argv=None):
    '''
    Function called to run main script including unit tests
    INPUT: List of arguments from the command line
    RETURNS: Exit code to be passed to sys.exit():
        -1: Invalid input
         0: Script completed successfully
    '''
    print(timeit.repeat(test_naive_union_find, number=1000))

    return 0
        
if __name__ == '__main__':
    sys.exit(main())
    
        
    
        
        