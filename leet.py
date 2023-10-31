from collections import defaultdict 
#36. Valid Sudoku
def isValidSudoku(board: list[list[str]]) -> bool:
    #Idea: check if each small square belongs to coordinated-associated rows, cols, and sqr 
    #Implement: create hashset (dict of sets) as cols, rows and sqr
    #each row, col, sqr is a set
    #Form of each dict(set): e.g: rows = {0: {set}, 1:{set},...}
    cols = defaultdict(set) 
    rows = defaultdict(set)
    sqr = defaultdict(set)

    for r in range(9):
            for c in range(9):
                if board[r][c] == ".":
                    continue
                if (
                    board[r][c] in rows[r]
                    or board[r][c] in cols[c]
                    or board[r][c] in sqr[(r // 3, c // 3)]
                ):
                    return False
                cols[c].add(board[r][c])
                rows[r].add(board[r][c])
                sqr[(r // 3, c // 3)].add(board[r][c])

    return True