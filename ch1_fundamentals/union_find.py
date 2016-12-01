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
                    # print('Read init line to create {} sites'.format(self.N))
                else:
                    # Read in the line, strip space and convert to integer 
                    # print('Read Line #{} with sites: {}'.format(line_count, line))
                    sites = line.split(' ')
                    sites = [int(site.strip()) for site in sites]
                    p, q = sites
                    if not self.connected(p, q):
                        self.union(p, q)

    def __repr__(self):
        return '{}'.format(self.id)

    def union(self, p, q):
        '''
        Merge components if two sites are in different components 
        INPUT: Site identifiers p and q
        RETURNS: None
        '''
        # print('Union of sites {} and {}'.format(p, q))
        p_comp = self.id[p] # 1 array access
        q_comp = self.id[q] # 1 array access
        # list comprehension does min: N + 1, max: N + N - 1 = 2N-1
        self.id = [q_comp if val == p_comp else val for val in self.id]
        # print('self.id: {}'.format(self.id))
        
    def find(self, p):
        '''
        Component identifier for p
          -> Implement this in subclass
        INPUT: Site p
        RETURNS: Component ID
        '''
        # print('Find of site {} = {}'.format(p, self.id[p]))
        # print(self.id)
        return self.id[p] # 1 array access
        
    def connected(self, p, q):
        '''
        Returns True if p and q are in the same component
        INPUT: Nodes p and q
        RETURNS: Boolean showing if the nodes are connected
        '''
        # print('Super connected for {} and {}'.format(p, q))
        return self.find(p) == self.find(q) # 2 array accesses

    def count(self):
        '''
        Returns number of components (not sites)
        INPUT: 
        RETURNS: Integer with number of components
        '''
        # print('Super count returning {}'.format(self.N))
        return self.N

class QuickUnionUnionFind(BookUnionFind):
    ''' Quick Union invariant:
    Maintains invariant that components share the same root site
    id[] array entry is a link to another site in same component
    - Can link to itself, in which case it's a root
    When creating union, add link from id[p] to id[q]
    '''
    def __init__(self, filename=None):
        '''
        Initializes structure from file
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

    def __repr__(self):
        return '{}'.format(self.id)
    
    def find_root(self, p):
        ''' Helper function to follow links until root site found.
        Note by definition a root is an entry in the id list whose val == idx
        INPUT: Site identifier p
        RETURNS: Root site 
        '''
        print('Finding Root for site idx {}, ids = {}'.format(p, self.id))
        p_idx = p
        while self.id[p_idx] != p_idx:
            print(' * {} -> {}'.format(p_idx, self.id[p_idx]))
            p_idx = self.id[p_idx]
        
        print('Found Root site: {} for {}'.format(p_idx, p))
        return p_idx

    def union(self, p, q):
        '''
        Merge components if two sites are in different components 
        INPUT: Site identifiers p and q
        RETURNS: None
        '''
        print('Union of sites {} and {}'.format(p, q))

        p_root = self.find_root(p)
        q_root = self.find_root(q)

        print('Union pre  self.id: {}'.format(self.id))
        self.id[p_root] = q_root
        print('Union post self.id: {}'.format(self.id))
        
    def find(self, p):
        '''
        Component identifier for p
          -> Implement this in subclass
        INPUT: Site p
        RETURNS: Component ID
        '''
        print('Find of site {} = {}'.format(p, self.id[p]))
        print(self.id)
        
        p_root = self.find_root(p)
        print('Found root of {} at {}'.format(p, p_root))
        return p_root
        
    def connected(self, p, q):
        '''
        Returns True if p and q are in the same component
        INPUT: Nodes p and q
        RETURNS: Boolean showing if the nodes are connected
        '''
        # print('Super connected for {} and {}'.format(p, q))
        return self.find(p) == self.find(q) # 2 array accesses

    def count(self):
        '''
        Returns number of components (not sites)
        INPUT: 
        RETURNS: Integer with number of components
        '''
        # print('Super count returning {}'.format(self.N))
        return self.N

class WeightedQuickUnionUnionFind(BookUnionFind):
    ''' Weighted Quick Union invariant:
    Maintains invariant that components share the same root site
    id[] array entry is a link to another site in same component
    sz[] array tracks size of root nodes
    - Can link to itself, in which case it's a root
    When creating union, always update site to point from smallest to largest tree
    '''
    def __init__(self, filename=None):
        '''
        Initializes structure from file
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
                    self.sz = [1 for _ in range(self.N)]
                    print('Read init line to create {} sites'.format(self.N))
                else:
                    # Read in the line, strip space and convert to integer 
                    print('Read Line #{} with sites: {}'.format(line_count, line))
                    sites = line.split(' ')
                    sites = [int(site.strip()) for site in sites]
                    p, q = sites
                    if not self.connected(p, q):
                        self.union(p, q)

    def __repr__(self):
        return '{}'.format(self.id)
    
    def find_root(self, p):
        ''' Helper function to follow links until root site found.
        Note by definition a root is an entry in the id list whose val == idx
        INPUT: Site identifier p
        RETURNS: Root site 
        '''
        print('Finding Root for site idx {}, ids = {}'.format(p, self.id))
        p_idx = p
        while self.id[p_idx] != p_idx:
            print(' * {} -> {}'.format(p_idx, self.id[p_idx]))
            p_idx = self.id[p_idx]
        
        print('Found Root site: {} for {}'.format(p_idx, p))
        return p_idx

    def union(self, p, q):
        '''
        Merge components if two sites are in different components 
        INPUT: Site identifiers p and q
        RETURNS: None
        '''
        print('Union of sites {} and {}'.format(p, q))

        p_root = self.find_root(p)
        q_root = self.find_root(q)

        print('Union pre  self.id: {}'.format(self.id))
        # This is where the magic weighting happens
        # self.id[p_root] = q_root<- standard quick-union
        if self.sz[p_root] < self.sz[p_root]:
            self.id[p_root] = q_root
            self.sz[p_root] += self.sz[q_root]
        else:
            self.id[q_root] = p_root
            self.sz[q_root] += self.sz[p_root]
            
        print('Union post self.id: {}'.format(self.id))
        
    def find(self, p):
        '''
        Component identifier for p
          -> Implement this in subclass
        INPUT: Site p
        RETURNS: Component ID
        '''
        print('Find of site {} = {}'.format(p, self.id[p]))
        print(self.id)
        
        p_root = self.find_root(p)
        print('Found root of {} at {}'.format(p, p_root))
        return p_root
        
    def connected(self, p, q):
        '''
        Returns True if p and q are in the same component
        INPUT: Nodes p and q
        RETURNS: Boolean showing if the nodes are connected
        '''
        # print('Super connected for {} and {}'.format(p, q))
        return self.find(p) == self.find(q) # 2 array accesses

    def count(self):
        '''
        Returns number of components (not sites)
        INPUT: 
        RETURNS: Integer with number of components
        '''
        # print('Super count returning {}'.format(self.N))
        return self.N

    
def test_tinyUF():
    tiny_file = 'data/tinyUF.txt'
    
    quick_find = QuickFindUnionFind(tiny_file)
    print('Quick-find result: {}'.format(quick_find))
    assert quick_find.id == [1,1,1,8,8,1,1,1,8,8]

    union_find = QuickUnionUnionFind(tiny_file)
    print('Union-find result: {}'.format(union_find))
    assert union_find.id == [1,1,1,8,3,0,5,1,8,8]

    union_find = WeightedQuickUnionUnionFind(tiny_file)
    print('Union-find result: {}'.format(union_find))
    assert union_find.id == [1,1,1,8,3,0,5,1,8,8]


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

    test_tinyUF()
    
    return 0
        
if __name__ == '__main__':
    sys.exit(main())
    
        
    
        
        