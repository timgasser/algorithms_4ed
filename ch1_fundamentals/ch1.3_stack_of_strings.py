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

class StackOfStringsList(StackBase):
    '''Implements stack using list. Newest item at highest index'''
    
    def __init__(self):
        '''Creates and new Stack'''
        super(StackOfStringsList, self).__init__()
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

class LinkedListNode(object):
    '''Node inside a linked list'''
    def __init__(self, item, next_node):
        self.item = item
        self.next_node = next_node
            
    def __repr__(self):
        return 'Item: {}, ptr: {}'.format(self.item, self.next_node)
    
class LinkedList(object):
    '''Linked List class'''
    
    def __init__(self, verbose=False):
        '''Creates a new linked list with no entries initially'''
        self.tail = LinkedListNode(None, None) # Pointer of None means end of chain
        self.head = LinkedListNode(None, self.tail)
        self.verbose = verbose

    def __repr__(self):
        '''Returns a list of all the items in the linked list'''
        items = list()
        node = self.head.next_node
        while node is not self.tail:
            items.append(node.item)
            node = node.next_node
        return str(items)

    def push_front(self, item):
        '''Adds an item to the front of the list'''
        old_first_node = self.head.next_node
        new_node = LinkedListNode(item, old_first_node)
        self.head.next_node = new_node
        if self.verbose: print('After push: {}'.format(self))

    def pop_front(self):
        '''Pops the item at the front of the list'''
        old_first_node = self.head.next_node
        if old_first_node == self.tail:
            return None # Nothing to pop if head -> tail, early out
            
        old_second_node = old_first_node.next_node
        self.head.next_node = old_second_node
        
        if self.verbose: print('After pop : {}'.format(self))
        return old_first_node.item

    def push_back(self, item):
        '''Adds an item to the back of the list'''
        raise NotImplementedError
        
    def pop_back(self):
        '''Pops the item at the back of the list'''
        raise NotImplementedError

    def size(self):
        ''' Check how many items are in the linked list'''
        node = self.head
        node_count = 0
        while node.next_node != self.tail:
            node_count += 1
            node = node.next_node
        return node_count

class StackOfStringsLinkedList(StackBase):
    '''Implements stack using list. Newest item at highest index'''
    
    def __init__(self):
        '''Creates and new Stack'''
        super(StackOfStringsLinkedList, self).__init__()
        self.items = LinkedList()

    def push(self, item):
        '''Adds an item to the stack'''
        self.items.push_front(item)
        
    def pop(self):
        '''Pops the most recently added item off stack'''
        node = self.items.pop_front()
        return node
        
    def is_empty(self):
        '''Is the stack empty?'''
        empty = (self.size() == 0)
        return empty

    def size(self):
        '''How many items are in the stack'''
        return self.items.size()



def string_test(stacks):
    '''Runs a stack-of-strings test on the stacks input tuple'''
    
    for stack in stacks:
        print('Testing {}'.format(stack))
        assert stack.is_empty() == True, 'Stack is not empty after creation !'
        
        input = ('to','be','or','not','to', '-', 'be','-','-','that', '-', '-', '-', 'is' )
        exp_output = ['to', 'be', 'not', 'that', 'or', 'be']
        
        result = list()
        for item in input:
            if item == '-':
                result.append(stack.pop())
            else:
                stack.push(item)
        
        assert stack.is_empty() == False, 'Stack is empty after pushes and pops !'
        
        passed = result == exp_output
        assert passed, 'Actual {}, expected {}'.format(result, exp_output)
        
        print('Test passed: {}'.format(passed))

def main(argv=None):
    if argv is None:
        argv = sys.argv
    
    
    string_test((StackOfStringsList(), StackOfStringsLinkedList()))
    
    
if __name__ == '__main__':
    sys.exit(main())
