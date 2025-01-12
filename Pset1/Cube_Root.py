## Procedures to find the cube root of a number
## Practicing writing loops
## Three algorithms for computing cube root
## Guess and check
## Approximate by
## Approximate using bisection
from setuptools.archive_util import default_filter


# Cube root via guess and check
# iterates over integers 1,2,...,n where n is number we want the cube root of
# checks if each integer is the cube root
# returns "not an integer" if the cube root is irrational
# note this method can  only support integers
# however it assumes |x| > 1

def cube_root_guess(x:int):
    cube = x
    for guess in range(abs(cube)+1):
        if guess**3 >= abs(cube):
            break

    if guess**3 != abs(cube):
        return 'The cube root of ' + str(cube) + ' is not an integer'
    else:
        if cube < 0:
            guess = -guess
        return 'The cube root of ' + str(cube) + ' is ' + str(guess)




# Approximate Cube Root
# Set initial guess and test absolute difference
# set tolerance level to end loops
# increment guess
# Note that if the delta increment is too large the error may not become small enough to break the loop
# resulting in a poor approximation
# Also note that this method can support floats and fractions
# Function runs recursively if |x| < 1 and x != 0.
# Could also bisect interval differently instead. Not sure which is faster, but this required less code

def cube_root_approx(x:float,tol:float = 0.01):
    # tol is tolerance level, % error
    cube = x  # set cube
    if cube == 0:
        return 0
    guess = 1   # initial guess
    delta = .0001 # increment for testing values
    iteration = 0
    abs_err = abs(guess**3 - abs(cube)) # compute initial absolute error
    #abs_perc_err = abs((guess**3 - abs(cube))/abs(cube)) # absolute percentage error
    while abs_err >= tol and abs(guess**3) <= abs(cube):
    #while abs_perc_err > 0.0001 and abs(guess**3) < abs(cube):
        guess += delta
        abs_err = abs(guess ** 3 - abs(cube))
        iteration +=1
    if cube < 0:
        guess = -guess
    if abs_err >= tol:
        print(iteration, ' iterations occurred')
        return 'No solution found'
    print(iteration,'iterations occurred')
    return guess


#print(cube_root_approx(0))


## Bisection method
## consider interval from [0,cube], inclucusive
# compute midpoint of interval and check its cube
# if that value < cube pick lower half of original interview
# if that value > cube pick upper half
# check error level
# repeat process using new interval until acceptable level of error has been reached
# may not work for negative values?

def cube_root_bisec(x:float,tol:float = 0.01):
    if x == 0:     # return 0 if value is 0
        return 0
    if abs(x) < 1 :      # if value is between -1 and 1 call function on reciprocal
        return 1/cube_root_bisec(1/x)
    else:
        cube = x
        low = 0 # set initial lower endpoint
        high = abs(cube) # set initial higher endpoint
        guess = (low+high)/2 # set initial guess as midpoint of interval from 0 to cube
        abs_err = abs(guess**3 - abs(cube)) # set initial absolute error
        iterations = 0 # set iteration counter
        while abs_err >= tol:
            if guess**3 < abs(cube):
                low = guess
            elif guess**3 > abs(cube):
                high = guess
            guess = (low + high)/2
            abs_err = abs(guess ** 3 - abs(cube)) # update error
            iterations += 1
            print(abs_err)
        if cube < 0:
            guess = -guess
        print(iterations,'iterations occurred. Approximate solution is: ')
        return guess

print(cube_root_bisec(1/-7.5,.00001))





###########################################################
## nth root
## Guess and check
## Modified code for cube root and accounted for imaginary values

def nth_root_guess(x:int,n:int):
    val = x

    if val < 0 and n % 2 == 0: # return non-real answer
        return 'The ' + str(n) + 'th root of ' + str(val) + ' is imaginary'

    for guess in range(abs(val)+1):
        if guess**3 >= abs(val):
            break       # break out of loop if sequence of cubes becomes too large

    if guess**3 != abs(val):
        return 'The ' + str(n) + 'th root of ' + str(val) + ' is not an integer'
    else:
        if val < 0:
            guess = -guess
        return 'The ' + str(n) + 'th root of'  + str(val) + ' is ' + str(guess)