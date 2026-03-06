'''
There is a single-player board game with N positions described by a string.
Each position can be empty (denoted by '.'), contain a player's token
(denoted by 'T') or contain a coin ('C'). The player may possess multiple
tokens. A coin is collected by the player when a token is put on the coin's
position (each coin can be collected only once).

In one turn, the player can move a token by exactly three positions to the
right (the token does not stop on the positions in between). Every token can
be moved multiple times. The token cannot be moved if there is already
another token in the position it would move onto.

What is the maximum number of coins the player can collect?

Write a function:
    def solution(board)
that, given a string board of length N, returns the maximum number of coins
the player can collect.

Examples:
1. For board = "TT.T.CCCCC" the function should return 3.
2. For board = "T...CCCC" the function should return 1.
3. For board = "C..TT.CT.C" the function should return 2.

Constraints:
- N is an integer within the range [1..100]
- board consists only of the characters: '.', 'T' and/or 'C'
'''


def solution(board: str) -> int:
    """
    Key insight: every move is exactly +3 positions, so a token at index i
    can only ever be at positions i, i+3, i+6, ... (same remainder mod 3).
    The board splits into 3 completely independent "lanes":

        Lane 0: positions 0, 3, 6, 9, ...
        Lane 1: positions 1, 4, 7, 10, ...
        Lane 2: positions 2, 5, 8, 11, ...

    Within a lane tokens can only move right and cannot pass each other,
    but they COOPERATE: when a token is blocked by another token ahead,
    we first move that blocker further right (recursively), clearing the
    path.  This means every coin that has at least one token to its left
    in the lane can always be collected.

    So the answer = sum over all lanes of
        (number of coins that appear AFTER the first token in that lane).

    Time O(N), Space O(1).
    """
    total = 0

    for lane in range(3):
        found_token = False
        for i in range(lane, len(board), 3):
            if board[i] == 'T':
                found_token = True        # token is now "available" in this lane
            elif board[i] == 'C' and found_token:
                total += 1                # token to the left → always collectible

    return total


# ─────────────────────────── tests ───────────────────────────

def run_tests():
    cases = [
        # ── given examples ──────────────────────────────────────────────────────
        # Example 1: three different lanes each contribute coins
        ("Example 1",
         "TT.T.CCCCC", 3),

        # Example 2: single token in lane 0; coins in lanes 1 & 2 are unreachable
        ("Example 2",
         "T...CCCC", 1),

        # Example 3: coin at pos 0 is BEFORE the lane-0 token; only coins after it count
        ("Example 3",
         "C..TT.CT.C", 2),

        # ── smallest possible board (N = 1) ─────────────────────────────────────
        ("N=1, only a token",   "T",  0),
        ("N=1, only a coin",    "C",  0),
        ("N=1, empty cell",     ".",  0),

        # ── no tokens → zero coins collectible ──────────────────────────────────
        ("All coins, no tokens",                "CCCCC",   0),
        ("Coins spread across lane 0, no token","C..C..C",  0),

        # ── no coins → nothing to collect ───────────────────────────────────────
        ("All tokens, no coins",                "TTTTT",   0),

        # ── same-lane fundamentals ───────────────────────────────────────────────
        # Token at pos 0 (lane 0), coin at pos 3 (lane 0) → collectible
        ("Token then coin, same lane",          "T..C",    1),

        # Coin at pos 0 (lane 0), token at pos 3 (lane 0) → coin is to the LEFT, not collectible
        ("Coin before token, same lane",        "C..T",    0),

        # Token at pos 0 (lane 0), coin at pos 1 (lane 1) → different lanes, no interaction
        ("Token and coin in different lanes",   "TC",      0),

        # ── one token can sweep MULTIPLE coins ──────────────────────────────────
        # Token hops 0→3→6→9, collecting every coin it lands on
        ("One token sweeps 3 coins in lane 0",  "T..C..C..C",  3),

        # ── two tokens cooperating ──────────────────────────────────────────────
        # Right token moves first (to pos 6), left token follows (to pos 3),
        # right token moves again (to pos 9). Both coins collected.
        ("Two tokens cooperate to collect 2 coins", "T..T..C..C", 2),

        # ── every lane contributes equally ──────────────────────────────────────
        # TTTCCC: lane0=(T@0,C@3), lane1=(T@1,C@4), lane2=(T@2,C@5) → 3 coins
        ("3 tokens + 3 coins, one per lane",    "TTTCCC",  3),

        # ── all coins precede all tokens → nothing collectible ──────────────────
        # CCCTTTTTT: in each lane the coin comes before the tokens
        ("All coins before all tokens",         "CCCTTTTTT", 0),

        # ── coin before AND after the same token ────────────────────────────────
        # C at pos 0 is before the token; C at pos 6 is after → only 1 collected
        ("Coin before token (bad) + after token (good)", "C..T..C", 1),

        # ── two coins before, two coins after the only token ────────────────────
        # lane 0: C(0), C(3), T(6), C(9), C(12) → 2 collected (only after T)
        ("Two coins before token, two after",   "C..C..T..C..C", 2),

        # ── token in lane 0 only; lanes 1 and 2 have coins but no tokens ─────────
        # T(0),C(3),C(6) in lane 0 → 2; lane1: C(1),C(4) no token; lane2: C(2),C(5) no token
        ("Token in lane 0 only, coins in all lanes", "TCCCCCC", 2),

        # ── long-range sweeping across the whole board ───────────────────────────
        # Positions 0,6,12,18 are all in lane 0; token at 0 sweeps coins at 6,12,18
        ("Token sweeps 3 distant coins in lane 0", "T.....C.....C.....C", 3),
    ]

    passed = 0
    for label, board, expected in cases:
        result = solution(board)
        ok = result == expected
        if ok:
            passed += 1
            print(f"  PASS  {label}")
        else:
            print(f"  FAIL  {label}")
            print(f"        board={board!r}  got={result}  expected={expected}")

    print(f"\n{passed}/{len(cases)} tests passed.")
    if passed == len(cases):
        print("All tests passed!")


if __name__ == "__main__":
    run_tests()
