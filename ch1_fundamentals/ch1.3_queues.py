# Stack of strings class
import sys

class QueueBase(object):
    '''Abstract Queue (FIFO) class'''

    def __init__(self):
        '''Creates an new Queue'''
        pass
    
    def enqueue(self, item):
        '''Adds an item on the back of the queue'''
        raise NotImplementedError
        
    def dequeue(self):
        '''Removes the item on the front of the queue'''
        raise NotImplementedError
        
    def is_empty(self):
        '''Is the stack empty?'''
        return self.size == 0
        
    def size(self):
        '''How many items are in the stack'''
        raise NotImplementedError

class QueueList(QueueBase):
    '''Implements a Queue (FIFO) using list. 
    Push uses append (end of list), Pop uses [0]
    Newest item at highest index'''
    
    def __init__(self):
        '''Creates and new Stack'''
        super(QueueList, self).__init__()
        self.items = list()

    def enqueue(self, item):
        '''Adds an item to the stack'''
        self.items.append(item)
        
    def dequeue(self):
        '''Pops the most recently added item off stack'''
        item = self.items.pop(0)
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
        self.first = None
        self.last = None
        self.verbose = verbose

    def __repr__(self):
        '''Returns a list of all the items in the linked list'''
        items = list()
        node = self.first
        while node.next_node is not None:
            items.append(node.item)
            node = node.next_node
        return str(items)

    def push_front(self, item):
        raise NotImplementedError

    def pop_front(self):
        if self.first is None:
            return None
        
        if self.first == self.last:
            single_node = self.first
            self.first = None
            self.last = None
            return single_node
        
        old_first = self.first
        self.first = self.first.next_node
        if self.verbose: print('After dequeue: {}'.format(self))
        return old_first.item

    def push_back(self, item):
        if self.last is None:
            new_node = LinkedListNode(item, None)
            self.first = new_node
            self.last = new_node
            return
        
        old_last = self.last
        new_node = LinkedListNode(item, None) # At end by definition so next is None
        old_last.next_node = new_node
        self.last = new_node
        if self.verbose: print('After enqueue: {}'.format(self))

    def pop_back(self):
        raise NotImplementedError

    def size(self):
        ''' Check how many items are in the linked list'''
        if self.first is None:
            return 0
        node = self.first
        node_count = 0
        
        while node.next_node is not None:
            node_count += 1
            node = node.next_node
        return node_count

class QueueLinkedList(QueueBase):
    '''Implements Queue using a linked list'''
    
    def __init__(self):
        '''Creates and new Stack'''
        super(QueueLinkedList, self).__init__()
        self.items = LinkedList()

    def enqueue(self, item):
        '''Adds an item to the stack'''
        self.items.push_back(item)
        
    def dequeue(self):
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

def string_test(queues):
    '''Runs a queue-of-strings test on the queues input tuple'''
    
    for queue in queues:
        print('Testing {}'.format(queue))
        assert queue.is_empty() == True, 'Stack is not empty after creation !'
        
        input = ('to','be','or','not','to', '-', 'be','-','-','that', '-', '-', '-', 'is' )
        exp_output = ['to', 'be', 'or', 'not', 'to', 'be']
        
        result = list()
        for item in input:
            if item == '-':
                result.append(queue.dequeue())
            else:
                queue.enqueue(item)
        
        assert queue.is_empty() == False, 'Stack is empty after pushes and pops !'
        
        passed = result == exp_output
        assert passed, 'Actual {}, expected {}'.format(result, exp_output)
        
        print('Test passed: {}'.format(passed))

def main(argv=None):
    if argv is None:
        argv = sys.argv
    
    string_test((QueueLinkedList(), QueueList()))
    
    
if __name__ == '__main__':
    sys.exit(main())
