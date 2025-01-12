# Problem Set 4B
# Name: <jks85>
# Collaborators:
# Time Spent: x:xx

import string
from string import ascii_lowercase


### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    #print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    #print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> test_list = load_words(WORDLIST_FILENAME) ; pass
    >>> is_word(test_list, 'bat')
    True
    >>> test_list = load_words(WORDLIST_FILENAME) ; pass
    >>> is_word(test_list, 'asdf')
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
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
        wordlist_copy = self.valid_words[:]  # create copy of word list via slicing
        return wordlist_copy

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''

        standard_dict = {a:b for (a,b) in enumerate(string.ascii_lowercase)} # dict mapping for 0 thru 25 to 'a' through 'z'
        lowercase_map_dict = {standard_dict[i]:standard_dict[(i + shift) % 26] # map old character to new character based on shift
                for i in range(len(string.ascii_lowercase))}
        new_dict = lowercase_map_dict.copy()    # copy dict to be used to create new dict that includes uppercase shifts
        for char in lowercase_map_dict.keys():  # iterate over keys of lowercase map_dict
            new_dict[char.upper()] = new_dict[char].upper() # convert shift to upper case and add to new dict. note lower/upper are mapped to corresponding values
        return new_dict


    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        shift_dict = self.build_shift_dict(shift) # dict containing shifted letter mapping
        new_str = str() # create empty string to hold new message
        message = self.get_message_text()   # unsure if getter method is necessary here stylistically
        for char in message:
            if char.lower() not in string.ascii_lowercase: # if character is non ascii (this covers upper and lower case)
                new_str += char # add character to new message
            else: # if character is ascii
                new_str += shift_dict[char] # shift character using dict and add new character to new message
        return new_str


class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object        
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        Message.__init__(self, text)
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(self.shift)    # unsure if self. is needed in argument
        self.message_text_encrypted = self.apply_shift(self.shift)

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        return self.shift

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class
        
        Returns: a COPY of self.encryption_dict
        '''
        encryption_dict_copy = self.encryption_dict.copy()   # copy encryption dict
        return encryption_dict_copy

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift.        
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        self.shift = shift  # change shift value
        self.__init__(self.get_message_text(),self.shift) # use init method to update dependencies


class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        Message.__init__(self, text)

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create 
        the maximum number of valid words, you may choose any of those shifts 
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        max_words = 0                                               # set counter for max words found
        best_shift = 0                                              # set variable to track best shift
        best_msg = ''                                               # set variable to track best message
        legit_words = self.get_valid_words()                        # load valid words

        for shift_val in range(26):                                 # iterate over possible shift values
            current_msg = PlaintextMessage(self.message_text, shift_val)    # note: this calls load_words each iteration which is problematic
            encryption = current_msg.get_message_text_encrypted()   # assign new variable for encrypted message
            encrypted_words = list(encryption.split(' '))           # create list of encrypted words
            word_count = 0                                          # set word count to 0 in encrypted message


            for word in encrypted_words:                            # iterate over words in encrypted message
                if is_word(legit_words, word):
                    word_count += 1                                 # increment word count for each word found
            if word_count > max_words:                              # if current word count is higher than previous max
                max_words = word_count                              # update max word count
                best_shift = shift_val                              # update best shift
                best_msg = current_msg.get_message_text_encrypted() # update best message

        return (best_shift, best_msg)

if __name__ == '__main__':

#    #Example test case (PlaintextMessage)
#    plaintext = PlaintextMessage('hello', 2)
#    print('Expected Output: jgnnq')
#    print('Actual Output:', plaintext.get_message_text_encrypted())
#
#    #Example test case (CiphertextMessage)
#    ciphertext = CiphertextMessage('jgnnq')
#    print('Expected Output:', (24, 'hello'))
#    print('Actual Output:', ciphertext.decrypt_message())

    #TODO: WRITE YOUR TEST CASES HERE

#   # Example test case (PlaintextMessage)
#   plaintext1 = PlaintextMessage("I'm like that",2)
#   print('Expected Output: "I'm like that"')
#   print('Actual Output:', plaintext1.get_message_text_encrypted())
#
#    #Example test case (CiphertextMessage)
#    ciphertext1 = CiphertextMessage("K'o nkmg vjcv")
#    print('Expected Output:', (24, "I'm like that"))
#    print('Actual Output:', ciphertext.decrypt_message())
    #TODO: best shift value and unencrypted story

    encrypted_story = get_story_string()    # convert story to string
    # print(encrypted_story)
    cipher_msg = CiphertextMessage(encrypted_story) # create cipher text message object
    print('Actual Output:', cipher_msg.decrypt_message())   # decrypt and print message

#   Note: I suppressed the print messages in load_words()
#   Decrypted message below. Best shift is 12


#   'Jack Florey is a mythical character created on the spur of a moment to help cover an insufficiently planned hack.
#   He has been registered for classes at MIT twice before, but has reportedly never passed aclass. It has been the
#   tradition of the residents of East Campus to become Jack Florey for a few nights each year to educate incoming
#   students in the ways, means, and ethics of hacking.')