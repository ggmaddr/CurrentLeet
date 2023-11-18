from typing import Optional

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
    def __str__(self):
        s = "("+ str(self.val) + ") => "
        tm = self.next
        while tm:
            s += str(tm.val) + " -> "
            tm = tm.next
        return s
    def __repr__(self):
        s = "("+ str(self.val) + ") => "
        tm = self.next
        while tm:
            s += str(tm.val) + " -> "
            tm = tm.next
        return s
            
            

def print_list(head: Optional[ListNode]) -> None:
    while head:
        print(head.val, end=" -> ")
        head = head.next
    print("None")

# Helper function to create a linked list from a list of values
def create_list(values):
    if not values:
        return None
    head = ListNode(values[0])
    current = head
    for val in values[1:]:
        current.next = ListNode(val)
        current = current.next
    return head

def removeNthFromEnd(head: Optional[ListNode], n: int) -> Optional[ListNode]:
    
    dummy = ListNode()
    #Dummy to remove head.
    dummy.next = head 
    l, r = dummy, head
    while n > 0:
       r = r.next
       n -=1
    #push r to null
    while r: 
        r = r.next
        l = l.next
    l.next = l.next.next
    
    return dummy.next

head = [1,2,3]

head1 = create_list(head)
print(removeNthFromEnd(head1,1))
    
