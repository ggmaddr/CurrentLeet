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

import math
def reorderList(head: Optional[ListNode]) -> None:
    """
    Do not return anything, modify head in-place instead.
    """
    # find middle
    s, f = head, head
    while f.next and f.next.next:
        s = s.next
        f = f.next.next
    
    #split
    se = s.next #saved second half
    s.next = None #cut tail at mid
    #mid 's' still belongs to head -> cut tail of head
    
    #Reverse
    prev = None
    while se:
        tm = se.next
        se.next = prev
        prev = se
        se = tm
    
    se = prev #prev is reversed list
    
    #Merge 2 halves
    
    fi = head #first half
    
    while fi and se:
        fnext, snext = fi.next, se.next
        fi.next = se
        se.next = fnext
        fi, se = fnext,snext
    return head #for testing
    
head = [1,2,3,4,5,6,7,8,9]

head1 = create_list(head)

print(reorderList(head1))
