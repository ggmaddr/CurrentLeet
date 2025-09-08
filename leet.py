# def convert(s: str, numRows: int) -> str:
#     if numRows == 1 or numRows >= len(s):
#         return s
    
#     rows = [""] * numRows
#     row, direction = 0, 1  # Start at row 0 and move down

#     for char in s:
#         rows[row] += char  # Add character to current row
#         if row == 0:  # If at the top, move down
#             direction = 1
#         elif row == numRows - 1:  # If at the bottom, move up
#             direction = -1
#         row += direction  # Update row index
    
#     return "".join(rows)  # Concatenate all rows
# s = "PAYPALISHIRING"
# numRows = 4
# convert(s, numRows)

from collections import Counter

def getMinimumCost(arr):
    # Count frequencies of elements
    freq = Counter(arr)
    
    # Sort elements by frequency (descending)
    sorted_elements = sorted(freq.items(), key=lambda x: -x[1])
    # Reconstruct the array by grouping identical elements
    grouped_arr = []
    for element, count in sorted_elements:
        grouped_arr.extend([element] * count)
    print(grouped_arr)

    # Calculate cost: sum of distinct elements in prefixes
    distinct_elements = set()
    cost = 0
    for num in grouped_arr:
        distinct_elements.add(num)
        cost += len(distinct_elements)
    
    return cost

arr = [2, 2, 2,1,3,5,6,3, 3, 1, 1]
# arr = [1,4,3,2]
print(getMinimumCost(arr))  # Output: 9
