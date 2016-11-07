# Bag ADT implementation

class Bag(object):
    def __init__(self):
        ''' Initializes an empty bag '''
        self.items = list() # Assume duplicates are allowed
    
    def add(self, item):
        ''' Adds an item to a bag'''
        self.items.append(item)
        
    def is_empty(self):
        ''' Returns bool showing if bag is empty'''
        return self.size() == 0
        
    def size(self):
        ''' Returns number of items in the bag'''
        return len(self.items)


# Unit tests for the bag
if __name__ == '__main__':

    test_bag = Bag()
    
    assert test_bag.size() == 0
    assert test_bag.is_empty() == True
    
    test_bag.add('a')
    assert test_bag.size() == 1
    assert test_bag.is_empty() == False

    test_bag.add('a') # Will only pass if duplicates are allowed
    assert test_bag.size() == 2
    assert test_bag.is_empty() == False

    test_bag.add(1)
    assert test_bag.size() == 3
    assert test_bag.is_empty() == False
    
    print('All tests passed')
