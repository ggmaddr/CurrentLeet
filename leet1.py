
def solution(S):
  moves = 0
  n = len(S)
  for pathway in range(3):
    hasTokenBefore = False
    for i in range(pathway, n, 3):
      if S[i] == 'T':
        hasTokenBefore = True
      elif S[i] == 'C' and hasTokenBefore:
        moves+=1
  return moves

# ─────────────────────────── tests ───────────────────────────
print("GRADY CUSTOM TEST", solution("C..TT.CT.C"))