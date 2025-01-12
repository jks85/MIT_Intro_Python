import math


'''
Write a program that does the following in order:
    1. Asks the user to enter a number “x”
    2. Asks the user to enter a number “y” 
    3. Prints out number “x”, raised to the power “y”.
    4. Prints out the log (base 2) of “x”.
'''

def ops():
    x = int(input('Enter a number "x": '))
    y = int(input('Enter a number "y": '))
    print(str(x),'raised to the power of',str(y),'is',str(x**y))
    return print('log base 2 of',str(x),'is',str(math.log2(x)))

ops()