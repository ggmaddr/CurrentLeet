#!/bin/python3

import math
import os
import random
import re
import sys


#
# Complete the 'fizzBuzz' function below.
#
# The function accepts INTEGER n as parameter.
#

def fizzBuzz(n):
    # Write your code her
    
    for i in range(n):
        if i%3==0 and i%5==0:
            print("FizzBuzz")
        
    
    return 0
if __name__ == '__main__':
    n = int(input().strip())

    fizzBuzz(n)
