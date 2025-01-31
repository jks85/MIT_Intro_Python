# Problem Set 4C
# Name: <jks85>
# Collaborators:
# Time Spent: x:xx

import string
from ps4a import get_permutations

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(load_words(WORDLIST_FILENAME), 'bat') #returns
    True
    >>> is_word(load_words(WORDLIST_FILENAME), 'asdf') #returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

# you may find these constants helpful
VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'

class SubMessage(object):
    def __init__(self, text):
        '''
        Initializes a SubMessage object
                
        text (string): the message's text

        A SubMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)
    
    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        wordlist_copy = self.valid_words[:]
        return wordlist_copy
                
    def build_transpose_dict(self, vowels_permutation):
        '''
        vowels_permutation (string): a string containing a permutation of vowels (a, e, i, o, u)
        
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to an
        uppercase and lowercase letter, respectively. Vowels are shuffled 
        according to vowels_permutation. The first letter in vowels_permutation 
        corresponds to a, the second to e, and so on in the order a, e, i, o, u.
        The consonants remain the same. The dictionary should have 52 
        keys of all the uppercase letters and all the lowercase letters.

        Example: When input "eaiuo":
        Mapping is a->e, e->a, i->i, o->u, u->o
        and "Hello World!" maps to "Hallu Wurld!"

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''


        vowel_map_dict = {VOWELS_LOWER[i]:vowels_permutation[i] for i in range(len(VOWELS_LOWER))} # dict mapping vowels to permutation
        transp_dict = dict()    # empty dict to hold new dict
        for letter in string.ascii_lowercase: # iterate over lower case letters
            if letter in CONSONANTS_LOWER:
                transp_dict[letter] = letter    # map consonant to itself
            elif letter in VOWELS_LOWER:
                transp_dict[letter] = vowel_map_dict[letter]    # map vowels using permutation argument
        transp_dict_copy = transp_dict.copy()   # create copy of dict for iteration purposes
        for char in transp_dict_copy.keys():
            transp_dict[char.upper()] = transp_dict[char].upper()   # create map for uppercase characters
        return transp_dict


    
    def apply_transpose(self, transpose_dict):
        '''
        transpose_dict (dict): a transpose dictionary
        
        Returns: an encrypted version of the message text, based 
        on the dictionary
        '''

        msg = self.message_text  # part of SubMessage class so don't need to use getter
        code_msg = ''            # empty string to create encrypted message
        for char in msg:
            if char.lower() not in string.ascii_lowercase:
                code_msg += char    # add character to new message if it is not an ascii character
            else:
                code_msg += transpose_dict[char]    # add mapped character to new message if it is an ascii character
        return code_msg                 # note code message is a string


class EncryptedSubMessage(SubMessage):
    def __init__(self, text):
        '''
        Initializes an EncryptedSubMessage object

        text (string): the encrypted message text

        An EncryptedSubMessage object inherits from SubMessage and has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        SubMessage.__init__(self, text) # initialize using SubMessage class. No data attributes

    def decrypt_message(self):
        '''
        Attempt to decrypt the encrypted message 
        
        Idea is to go through each permutation of the vowels and test it
        on the encrypted message. For each permutation, check how many
        words in the decrypted text are valid English words, and return
        the decrypted message with the most English words.
        
        If no good permutations are found (i.e. no permutations result in 
        at least 1 valid word), return the original string. If there are
        multiple permutations that yield the maximum number of words, return any
        one of them.

        Returns: the best decrypted message    
        
        Hint: use your function from Part 4A
        '''
        all_vowel_perms = get_permutations(VOWELS_LOWER)  # get all permutations of lower case vowels
        max_words = 0                                     # track number of "real" words. initialize to 0
        best_msg = self.get_message_text()                # set best message tracker. initialize to given text
        legit_words = self.get_valid_words()              # set valid word list
        for perm in all_vowel_perms:                      # iterate over vowel permutations
        #for perm in ['aeiou','eaiou']:
            perm_dict = self.build_transpose_dict(perm)   # create dictionary for vowel permutation
            perm_msg = self.apply_transpose(perm_dict)    # apply permutation mapping (really unmapping/inversion)
            perm_words = list(perm_msg.split(' '))        # create list of words for mapped string
            word_count = 0                                # set counter for real words in this permutation
            for word in perm_words:
                #print(perm_msg, word, legit_words)
                #print(is_word(legit_words, word))
                if is_word(legit_words, word):            # counts number of real words in decryption
                    word_count += 1

            if word_count > max_words:
                max_words = word_count
                best_msg = perm_msg         # updates current decryption to best message if its word count > max count

        return best_msg

    


if __name__ == '__main__':

    #check_msg = EncryptedSubMessage('Hello World')
    #print(get_permutations(VOWELS_LOWER)[99])
    #print(check_msg.build_transpose_dict(get_permutations(VOWELS_LOWER)[99]))
    #print(check_msg.decrypt_message())
    #print('World' in check_msg.get_valid_words())
    #print(is_word(check_msg.get_valid_words(),'afar'))

    # Example test case
    print('Example Test Case')
    message = SubMessage("Hello World!")
    permutation = "eaiuo"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Hallu Wurld!")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())
    print(' ')
    #
    #TODO: WRITE YOUR TEST CASES HERE


    # Test Case 1
    print('Test Case 1')
    message1 = SubMessage("I'm him. I'm like that") # create submessage instance
    permutation1 = 'oiuae'  # set permutation to use for encryption
    enc_dict1 = message1.build_transpose_dict(permutation1) # create permutation dictionary
    print("Original message:",message1.get_message_text(), "Permutation:",permutation1) # original message
    print("Expected encryption:", "U'm hum. U'm luki thot")     # print expected encryption
    print("Actual message:", message1.apply_transpose(enc_dict1))   # print actual encryption
    encryption1 = message1.apply_transpose(enc_dict1)      # encrypted message
    enc_message1 = EncryptedSubMessage(encryption1)     # create encrypted message instance
    print("Decrypted message:",enc_message1.decrypt_message())          # decrypt encrypted message
    print(' ')


    # Test Case 2
    print('Test Case 2')
    message2 = SubMessage("Chef Curry with the pot") # create submessage instance
    permutation2 = 'eauio'  # set permutation to use for encryption
    enc_dict2 = message1.build_transpose_dict(permutation2) # create permutation dictionary
    print("Original message:",message2.get_message_text(), "Permutation:",permutation1) # original message
    print("Expected encryption:", "Chaf Corry wuth tha pit")     # print expected encryption
    print("Actual message:", message2.apply_transpose(enc_dict2))   # print actual encryption
    encryption2 = message2.apply_transpose(enc_dict2)      # encrypted message
    enc_message2 = EncryptedSubMessage(encryption2)     # create encrypted message instance
    print("Decrypted message:",enc_message2.decrypt_message())                   # decrypt encrypted message
