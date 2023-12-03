def print_spiral(matrix):
    if not matrix:
        print("Matrix is empty.") 
        return
    top, bottom = 0, len(matrix) - 1 
    left, right = 0, len(matrix[0]) - 1
    while top <= bottom and left <= right:
    # Traverse from left to right along the top row 
        for i in range(left, right + 1):
            print(matrix[top][i], end=" ") 
        top += 1
    # Traverse from top to bottom along the right column
        for i in range(top, bottom + 1): 
            print(matrix[i][right], end=" ")
        right -= 1
    # Traverse from right to left along the bottom row (only if
        if top <= bottom:
            for i in range(right, left -1, -1):
                print(matrix[bottom][i], end=" ") 
            bottom -= 1
        # Traverse from bottom to top along the left column (only if
        if left <= right:
            for i in range(bottom, top - 1, -1):
                print(matrix[i][left], end=" ") 
            left += 1
    print()
matrix = [[1,2,3],[4,5,6],[7,8,9]]
print(print_spiral(matrix))