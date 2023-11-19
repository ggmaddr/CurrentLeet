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

def addTwoNumbers(l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        res = ListNode()
        temp = res
        carr = 0 #carry
        
        #finsih loop while both l1 and l2 end
        while l1 or l2:
            
            if l1 and l2:
                ssum = l1.val + l2.val + carr
            elif l1:
                ssum = l1.val + carr if l1 else l2.val + carr
        
            temp.val = ssum%10
            carr = ssum//10

            l1 = l1.next if l1 else None
            l2 = l2.next if l1 else None
            if l1 or l2:
                temp.next = ListNode()
                temp = temp.next
                
        if carr == 1:
            temp.next = ListNode()
            temp = temp.next
        
        return res
l1 = create_list([9,9,9,9,9,9,9])
l2 = create_list([9,9,9,9])
addTwoNumbers(l1, l2)

    
