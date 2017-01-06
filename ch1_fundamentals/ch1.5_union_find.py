# Chapter 1.5: Union-Find

# Needed to get command line arguments
import sys 

from timeit import Timer

class UnionFindBase(object):
    ''' Superclass with common functionality of all Union Find algos in book'''
    def __init__(self, filename=None):
        '''
        Initializes Union Find structure 
        '''
        if filename is not None:
            self.load_file(filename)
        
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
        # print('Super connected for {} and {}'.format(p, q))
        return self.find(p) == self.find(q)

    def count(self):
        '''
        Returns number of components (not sites)
        INPUT: 
        RETURNS: Integer with number of components
        '''
        # print('Super count returning {}'.format(self.N))
        return self.N
        
    def load_file(self, filename):
        '''
        Load data in file into union-find structure
        INPUT: string with filename to be loaded
        RETURNS: Nothing
        '''
        assert filename is not None, 'Error - please specify a file to load'

        line_count = 0
        try:
            with open(filename, 'r') as f:
                for line in f:
                    line_count += 1
                    
                    # Create new Union-Find using N on first line of file
                    if line_count == 1:
                        N = int(line)
                        self.N = N
                        self.id = list(range(N))
                        # print('Creating Union find with {} sites'.format(self.N))
    
                    else:
                        # Read in the line, strip space and convert to integer 
                        # print('Read Line #{} with sites: {}'.format(line_count, line))
                        sites = line.split(' ')
                        sites = [int(site.strip()) for site in sites]
                        p, q = sites
                        # print('Sites {} and {} connected? {}'.format(p, q, self.connected(p, q)))
                        if not self.connected(p, q):
                            self.union(p, q)
        except IOError as e:
            print('Error opening file - {}'.format(e))
            
class QuickFind(UnionFindBase):
    ''' Quick Find invariant:
    `p` and `q` are connected iff id[p] == id[q].
    All sites in the same component must have the same value in the id list
    When creating union, change all values in id[p] to id[q]
    '''
    def __init__(self, filename=None):
        super(QuickFind, self).__init__(filename)

    def __repr__(self):
        return '{}'.format(self.id)

    def connected(self, p, q):
        return super(QuickFind, self).connected(p, q)

    def count(self):
        return super(QuickFind, self).count()

    def load_file(self, filename=None):
        super(QuickFind, self).load_file(filename)

    def union(self, p, q):
        '''
        Merge components if two sites are in different components 
        INPUT: Site identifiers p and q
        RETURNS: None
        '''
        p_comp = self.id[p] # 1 array access
        q_comp = self.id[q] # 1 array access
        # list comp accesses: ~2N (1 to read value, w/c 1 to write back)
        self.id = [q_comp if val == p_comp else val for val in self.id]
        self.N -= 1
        
    def find(self, p):
        '''
        Component identifier for p
          -> Implement this in subclass
        INPUT: Site p
        RETURNS: Component ID
        '''
        return self.id[p] # 1 array access

class QuickUnion(UnionFindBase):
    ''' Quick Union invariant:
    Maintains invariant that components share the same root site
    id[] array entry is a link to another site in same component
    - Can link to itself, in which case it's a root
    When creating union, add link from id[p] to id[q]
    '''
    def __init__(self, filename=None):
        super(QuickUnion, self).__init__(filename)

    def __repr__(self):
        return '{}'.format(self.id)

    def connected(self, p, q):
        return super(QuickUnion, self).connected(p, q)

    def count(self):
        return super(QuickUnion, self).count()

    def load_file(self, filename=None):
        super(QuickUnion, self).load_file(filename)
    
    def find_root(self, p):
        ''' Helper function to follow links until root site found.
        Note by definition a root is an entry in the id list whose val == idx
        INPUT: Site identifier p
        RETURNS: Root site 
        '''
        p_idx = p
        while self.id[p_idx] != p_idx:
            p_idx = self.id[p_idx]
        return p_idx

    def union(self, p, q):
        '''
        Merge components if two sites are in different components 
        INPUT: Site identifiers p and q
        RETURNS: None
        '''
        p_root = self.find_root(p)
        q_root = self.find_root(q)
        self.id[p_root] = q_root
        self.N -= 1
        
    def find(self, p):
        '''
        Component identifier for p
          -> Implement this in subclass
        INPUT: Site p
        RETURNS: Component ID
        '''
        p_root = self.find_root(p)
        return p_root

class WeightedQuickUnion(UnionFindBase):
    ''' Weighted Quick Union invariant:
    Maintains invariant that components share the same root site
    id[] array entry is a link to another site in same component
    sz[] array tracks size of root nodes
    - Can link to itself, in which case it's a root
    When creating union, always update site to point from smaller to larger tree
    '''
    def __init__(self, filename=None):
        # Need our own load_file to create size array before calling unions
        self.load_file(filename)
        
    def __repr__(self):
        return '{}'.format(self.id)

    def connected(self, p, q):
        return super(WeightedQuickUnion, self).connected(p, q)

    def count(self):
        return super(WeightedQuickUnion, self).count()

    def find_root(self, p):
        ''' Helper function to follow links until root site found.
        Note by definition a root is an entry in the id list whose val == idx
        INPUT: Site identifier p
        RETURNS: Root site 
        '''
        p_idx = p
        while self.id[p_idx] != p_idx:
            # print(' * {} -> {}'.format(p_idx, self.id[p_idx]))
            p_idx = self.id[p_idx]
        
        return p_idx

    def union(self, p, q):
        '''
        Merge components if two sites are in different components 
        INPUT: Site identifiers p and q
        RETURNS: None
        '''
        p_root = self.find_root(p)
        q_root = self.find_root(q)

        if self.sz[p_root] < self.sz[q_root]:
            self.id[p_root] = q_root
            self.sz[q_root] += self.sz[p_root]
        else:
            self.id[q_root] = p_root
            self.sz[p_root] += self.sz[q_root]
        self.N -= 1
        
    def find(self, p):
        '''
        Component identifier for p
          -> Implement this in subclass
        INPUT: Site p
        RETURNS: Component ID
        '''
        p_root = self.find_root(p)
        return p_root

    def load_file(self, filename):
        '''
        Load data in file into union-find structure
        INPUT: string with filename to be loaded
        RETURNS: Nothing
        '''
        assert filename is not None, 'Error - please specify a file to load'

        line_count = 0
        try:
            with open(filename, 'r') as f:
                for line in f:
                    line_count += 1
                    
                    # Create new Union-Find using N on first line of file
                    if line_count == 1:
                        N = int(line)
                        self.N = N
                        self.id = list(range(N))
                        self.sz = [1 for _ in range(self.N)] # Weighing needs a size array too
                        # print('Creating Union find with {} sites'.format(self.N))
    
                    else:
                        # Read in the line, strip space and convert to integer 
                        # print('Read Line #{} with sites: {}'.format(line_count, line))
                        sites = line.split(' ')
                        sites = [int(site.strip()) for site in sites]
                        p, q = sites
                        # print('Sites {} and {} connected? {}'.format(p, q, self.connected(p, q)))
                        if not self.connected(p, q):
                            self.union(p, q)
        except IOError as e:
            print('Error opening file - {}'.format(e))
            
class PathCompressUnionFind(UnionFindBase):
    def __init__(self, filename=None):
        # Need our own load_file to create size array before calling unions
        self.load_file(filename)
        
    def __repr__(self):
        return '{}'.format(self.id)

    def connected(self, p, q):
        return super(PathCompressUnionFind, self).connected(p, q)

    def count(self):
        return super(PathCompressUnionFind, self).count()

    def find_root(self, p):
        ''' Helper function to follow links until root site found.
        Note by definition a root is an entry in the id list whose val == idx
        INPUT: Site identifier p
        RETURNS: Root site 
        '''
        p_idx = p
        while self.id[p_idx] != p_idx:
            # print(' * {} -> {}'.format(p_idx, self.id[p_idx]))
            p_idx = self.id[p_idx]
            self.id[p_idx] = self.id[self.id[p_idx]]
        
        p_root = p_idx
        p_idx = p
        
        # 2-pass to point all p_idx's children to p_idx
        while self.id[p_idx] != p_idx:
            # print(' * {} -> {}'.format(p_idx, self.id[p_idx]))
            p_idx = self.id[p_idx]
            self.id[p_idx] = p_root

        return p_idx

    def union(self, p, q):
        '''
        Merge components if two sites are in different components 
        INPUT: Site identifiers p and q
        RETURNS: None
        '''
        p_root = self.find_root(p)
        q_root = self.find_root(q)

        if self.sz[p_root] < self.sz[q_root]:
            self.id[p_root] = q_root
            self.sz[q_root] += self.sz[p_root]
        else:
            self.id[q_root] = p_root
            self.sz[p_root] += self.sz[q_root]
        self.N -= 1
        
    def find(self, p):
        '''
        Component identifier for p
          -> Implement this in subclass
        INPUT: Site p
        RETURNS: Component ID
        '''
        p_root = self.find_root(p)
        return p_root

    def load_file(self, filename):
        '''
        Load data in file into union-find structure
        INPUT: string with filename to be loaded
        RETURNS: Nothing
        '''
        assert filename is not None, 'Error - please specify a file to load'

        line_count = 0
        try:
            with open(filename, 'r') as f:
                for line in f:
                    line_count += 1
                    
                    # Create new Union-Find using N on first line of file
                    if line_count == 1:
                        N = int(line)
                        self.N = N
                        self.id = list(range(N))
                        self.sz = [1 for _ in range(self.N)] # Weighing needs a size array too
                        # print('Creating Union find with {} sites'.format(self.N))
    
                    else:
                        # Read in the line, strip space and convert to integer 
                        # print('Read Line #{} with sites: {}'.format(line_count, line))
                        sites = line.split(' ')
                        sites = [int(site.strip()) for site in sites]
                        p, q = sites
                        # print('Sites {} and {} connected? {}'.format(p, q, self.connected(p, q)))
                        if not self.connected(p, q):
                            self.union(p, q)
                            
        except IOError as e:
            print('Error opening file - {}'.format(e))
            
def test_union_find(filename, expected):

    quick_find = QuickFind(filename)
    actual = quick_find.count()
    assert actual == expected, print('QuickFind expected {}, got {}'.format(expected, actual))

    union_find = QuickUnion(filename)
    actual = union_find.count()
    assert actual == expected, print('QuickUnion expected {}, got {}'.format(expected, actual))

    union_find = WeightedQuickUnion(filename)
    actual = union_find.count()
    assert actual == expected, print('WeightedQuickUnion expected {}, got {}'.format(expected, actual))

    union_find = PathCompressUnionFind(filename)
    actual = union_find.count()
    assert actual == expected, print('PathCompressUnionFind expected {}, got {}'.format(expected, actual))



def main(argv=None):
    '''
    Function called to run main script including unit tests
    INPUT: List of arguments from the command line
    RETURNS: Exit code to be passed to sys.exit():
        -1: Invalid input
         0: Script completed successfully
    '''
    # print(timeit.repeat(test_naive_union_find, number=1000))

    # DIR = 'data/'
    # test_dict = {'tinyUF.txt' : 2,
    #              'mediumUF.txt' : 3,
    #              'largeUF.txt' : 6}
    
    # for file, exp in test_dict.items():
    #     print('Testing file {}'.format(file))
    #     test_union_find(DIR + file, exp)

    tiny_times = dict()
    algos = ('QuickFind', 'QuickUnion', 'WeightedQuickUnion', 'PathCompressUnionFind')
    files = ('mediumUF.txt',)
    NUM_RUNS = 10
    
    # for algo in algos:
    #     for file in files:
    #         function = '"' + algo + "('data/" + file + "')" + '"'
    #         imports = '"from __main__ import ' + algo + '"'
    #         # print('Testing function {}'.format(function))
    #         print('Command is {} & {}'.format(function, imports))
            
    #         t = Timer(function, imports)
    #         time = t.timeit(number=NUM_RUNS)/NUM_RUNS
    #         print(time)

    
    # tiny UF  
    print('\nTiming tinyUF.txt algorithms:')
    NUM_RUNS = 100

    t = Timer("QuickFind('data/tinyUF.txt')", "from __main__ import QuickFind")
    time = t.timeit(number=NUM_RUNS)/NUM_RUNS
    print('QuickFind - {}.'.format(time))

    t = Timer("QuickUnion('data/tinyUF.txt')", "from __main__ import QuickUnion")
    time = t.timeit(number=NUM_RUNS)/NUM_RUNS
    print('QuickUnion - {}.'.format(time))

    t = Timer("WeightedQuickUnion('data/tinyUF.txt')", "from __main__ import WeightedQuickUnion")
    time = t.timeit(number=NUM_RUNS)/NUM_RUNS
    print('WeightedQuickUnion - {}.'.format(time))

    t = Timer("PathCompressUnionFind('data/tinyUF.txt')", "from __main__ import PathCompressUnionFind")
    time = t.timeit(number=NUM_RUNS)/NUM_RUNS
    print('PathCompressUnionFind - {}.'.format(time))
    

    print('\nTiming mediumUF.txt algorithms:')
    NUM_RUNS = 100

    t = Timer("QuickFind('data/mediumUF.txt')", "from __main__ import QuickFind")
    time = t.timeit(number=NUM_RUNS)/NUM_RUNS
    print('QuickFind - {}.'.format(time))

    t = Timer("QuickUnion('data/mediumUF.txt')", "from __main__ import QuickUnion")
    time = t.timeit(number=NUM_RUNS)/NUM_RUNS
    print('QuickUnion - {}.'.format(time))

    t = Timer("WeightedQuickUnion('data/mediumUF.txt')", "from __main__ import WeightedQuickUnion")
    time = t.timeit(number=NUM_RUNS)/NUM_RUNS
    print('WeightedQuickUnion - {}.'.format(time))

    t = Timer("PathCompressUnionFind('data/mediumUF.txt')", "from __main__ import PathCompressUnionFind")
    time = t.timeit(number=NUM_RUNS)/NUM_RUNS
    print('PathCompressUnionFind - {}.'.format(time))


    print('\nTiming largeUF.txt algorithms:')
    NUM_RUNS = 1

    # Had to comment these two out, it runs for 10s of minutes
    
    # t = Timer("QuickFind('data/largeUF.txt')", "from __main__ import QuickFind")
    # time = t.timeit(number=NUM_RUNS)/NUM_RUNS
    # print(time)

    # t = Timer("QuickUnion('data/largeUF.txt')", "from __main__ import QuickUnion")
    # time = t.timeit(number=NUM_RUNS)/NUM_RUNS
    # print('QuickUnion - {}.'.format(time))

    t = Timer("WeightedQuickUnion('data/largeUF.txt')", "from __main__ import WeightedQuickUnion")
    time = t.timeit(number=NUM_RUNS)/NUM_RUNS
    print('WeightedQuickUnion - {}.'.format(time))

    t = Timer("PathCompressUnionFind('data/largeUF.txt')", "from __main__ import PathCompressUnionFind")
    time = t.timeit(number=NUM_RUNS)/NUM_RUNS
    print('PathCompressUnionFind - {}.'.format(time))

    return 0
        
if __name__ == '__main__':
    sys.exit(main())
    
        
    
        
        