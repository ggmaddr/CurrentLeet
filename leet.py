class LRUCache:

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.head = Node(0,0) #most recent used
        self.tail = Node(0,0) #least recent used
        self.mdict = {}
        self.tail.next, self.head.prev = self.head, self.tail
        
        
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
            print("get: ",-1)

            return -1
        node = self.mdict[key]
        #each time use the element, remove and reinsert
        self.remove(node)
        self.insert(node)
        print("get: ",node.val)
        return node.val
    
    def put(self, key: int, value: int) -> None:
        
        if key in self.mdict:
            self.remove(self.mdict[key])
            
        nNode = Node(key=key, val=value)
        #add to dict and list
        self.mdict[key] = nNode
        self.insert(nNode)
        
        #dismiss LRU
        if len(self.mdict) > self.capacity:
            lru = self.tail.next
            self.remove(lru)
            self.mdict.pop(lru.key)

            
        
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
    def __init__(self, key, val, next = None, prev=None):
        self.key = key
        self.val = val
        self.next = next
        self.prev = prev
    def __str__(self) -> str:
        return "(" +  str(self.key) + ": " + str(self.val) + ")"
    def __repr__(self) -> str:
        return "(" + str(self.key) + ": " + str(self.val) + ")"

capacity = 1

obj = LRUCache(capacity)
# param_1 = obj.get(3)
obj.put(2, 1)
obj.get(2)
obj.put(3, 2)
obj.get(2)
obj.get(3)

# obj.put(4, 1)
print(obj)