# Stack of strings class
import sys

class StackBase(object):
    '''Abstract Stack of Strings class'''

    def __init__(self):
        '''Creates and new Stack'''
        pass
    
    def push(self, item):
        '''Adds an item to the stack'''
        raise NotImplementedError
        
    def pop(self):
        '''Pops the most recently added item off stack'''
        raise NotImplementedError
        
    def is_empty(self):
        '''Is the stack empty?'''
        return self.size == 0
        
    def size(self):
        '''How many items are in the stack'''
        raise NotImplementedError


class StackOfStrings(StackBase):
    '''Implements stack using list. Newest item at highest index'''
    
    def __init__(self):
        '''Creates and new Stack'''
        super(StackOfStrings, self).__init__()
        self.items = list()

    def push(self, item):
        '''Adds an item to the stack'''
        self.items.append(item)
        
    def pop(self):
        '''Pops the most recently added item off stack'''
        item = self.items.pop()
        return item
        
    def is_empty(self):
        '''Is the stack empty?'''
        empty = (self.size() == 0)
        return empty

    def size(self):
        '''How many items are in the stack'''
        return len(self.items)



def main(argv=None):
    if argv is None:
        argv = sys.argv
    
    stack = StackOfStrings()
    assert stack.is_empty() == True, 'Stack is not empty after creation !'
    
    result = list()
    for item in ('to','be','or','not','to', '-', 'be','-','-','that', '-', '-', '-', 'is' ):
        if item == '-':
            result.append(stack.pop())
        else:
            stack.push(item)
    
    assert stack.is_empty() == False, 'Stack is empty after pushes and pops !'

    
    print('Result is {}'.format(result))
    

    
    
if __name__ == '__main__':
    sys.exit(main())
