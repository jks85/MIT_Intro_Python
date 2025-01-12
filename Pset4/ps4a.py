# Problem Set 4A
# Name: <jks85>
# Collaborators:
# Time Spent: x:xx

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
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
                new_perm = perm[0:i] + char + perm[i:len(perm)] # insert first character in each position in substring
                perm_list.append(new_perm)
        return sorted(perm_list)    # sort final list alphabetically

print(len(get_permutations('Angela')))





if __name__ == '__main__':
#    #EXAMPLE
#    example_input = 'abc'
#    print('Input:', example_input)
#    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
#    print('Actual Output:', get_permutations(example_input))
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)

    pass #delete this line and replace with your code here

