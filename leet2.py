'''
An array consists of N two-digit numbers. A group of numbers can be chosen
from the array only if all of them share at least one digit. For example,
numbers 52, 25 and 55 can be chosen together (they share digit 5), but 11,
52 and 34 cannot. What is the maximum number of array elements that can be
chosen together?

Write a function:
    def solution(A)
that, given an array A of length N, returns the maximum number of elements
that can be chosen.

Examples:
1. For A = [52, 25, 11, 52, 34, 55] the function should return 4.
   Elements 52, 25, 52 and 55 can be chosen (they all share digit 5).
2. For A = [71, 23, 57, 15] the function should return 2.
3. For A = [11, 33, 55] the function should return 1.
   No two numbers share any digit.
4. For A = [90, 90, 90] the function should return 3.

Constraints:
- N is an integer within the range [1..100]
- each element of array A is an integer within the range [10..99]
'''


def solution(A: list[int]) -> int:
    """
    A valid group requires ALL members to share at least one common digit.

    Key observation: if a group shares digit d, then EVERY number in the
    group contains d.  So the largest possible group for digit d is simply
    "all numbers in A that contain d."

    Since numbers are two-digit (10-99), each number has exactly one tens
    digit and one units digit.  We try all 10 possible shared digits (0-9),
    count how many numbers contain that digit, and return the maximum count.

    Time: O(10 * N) = O(N).  Correctness is the goal here.
    """
    best = 0

    for digit in range(10):                 # try every possible shared digit
        count = 0
        for num in A:
            tens  = num // 10               # e.g. 52 → tens=5
            units = num % 10               # e.g. 52 → units=2
            if tens == digit or units == digit:
                count += 1
        best = max(best, count)

    return best


# ─────────────────────────── tests ───────────────────────────

def run_tests():
    cases = [
        # ── given examples ──────────────────────────────────────────────────────
        # digit 5 appears in 52, 25, 52, 55 → 4
        ("Example 1: shared digit 5",
         [52, 25, 11, 52, 34, 55], 4),

        # best shared digit gives only 2 (e.g. digit 7: 71, 57)
        ("Example 2: best group has 2 elements",
         [71, 23, 57, 15], 2),

        # no two numbers share any digit
        ("Example 3: no shared digit, best is 1",
         [11, 33, 55], 1),

        # all share digit 9 (and also digit 0)
        ("Example 4: all share digit 9",
         [90, 90, 90], 3),

        # ── single element ───────────────────────────────────────────────────────
        # any single number trivially forms a group of size 1
        ("Single element",
         [42], 1),

        # ── all numbers share digit 0 ────────────────────────────────────────────
        # 10,20,30,40,50 all contain 0 → group of 5
        ("All numbers contain 0",
         [10, 20, 30, 40, 50], 5),

        # ── numbers share digit in both positions ─────────────────────────────────
        # 12 and 21 both contain digits 1 and 2 → group of 2
        ("Two numbers sharing both digits",
         [12, 21], 2),

        # ── all numbers share digit 3 ────────────────────────────────────────────
        # 13,31,53,35 all contain digit 3
        ("All four share digit 3",
         [13, 31, 53, 35], 4),

        # ── leading digit shared across all ─────────────────────────────────────
        # 10,11,12,13 all contain digit 1
        ("All share tens digit 1",
         [10, 11, 12, 13], 4),

        # ── unit digit shared across all ─────────────────────────────────────────
        # 55,56,57,58,59 all contain digit 5
        ("All share units digit 5... wait, 56 has 5 in tens",
         [55, 56, 57, 58, 59], 5),

        # ── duplicates of same number ─────────────────────────────────────────────
        # 99 contains 9 twice — still counts as one number containing 9
        ("Duplicates of same number",
         [99, 99, 99, 99], 4),

        # ── no two numbers share any digit (staircase pattern) ───────────────────
        # 12,34,56,78 — digits: {1,2},{3,4},{5,6},{7,8} — all disjoint
        ("No two numbers share a digit",
         [12, 34, 56, 78], 1),

        # ── two equally-sized groups, answer is max ──────────────────────────────
        # digit 1: 11,12,13 (3); digit 2: 12,22,23 (3) → best is 3
        ("Two tied groups of size 3",
         [11, 12, 13, 22, 23, 34], 3),

        # ── minimum and maximum two-digit values ─────────────────────────────────
        # 10 has digits 1,0; 99 has digits 9,9 — no overlap → best is 1
        ("Min value 10 and max value 99, no shared digit",
         [10, 99], 1),

        # ── all numbers share the same digit 9 ──────────────────────────────────
        # 99,98,97,96 all contain 9
        ("All contain digit 9",
         [99, 98, 97, 96], 4),

        # ── mixed: one digit dominates ───────────────────────────────────────────
        # digit 5: 15,25,35,45,55 → 5; others smaller
        ("One digit clearly dominates",
         [15, 25, 35, 45, 55, 11, 22, 33], 5),

        # ── number with 0 in units vs tens ───────────────────────────────────────
        # 10 (digit 0), 20 (digit 0), 30 (digit 0), 11 (no 0) → digit 0 count = 3
        ("Shared zero in units digit",
         [10, 20, 30, 11], 3),
    ]

    passed = 0
    for label, nums, expected in cases:
        result = solution(nums)
        ok = result == expected
        if ok:
            passed += 1
            print(f"  PASS  {label}")
        else:
            print(f"  FAIL  {label}")
            print(f"        input={nums}  got={result}  expected={expected}")

    print(f"\n{passed}/{len(cases)} tests passed.")
    if passed == len(cases):
        print("All tests passed!")


if __name__ == "__main__":
    run_tests()
