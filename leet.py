class LRUCache:

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.head = Node() #most recent used
        self.tail = Node() #least recent used
        self.mdict = dict()
        
    def remove(self,node):
        #all nodes have prev and next thanks to head and tail
        prev, next = node.prev, node.next
        prev.next = next
        next.prev = prev
        
    def insert(self,node):
        prev, next = self.head.prev, self.head
        prev.next = next.prev =node
        node.next, node.prev = next, prev
        
        
        
    def get(self, key: int) -> int:
        if key not in self.mdict:
            return -1
        node = self.mdict[key]
        #each time use the element, remove and reinsert
        self.remove(node)
        self.insert(node)
        return node.val
    
    def put(self, key: int, value: int) -> None:
        
        if key in self.mdict:
            self.remove(self.mdict[key])
            
        nNode = Node(key=key, val=val)
        #add to dict and list
        self.insert(nNode)
        self.mdict[key] = nNode
        
        #dismiss LRU
        if len(self.mdict) > capacity:
            lru = self.tail.next
            self.remove(self.mdict[lru])
            del self.mdict(lru.key)

            
        
    def __str__(self) -> str:
        s = "("+ str(self.head.val) + ") => "
        tm = self.head.next
        while tm:
            s += str(tm.val) + " -> "
            tm = tm.next
        s+='\n'
        s+=str(self.mdict)
        return s
   
    def __repr__(self):
        s = "("+ str(self.head.val) + ") => "
        tm = self.head.next
        while tm:
            s += str(tm.val) + " -> "
            tm = tm.next
        s+='\n'
        s+=str(self.mdict)
        return s
class Node():
    def __init__(self, key = -1, val = -1, next = None, prev=None):
        self.key = key
        self.val = val
        self.next = next
        self.prev = prev
    def __str__(self) -> str:
        return "(" +  str(self.key) + ": " + str(self.val) + ")"
    def __repr__(self) -> str:
        return "(" + str(self.key) + ": " + str(self.val) + ")"

capacity = 2

obj = LRUCache(capacity)
# param_1 = obj.get(3)
obj.put(2, 1)
obj.put(1, 1) 

obj.put(2, 3)

obj.put(4, 1)
 
print("get 1",obj.get(1)   )
print("get 2",obj.get(2)   )
print(obj)