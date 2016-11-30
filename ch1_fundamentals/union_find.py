# Chapter 1.5: Union-Find

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
        
    
        
        