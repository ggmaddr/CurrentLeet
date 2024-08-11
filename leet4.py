from typing import Optional

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
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
import copy
def reorderList(head: Optional[ListNode]) -> None:
    """
    Do not return anything, modify head in-place instead.
    """
    if head.next == None or head.next.next == None:
        return head
        
    r = 0
    cur = head
    mlist = list()
    while cur:
        mlist.append(cur)
        r+=1
        cur = cur.next
    
    stop = r//2
    for l in range (stop):
        # todo: examine 3-4-5 case.   
        mlist[l].next = mlist[r-1]
        mlist[r-1].next = mlist[l+1]
        r-=1
    mlist[r-1].next = None
    print(head)
    return head


head = [1,2,3,4]

head1 = create_list(head)
print(head1)

print(reorderList(head1))