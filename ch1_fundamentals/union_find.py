# Chapter 1.5: Union-Find

# Needed to get command line arguments
import sys 

import timeit

# Constants
DATA_DIR = 'data'
DEF_FILE = DATA_DIR + '/tinyUF.txt'

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
        # print('Creating Union Find with {} entries'.format(N))
        self.components = list()

    def __repr__(self):
        rep = 'Printing Union Find with {} components:\n'.format(len(self.components))
        for idx, comp in enumerate(self.components):
            rep += 'Component: {}\n'.format(comp)
        return rep

    def union(self, p, q):
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
        # print('Find of site {}'.format(p))

        for comp in self.components:
            if p in comp:
                print('Found! In {}'.format(comp))
                return comp
        
        # print('Not Found!')
        return None

    def connected(self, p, q):
        # print('Connected for sites {} and {}'.format(p, q))
        if self.find(p) == self.find(q):
            return True
        
        return False

    def count(self):
        # print('Count called')
        return len(self.components)


class BookUnionFind(UnionFind):
    ''' Superclass with common functionality of all Union Find algos in book'''
    def __init__(self, N):
        '''
        Initializes Union Find structure with N entries
        '''
        # The site number is implicitly stored as the self.id index
        print('Super init: N = {}'.format(N))
        self.N = N # Call this N to avoid namespace clash with count function
        self.id = list(range(N))
        
        print('Super init: N = {}, id = {}'.format(self.N, self.id))
        
    def union(self, p, q):
        '''
        Merge components if two sites are in different components 
          -> Implement this in subclass
        INPUT: Site identifiers p and q
        RETURNS: None
        '''
        raise NotImplementedError()
        
    def find(self, p):
        '''
        Component identifier for p
          -> Implement this in subclass
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
        print('Super connected for {} and {}'.format(p, q))
        return self.find(p) == self.find(q)

    def count(self):
        '''
        Returns number of components (not sites)
        INPUT: 
        RETURNS: Integer with number of components
        '''
        print('Super count returning {}'.format(self.N))
        return self.N
        
    @classmethod
    def create_from_file(cls, filename=None):
        if filename is None:
            filename = DEF_FILE
        
        line_count = 0
        with open(filename, 'r') as f:
            for line in f:
                line_count += 1
                
                # Create new Union-Find using N on first line of file
                if line_count == 1:
                    N = int(line)
                    print('Read init line to create {} sites'.format(N))
                    new_class = cls(N)
                else:
                    # Read in the line, strip space and convert to integer 
                    print('Read Line #{} with sites: {}'.format(line_count, line))
                    sites = line.split(' ')
                    sites = [int(site.strip()) for site in sites]
                    p, q = sites
                    print('Sites {} and {} connected? {}'.format(p, q, new_class.connected(p, q)))
                    # if not new_class.connected(p, q):
                    #     new_class.union(p, q)

        print('File {}\nUnion-Find:\n{}'.format(filename, new_class))
        return new_class

class QuickFindUnionFind(BookUnionFind):
    ''' Quick Find invariant:
    `p` and `q` are connected iff id[p] == id[q].
    All sites in the same component must have the same value in the id list
    When creating union, change all values in id[p] to id[q]
    '''
    def __init__(self, filename=None):
        '''
        Initializes Union Find structure from file
        '''
        if filename is None:
            filename = DEF_FILE
        
        line_count = 0
        with open(filename, 'r') as f:
            for line in f:
                line_count += 1
                
                # Create new Union-Find using N on first line of file
                if line_count == 1:
                    self.N = int(line)
                    self.id = list(range(self.N))
                    print('Read init line to create {} sites'.format(self.N))
                else:
                    # Read in the line, strip space and convert to integer 
                    print('Read Line #{} with sites: {}'.format(line_count, line))
                    sites = line.split(' ')
                    sites = [int(site.strip()) for site in sites]
                    p, q = sites
                    if not self.connected(p, q):
                        self.union(p, q)

    def union(self, p, q):
        '''
        Merge components if two sites are in different components 
        INPUT: Site identifiers p and q
        RETURNS: None
        '''
        print('Union of sites {} and {}'.format(p, q))
        self.id = [self.id[q] if val == self.id[p] else val for idx, val in enumerate(self.id)]
        print('self.id: {}'.format(self.id))
        
    def find(self, p):
        '''
        Component identifier for p
          -> Implement this in subclass
        INPUT: Site p
        RETURNS: Component ID
        '''
        print('Find of site {} = {}'.format(p, self.id[p]))
        # print(self.id)
        return self.id[p]
        
    def connected(self, p, q):
        '''
        Returns True if p and q are in the same component
        INPUT: Nodes p and q
        RETURNS: Boolean showing if the nodes are connected
        '''
        print('Super connected for {} and {}'.format(p, q))
        return self.find(p) == self.find(q)

    def count(self):
        '''
        Returns number of components (not sites)
        INPUT: 
        RETURNS: Integer with number of components
        '''
        print('Super count returning {}'.format(self.N))
        return self.N
        
    
def test_quickfind():
    quick_find = QuickFindUnionFind()
    assert quick_find.id == [1,1,1,8,8,1,1,1,8,8]

def test_naive_union_find(filename=None):
    
    if filename is None:
        filename = DEF_FILE
    
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
    # print(timeit.repeat(test_naive_union_find, number=1000))

    test_quickfind()
    
    return 0
        
if __name__ == '__main__':
    sys.exit(main())
    
        
    
        
        