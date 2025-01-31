# Practicing writing recursive methods
# Also practicing using doctests and exceptions

from idlelib.configdialog import is_int

def count_down_from_n(n:int):
    '''
    Counts down from n to 1 for some non-negative integer n. Numbers are printed on the same line

    :param n:
    :return: prints decreasing sequence of numbers n, n-1, . . .

    Example:
    >>> count_down_from_n(10)
    10 9 8 7 6 5 4 3 2 1

    >>> count_down_from_n(0)
    'Invalid input. Please select a non-negative integer.'

    '''

    try:
        is_int(n)
        if n <= 0:
            return 'Invalid input. Please select a non-negative integer.'
        if n == 1:
            return 1
        else:
            print(n, end = ' ') # print numbers on same line with spaces in between each value
            return count_down_from_n(n-1)

    except:
        'Invalid input. Please select a non-negative integer.'

# print(count_down_from_n(5))
# print(count_down_from_n(0))

def factorial(n):
    '''

    Recursively computes factorial of n for non-negative values of n. Returns an error in other cases

    :param n: non-negative integer
    :return: n!

    Example:
    >>> factorial(0)
    1

    >>> factorial(-1)
    'Invalid input. Please select a non-negative integer.'

    >>> factorial(1.5)
    'Invalid input. Please select a non-negative integer.'

    >>> factorial(5)
    120

    '''

    try:
        isinstance(n, int)
        if n < 0:
            return 'Invalid input. Please select a non-negative integer.'
        else:
            if n == 0:
                return 1
            else:
                return n*factorial(n-1)

    except:
        return 'Invalid input. Please select a non-negative integer.'


def fibonacci_recur1(n:int):

    '''
    Computes nth Fibonacci number. Note: treats F_1 = 1 and F_2 = 1

    This method is inefficient (exponential order). See fibonacci_recur2 for a dictionary based method
    which is more efficient recursive method. See fib_iter (further down) for an iterative method that
    is O(n)

    :param n: integer n
    :return: nth Fibonacci #


    Examples:

    >>> fibonacci_recur1(-1)
    'Invalid input. Please choose a non-negative integer.'

    >>> fibonacci_recur1(1)
    1

    >>> fibonacci_recur1(2)
    1

    >>> fibonacci_recur1(5)
    5

    >>> fibonacci_recur1(29)
    514229


    '''

    if n < 1:
        return 'Invalid input. Please choose a non-negative integer.'
    elif n == 1 or n == 2:
        return 1
    else:
        return fibonacci_recur1(n-1) + fibonacci_recur1(n-2)


print(fibonacci_recur1(10))

def fibonacci_recur2(n:int, fib_dict = {1:1,2:1}):

    '''
    Computes nth Fibonacci number. Note: treats F_1 = 1 and F_2 = 1

    This method is more efficient than fibonacci_recur1 since it uses a diciontary to set initial
    values of sequence and to access previously computed values.

    Note that the dictionary of initial values is a function parameter. The dictionary defaults
    two the first two fibonacci numbers. Additionally, the dictionary is mutated throughout the
    recursive calls

    :param n: integer n
    :return: nth Fibonacci #


    Examples:

    >>> fibonacci_recur2(-1)
    'Invalid input. Please choose a non-negative integer.'

    >>> fibonacci_recur2(1)
    1

    >>> fibonacci_recur2(2)
    1

    >>> fibonacci_recur2(5)
    5

    >>> fibonacci_recur2(29)
    514229


    '''

    if n < 0:
        return 'Invalid input. Please choose a non-negative integer.'

    if n in fib_dict:
        return fib_dict[n]  # return key (fibonacci #) if dictionary contains n
    else:
        # next_val = fibonacci_recur2(n-1, fib_dict) + fibonacci_recur2(n-2, fib_dict)
        fib_dict[n] = fibonacci_recur2(n-1, fib_dict) + fibonacci_recur2(n-2, fib_dict)
        return fib_dict[n]



def get_permutations(sequence):
    '''
    Enumerates all permutations of a given string using recursion

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.

    Returns: a list of all permutations of sequence in alphabetical order

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    '''

    seq = sequence  # shorter variable name for sequence to be permuted
    perm_list = []   # initialize empty list to hold permutations
    if len(seq) <= 1:
        perm_list.append(seq)    # append sequence to list
        return perm_list # return the string if it has 1 character or 0 characters


    if len(seq) > 1:# if string has length > 1
        char = seq[0]   # store first character of sequence -- char
        sub_str = seq[1:len(seq)]   # store remaining characters of sequence as substring-- perm_sub
        for perm in get_permutations(sub_str): # recursive call to function; loop over list of permuted substrings
            for i in range(len(perm)+1):    # loop over length of substring. note the upper index is length + 1
                new_perm = perm[0:i] + char + perm[i:len(perm)] # insert first character in each possible position in substring
                perm_list.append(new_perm)      # append permutation to list
        return sorted(perm_list)    # sort final list alphabetically


def cart_product(A:set, B:set):

    '''
    Returns the cartesian product of sets A and B which a set of 2-tuples.
    Not recursive but including it here.


    :param A: a set A
    :param B: a set B
    :return: all 2-tuples in the cartesian product of A and B
    '''

    return {(a,b) for a in A for b in B}    # non-recursive method




def cart_product_n(S, n:int):

    '''
    Computes the cartesian product of an iterable object S with itself n times. Returns
    the list of tuples in the product.

    For example cart_product({1,2},2) returns [(1,1), (1,2), (2,1), (1,2)]

    :param s: A set of
    :param n: integer
    :return:
    '''

    if len(S) < 1:
        return [tuple()]   # return list of empty tuples
    if n == 0:
        return [tuple()]
    else:
        prod_list = []
        for x in S:     # iterate over elements of S
            for tup in tuple(cart_product_n(S,n-1)): # iterate over tuples in previous sub product
                prod_list.append((x,) + tup)        # add each element of S onto product and append to list
    return prod_list


def power_set(n:int):
    '''
    Given an integer n, returns all possible subsets of integers 1,2,3,...,n (including empty set)

    Note: A function that  takes a list and returns the subsets would be better. See below gen_power_set()

    :param n: positive integer n
    :return: returns list of all possible subsets of integers 1,2,...,n
    '''
    if n == 0:
        return [[]]     # return list containing empty list
    else:
        p_set = []
        sub_power_set = power_set(n-1)     # generate power set of integers from 1 to n-1
        for x in sub_power_set:            # iterate over sub power set
            p_set.append(x + [n])          # add n to each element of sub power set
        return sub_power_set + p_set       # combine lists to create power set

def gen_power_set(L):
    '''
    Given an iterable (list, tuple, etc.) generates the power set of elements in the iterable.
    The power set is returned as a *LIST*

    Note: The power set is the set of all possible sets (i.e. subsets of any size)

    :param L: iterable
    :return: list representing power set of elements in iterable

    Examples:

    >>> gen_power_set([])
    [[]]

    >>> gen_power_set([1,2])
    [[], [1], [2], [1, 2]]

    >>> gen_power_set((1,2,3))
    [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]

    >>> gen_power_set('abc')
    [[], ['a'], ['b'], ['a', 'b'], ['c'], ['a', 'c'], ['b', 'c'], ['a', 'b', 'c']]
    '''

    if len(L) == 0 :
        return [[]]     # return empty list if iterable is empty
    power_subset = gen_power_set(L[:-1])   # generate power set of set excluding the last element of L
    last = [L[-1]]    # create list containing last element of L. The element is put into a list so that the function works for any iterable L
    temp_set = []      # empty set that will hold new subsets
    for subset in power_subset:
        temp_set.append(subset + last) # concatenate last element of L to each member of the "power_subset" and append result to temp list
    return power_subset + temp_set      # add power subset and temp set to get power set

def fib_iter(n:int):
    '''

    Iterative implementation of generating Fibonacci numbers. This method is O(n)

    :param n: non-negative integer n
    :return: n_th Fibonacci number
    '''

    # iterative implementation of fibonacci
    #

    if n < 0:
        return 'Choose a non-negative integer'

    if n == 0:
        return 0
    if n == 1:
        return 1
    fib_i = 0  # set base cases
    fib_ii = 1
    for i in range(n-1):
        tmp_fib = fib_i             # store value temporarily for assignment (current value of first fib #)
        fib_i = fib_ii              # second fib value for current iteration becomes first fib value for next iteration
        fib_ii = tmp_fib + fib_ii  # second fib for next iteration is sum of current two fib values
    return fib_ii