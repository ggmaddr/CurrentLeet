from collections import defaultdict 
#36. Valid Sudoku
def isValidSudoku(board: list[list[str]]) -> bool:
    #create hashset of cols, rows and sqr
    cols = defaultdict(set)
    rows = defaultdict(set)
    sqr = defaultdict(set)

def def_value(): 
    return "Present"
      
# Defining the dict 
d = defaultdict(def_value) 
d["a"] = 1
d["b"] = 2
  
print(d["a"]) 
print(d["b"]) 
print(d["c"]) 
    