# Problem Set 2, hangman.py
# Name: Julian Simington
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"

# Note: I only completed problems 1-3. The baseline version of the games runs
# and meets the required specs but does not provide hints (problem 4).

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    # could use 'in' operator but practicing nested loops
    matches = 0 # initialize number of matches
    for char in secret_word:
        matches = 0  # initialize number of matches
        for guess in letters_guessed:
            if guess == char:
                matches += 1
        if matches == 0:
            return False
    return True





def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    # using 'in' operator here as nested loop seems unproductive
    guessed_word = '' # initialize empty string
    for char in secret_word:
        if char in letters_guessed:
            guessed_word += char
        else:
            guessed_word += '_'
    return guessed_word

print(get_guessed_word('ready',[]))


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    # using 'in' again here
    available_letters = '' # initialize empty string
    for char in string.ascii_lowercase:
        if char not in letters_guessed:
            available_letters += char
    return available_letters


    

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    wordlist = load_words() # loast wordlist
    secret_word = choose_word(wordlist) # select word to guess
    letters_guessed = [] # initialize list of guesses to empty
    available_letters = get_available_letters(letters_guessed) # set initial list letters to choose
    remaining_guess = 6 # set initial number of guesses
    remaining_warnings = 3 # set number of initial warnings
    print('Welcome to the game Hangman!')
    print('I am thinking of a word that is ',str(len(secret_word)),' letters long.')
    print('Guess a letter when prompted. Your guess must be a lowercase letter. '
          'Type a letter then press Enter.')
    print('You will receive a warning each time you enter an invalid input. '
          'After 3 warnings you lose a turn')
    print('---------------')

    unique_letters = len({char for char in secret_word})# compute unique number of letters in word for score

    while not is_word_guessed(secret_word,letters_guessed):

        print('You have ', str(remaining_guess), ' guesses left.') # instructions
        print('Available letters: ', str(available_letters))
        print('\n')
        current_guess = str.lower(input('Please guess a lowercase letter: '))     # user input to guess letter

        # check valid input
        if current_guess not in string.ascii_lowercase:
            remaining_warnings -= 1                     # remove a warning if invalid
            if remaining_warnings == 0:         # remove a guess if no remaining warnings
                remaining_guess -= 1
                if remaining_guess == 0:
                    return print('Game Over. The word was ', secret_word)
                else:
                    print('Penalty! You have ',str(remaining_guess),' guesses left.')
                    print('---------------')
                    remaining_warnings = 3          # reset warnings counter
            else:
                print('---------------')
                print('Warning Please choose a lower case letter!') # remind user of valid inputs
                print('You have ', str(remaining_warnings),' warnings left before losing a guess.')
                print('You have ', str(remaining_guess), ' guesses left.')

        else:
            if current_guess in letters_guessed:    # penalties for repeat guesses
                print('---------------')
                print('Warning! You already guessed that letter.')
                remaining_warnings -= 1  # remove a warning if invalid
                if remaining_warnings == 0:  # remove a guess if no remaining warnings
                    remaining_guess -= 1
                    if remaining_guess == 0:
                        return print('Game Over. The word was ', secret_word)
                    else:
                        print('Penalty! You have ', str(remaining_guess), ' guesses left.')
                        remaining_warnings = 3  # reset warnings counter
                else:
                    print('---------------')
                    print('Warning Please choose a new lowercase letter!')  # remind user of valid inputs
                    print('You have ', str(remaining_warnings), ' warnings left before losing a guess.')
                    print('You have ', str(remaining_guess), ' guesses left.')


        # check user input against word and update game state
        letters_guessed.append(current_guess)  # updated guessed letters
        available_letters = get_available_letters(letters_guessed) # update available letters
        #print(letters_guessed)
        if current_guess in secret_word:
            print('---------------')
            print('Good guess: ',get_guessed_word(secret_word,letters_guessed)) # show current word

        else:     #check for vowels
            print('---------------')
            print('Oops! That letter is not in my word: ',get_guessed_word(secret_word,letters_guessed))

            if current_guess in ['a', 'e', 'i', 'o', 'u']: # check for vowels
                remaining_guess -= 2       # remove 2 guesses for incorrect vowel
                if remaining_guess <= 0:   # check remaining guesses and for end of game
                    return print('Game Over. The word was ', secret_word)

            else:
                remaining_guess -=1     # remove 1 guess for incorrect consonant
                if remaining_guess == 0:   # check remaining guesses and for end of game
                    return print('Game Over. The word was ', secret_word)

    score = remaining_guess*unique_letters
    return print('Congratulations. You correctly guessed the secret word-- ',
                 get_guessed_word(secret_word, letters_guessed),' .',
                 'You scored',score,'points.')






# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    pass



def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    pass



def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    pass



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    #pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    secret_word = choose_word(wordlist)
    hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    #secret_word = choose_word(wordlist)
    #hangman_with_hints(secret_word)

