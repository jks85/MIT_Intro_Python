# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : <Julian Simington>
# Collaborators : <>
# Time spent    : <>

import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'

HAND_SIZE = 7

# assigned '*' a point value of 1 at end of letter values

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8,
    'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1,
    'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10, '*':1
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    word = word.lower()     # convert word to lowercase string
    point_score = sum([SCRABBLE_LETTER_VALUES[char] for char in word])  # used list comprehension instead of for loop
    length_score = max(1, 7*len(word)-3*(n-len(word)))

    if '*' in word.lower():
        return (point_score-1)*length_score # score adjustment if word has a '*'
    else:
        return point_score*length_score


#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line
    return print()                              # print an empty line

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    hand={'*':1}
    # num_vowels = int(math.ceil(n / 3)) # number of vowels. commented out and updated for problem 4
    num_vowels = int(math.ceil(n / 3)) - 1 # reduce number of vowels by 1 to allow for a wildcard char, '*'
    for i in range(num_vowels):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels+1, n):
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    
    return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """

    new_hand = hand.copy() # initialize new hand dictionary
    word = word.lower() # convert word to lower case
    word_freq = get_frequency_dict(word) # get frequency of each letter in word
    for char in hand.keys():
        if char in word:
            tiles_left = new_hand[char] - word_freq[char] # compute remaining number of tiles for a letter
            if tiles_left > 0:
                new_hand[char] = tiles_left
            else:
                new_hand.pop(char)
    return new_hand

#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    word_freqs = get_frequency_dict(word.lower()) # get frequencies of lower case characters in word
    if '*' in word.lower():     # check case where word contains a wildcard
        wild_words = [] # initialize empty list to hold possible wildcard words
        wild_index = word.lower().find('*') # get indices for wildcards

        for char in VOWELS:
            # could us str.replace() to replace '*' with vowels instead of string concatenation
            fill_wild_card = word.lower()[:wild_index] + char + word.lower()[wild_index+1:] # create new string
            wild_words.append(fill_wild_card) # creates list of possible wild words

        i = 0   # counter for number of "new words that are in the word list
        for new_word in wild_words:
            if new_word in word_list:
                i += 1
        if i == 0:
            return False
        else:
            return True


    if word.lower() in word_list:   # check if lower case version of word is in wordlist
        for char in word.lower():
            if char not in hand:    # return false if character is not in hand
                return False
            else:
                num_tiles_left = hand[char] - word_freqs[char]  # compute number of letters that would be left
                if num_tiles_left < 0: # return false if too few letters in hand to make the word
                    return False
        return True
    else:
        return False


#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    
    return sum([freq for freq in hand.values()]) # comprehension instead of loop


def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """

    # Keep track of the total score
    total_score = 0 # initialize total score to 0
    # As long as there are still letters left in the hand:
    current_handlen = calculate_handlen(hand) #initiaize hand length
    while current_handlen > 0:
        # Display the hand
        print(display_hand(hand))
        # Ask user for input
        user_action = input('Enter word, or "!!" to indicate that you are finished: ')
        # If the input is two exclamation points:
        if user_action == '!!':
            # End the game (break out of the loop)
            print('Total score:',total_score,'points')
            return total_score

        # Otherwise (the input is not two exclamation points):
        else:

            # If the word is valid:
            if is_valid_word(user_action,hand,word_list):
                # Tell the user how many points the word earned,
                # and the updated total score
                word_score = get_word_score(user_action,current_handlen)    # compute score of word
                total_score += word_score
                print('"'+ user_action + '" earned ' +str(word_score) +' points. Total : ' + str(total_score) + ' points.')

            # Otherwise (the word is not valid):
            else:
                # Reject invalid word (print a message)
                print('That is not a valid word. Please choose another word.')
                return total_score
            # update the user's hand by removing the letters of their inputted word
            hand = update_hand(hand, user_action)
            current_handlen = calculate_handlen(hand)

    # Game is over (user entered '!!' or ran out of letters),
    # so tell user the total score
    print('Ran out of letters. Total score: ' + str(total_score)+ ' points')
    # Return the total score as result of function
    return total_score

#play_hand({'c': 1, 'o': 1, '*': 1, 'w': 1, 's':1, 'z':1, 'y': 2},load_words())

#
# Problem #6: Playing a game
# 


#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """

    if letter.lower() not in string.ascii_lowercase:   # check if selection is a letter
        print('Invalid selection. Please choose a letter.')
        return hand
    if letter.lower() not in hand:
        return hand     # return current hand if submitted letter is not in hand
    # else
    else:
        new_letter = letter.lower() # create copy of letter
        lowercase_letters = string.ascii_lowercase  # get lower case letters (consonants and vowels)
        while new_letter in hand:
            new_letter = random.choice(lowercase_letters)   # assign copy a randomly selected a consonant or vowel

    sub_hand = hand.copy()      # copy hand dict
    sub_hand.update({new_letter:hand[letter]})  # add new letter to dict
    del sub_hand[letter]    # del old letter
    return sub_hand # return new dict


       
    
def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitute option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """

    wordlist = load_words() # load available words
    max_hands = int(input('Input the number of hands you want to play.')) # input number of hands
    hands_played = 0    # initialize number of hands played
    agg_score = 0 # initialize aggregate hand score

    subs_used = False # tracks if substitution option has been used
    replays_used = False # track if replay option has been used

    while hands_played <= max_hands:
        print('----------')
        print('Dealing new hand. . . \n')
        initial_hand = deal_hand(HAND_SIZE)  # deal new hand
        sub_hand = initial_hand # create possible hand to substitute to avoid mutating current hand
        initial_score = 0   # initialize hand_score to 0. will correspond to score for sub or no sub
        replay_score = 0    # initialize replay hand score to 0

        if not subs_used:
            display_hand(initial_hand) # display hand if no sub has occured. will auto display otherwise

        if not subs_used:       # if substitutions have not been used
            ask_sub = input('Do you want to substitute a letter? Type "yes" or "no".')# ask player if they want to sub hand
            if ask_sub.lower() == 'yes':    # if yes (coerce string to lower case)
                sub_letter = input('Type the character in your hand of the letter you would like to substitute.'
                                   ' All copies of the letter will be replaced.')#  input letter
                sub_hand  = substitute_hand(initial_hand,sub_letter.lower())
                subs_used = True  # update substitution state
                initial_score = play_hand(sub_hand, wordlist)  # compute score for sub hand. may be altered by replaying...
            else:
                initial_score = play_hand(initial_hand, wordlist)  # play initial hand if subs available but don't want to sub

        else:
            initial_score = play_hand(initial_hand, wordlist) # play initial hand if no subs available

        hands_played += 1  # update number of hands played
        # cover replay cases before tallying final hand score
        if not replays_used:    # if replays have not been used
            ask_replay = input('Do you want to replay this hand? You may only replay one hand.'
                               'Replay do not count towards total number of hands. Type "yes" or "no".')  # ask player if they want to replay hand
            if ask_replay.lower() == 'yes':  # if yes (coerce string to lower case)
                replays_used = True   # update replay state
                replay_score = play_hand(initial_hand, wordlist)    # compute replay score
        agg_score += max(initial_score,replay_score)    # updated overall score
        print('Total score for this hand:',str(max(initial_score,replay_score))) # print score for this hand
    return print('Total score overall hands:',str(agg_score))   # print overall score



#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
