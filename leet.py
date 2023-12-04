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
# root = [3,9,20,None,None,15,7]
# mtree = to_tree(root)
# mtree

#Approach 2: O(mn)
def isSubtree(root: TreeNode, t: TreeNode) -> bool:
 
    print(root, t)    

    if not t:
        return True
    if not root:
        print("lastfalse 1")
        return False
    
    if isSameTree(root, t):
        return True
    #dfs traverse: If leftsub tree is equal or rightsubtree is equal
    boole = isSubtree(root.left, t) or isSubtree(root.right, t)
    if not boole: print("lastfalse 2")

    return boole
def isSameTree(q,p) -> bool:
    if not q and not p:
        return True
    
    if p and q and p.val == q.val:
        return isSameTree(p.left,q.left) and isSameTree(p.right,q.right) 
    
    return False #False otherwise

root = to_tree([1,None,1,None,1,None,1,None,1,None,1,None,1,None,1,None,1,None,1,None,1,2])
t = to_tree([1,None,1,None,1,None,1,None,1,None,1,2])

print(isSubtree(root, t))