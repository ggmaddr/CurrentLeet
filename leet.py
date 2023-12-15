# from typing import Optional
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
#     def __repr__(self):
#         result = "tree: {"
#         queue = [self]

#         while queue:
#             current = queue.pop(0)

#             if current:
#                 result += str(current.val) + " "

#                 # Enqueue left and right children
#                 queue.append(current.left)
#                 queue.append(current.right)
#             else:
#                 result += "null "
#         result += "}"
#         return result.rstrip()
# def to_tree(lst):
#     if not lst:
#         return None

#     root = TreeNode(lst[0])
#     nodes = [root]
#     i = 1

#     while nodes and i < len(lst):
#         current = nodes.pop(0)

#         if lst[i] is not None:
#             current.left = TreeNode(lst[i])
#             nodes.append(current.left)

#         i += 1

#         if i < len(lst) and lst[i] is not None:
#             current.right = TreeNode(lst[i])
#             nodes.append(current.right)

#         i += 1

#     return root
# # root = [3,9,20,None,None,15,7]
# # mtree = to_tree(root)
# # mtree
# def kthSmallest(root: Optional[TreeNode], k: int) -> int:
#     count = 0
#     stack = [root]
#     cur = root
#     while stack or cur:
#         #go all the way to bottom left before performing code
#         while cur:
#             stack.append(cur) #all e in stack is not null
#             cur = cur.left
        
#         cur = stack.pop() 
#         #perform at node
#         count+=1
#         if count == k:
#             return cur.val
#         #go to rights
#         cur = cur.right
    
# root = to_tree([50, 30,90,15,40,72,101,10,25,None, None, 65, 76, 95, 110, 8, 12, None, None, 59, None, None, None, None, None, None,None, 6,9,11,13,7])
# print(root)
# print(kthSmallest(root, 2))
