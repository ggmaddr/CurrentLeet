"""
Segment tree built from TreeNode (pointer-based).
Supports: build, point update, range-sum query.
"""


class SegmentTree:
    class TreeNode:
        def __init__(self, leftBound, rightBound, val):
            self.val = val
            self.leftBound = leftBound
            self.rightBound = rightBound
            self.leftChild = None
            self.rightChild = None

    def __init__(self, arr):
        self.n = len(arr)
        self.root = self._build(0, self.n - 1, arr)

    def _build(self, left, right, arr):
        """Recursively build tree, create leftChild/rightChild, return root node."""
        node = self.TreeNode(left, right, 0)
        if left == right:
            node.val = arr[left]
            return node
        mid = (left + right) // 2
        node.leftChild = self._build(left, mid, arr)
        node.rightChild = self._build(mid + 1, right, arr)
        node.val = node.leftChild.val + node.rightChild.val
        return node

    def update(self, index, value):
        """Point update: set arr[index] = value."""
        self._update(self.root, index, value)

    def _update(self, cur, index, value):
        if cur.leftBound == cur.rightBound == index:
            cur.val = value
            return
        mid = (cur.leftBound + cur.rightBound) // 2
        if index <= mid:
            self._update(cur.leftChild, index, value)
        else:
            self._update(cur.rightChild, index, value)
        cur.val = cur.leftChild.val + cur.rightChild.val

    def query(self, qLeft, qRight):
        """Range query: sum of arr[qLeft..qRight] (inclusive)."""
        return self._query(self.root, qLeft, qRight)

    def _query(self, cur, qLeft, qRight):
        if qRight < cur.leftBound or cur.rightBound < qLeft:
            return 0
        if qLeft <= cur.leftBound and cur.rightBound <= qRight:
            return cur.val
        return (
            self._query(cur.leftChild, qLeft, qRight) +
            self._query(cur.rightChild, qLeft, qRight)
        )


# Usage
if __name__ == "__main__":
    arr = [1, 2, 3, 4, 5, 16, 7, 8, 9, 18, 11, 13, 17]
    st = SegmentTree(arr)

    print(st.query(0, 2))   # 1+2+3 = 6
    print(st.query(5, 5))    # 16
    st.update(5, 6)
    print(st.query(5, 5))   # 6
