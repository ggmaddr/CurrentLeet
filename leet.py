class LRUCache:

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.head = Node() #most recent used
        self.tail = Node() #least recent used
        self.mdict = dict()
        
    def getUse(self, uNode):
        
        
        currhead= self.head
        self.head = uNode 
        self.head.next = currhead
        currhead.prev = uNode
        
        self.head.prev = None
    
    def get(self, key: int) -> int:
        if key not in self.mdict.keys():
            return -1
        
        getNode = self.mdict[key]

        
        if not getNode.prev: #if node is head
            return getNode.val
        
        #if node is tail
        if not getNode.next:
            self.tail = getNode.prev #update tail
            self.tail.next = None
            # print("im tail 1", self.tail)
        else:
            getNode.next.prev = getNode.prev #next point back to getNode's back 
            getNode.prev.next = getNode.next #prev point next to getNode's next
        
        
        # print("im tail " /, self.tail)

        return getNode.val
        
        
    def put(self, key: int, value: int) -> None:
        
        if key in self.mdict.keys():
            node = self.mdict[key]
            node[key] = value
            
        
        #if first node
        if self.head.val == -1:
            self.head = Node(key=key,val=value)
            self.mdict[key] = self.head
            return 
        
        newN = Node(key=key, val=value) #new node
        
        #add to front
        currhead = self.head
        #if not head.next (tail not exist)
        if not currhead.next:
            self.tail = currhead
            
        currhead.prev = newN
        newN.next = currhead
        
        
        self.head = newN
        self.mdict[key] = self.head
        
        #dismiss the LRU
        if len(self.mdict) > self.capacity:
            
            ntail = self.tail.prev #next tail
            ntail.next = None
            
            self.mdict.pop(self.tail.key)#Reason why Node should have key attribute

            self.tail = ntail

            
        
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