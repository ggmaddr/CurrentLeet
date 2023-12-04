from typing import Optional
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
    def __repr__(self):
        result = "tree: {"
        queue = [self]

        while queue:
            current = queue.pop(0)

            if current:
                result += str(current.val) + " "

                # Enqueue left and right children
                queue.append(current.left)
                queue.append(current.right)
            else:
                result += "null "
        result += "}"
        return result.rstrip()
def to_tree(lst):
    if not lst:
        return None

    root = TreeNode(lst[0])
    nodes = [root]
    i = 1

    while nodes and i < len(lst):
        current = nodes.pop(0)

        if lst[i] is not None:
            current.left = TreeNode(lst[i])
            nodes.append(current.left)

        i += 1

        if i < len(lst) and lst[i] is not None:
            current.right = TreeNode(lst[i])
            nodes.append(current.right)

        i += 1

    return root
from collections import deque
#BFS
def levelOrder(root: Optional[TreeNode]) -> list[list[int]]:
    res = []
    
    queue = deque([root])
    while queue:
        temp = [] #create new list at curr level
        #for each node at curr level
        for i in range(len(queue)):
            node = queue.popleft()  
            if node: 
                temp.append(node.val)

            if node.left:
                queue.append(node.left)
            if node.right: 
                queue.append(node.right)
        
        res.append(temp)
    return res
root = to_tree([3,9,20,None,None,15,7])
print(levelOrder(root))
    