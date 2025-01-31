# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

# import feedparser
import myfeedparser
import datefinder
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz

# feedparser was removed. changes to the 'collections' module
# caused the RSS feed not to populate for the filtering section (problems 9-12)
# myfeedparser was added from Andre Soeiro's github (https://github.com/afsoeiro)
# the original process() helper function has been commented out below

#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================
def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """


    entries = myfeedparser.fetch_url(url)
    ret = []
    # The following loop is now using information from the feedparser I developed
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.pubdate)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
        except ValueError:
            matches = datefinder.find_dates(pubdate)

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

# def process(url):
#     """
#     Fetches news items from the rss url and parses them.
#     Returns a list of NewsStory-s.
#     """
#     feed = feedparser.parse(url)
#     entries = feed.entries
#     ret = []
#     for entry in entries:
#         guid = entry.guid
#         title = translate_html(entry.title)
#         link = entry.link
#         description = translate_html(entry.description)
#         pubdate = translate_html(entry.published)
# 
#         try:
#             pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
#             pubdate.replace(tzinfo=pytz.timezone("GMT"))
#           #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
#           #  pubdate.replace(tzinfo=None)
#         except ValueError:
#             pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")
# 
#         newsStory = NewsStory(guid, title, description, link, pubdate)
#         ret.append(newsStory)
#     return ret

#======================
# Data structure design
#======================

# Problem 1

class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_link(self):
        return self.link

    def get_pubdate(self):
        return self.pubdate


#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2

class PhraseTrigger(Trigger):    # create phrase trigger subclass
    '''
    PhraseTrigger is a subclass of Trigger. It contains a method to check
    whether a phrase exists within string. This class has no getter method since
    it is an abstract class, so we will not create instances of it.

    A "phrase" is one or more words separated by a single space between the words. You may
    assume that a phrase does not contain any punctuation.
    '''
    def __init__(self,phrase):
        self.phrase = phrase

    def is_phrase_in(self,text):
        '''
        Checks whether text contains the phrase. Matching phrases are not case-sensitive.
        '''

        # clean text string (remove punctuation and spaces. make text lower case)
        # could be useful to make this a separate method
        for char in string.punctuation:     # replace punctuation with spaces
            text = text.replace(char, ' ')

        text_lower = str.lower(text)  # convert text to lower case
        text_list = text_lower.split(' ') # split text on spaces. the resulting list contains empty strings ''
                                          # if the text contains consecutive spaces

        text_clean = []     # empty list that will contain text with spaces removed and no punctuation
        for val in text_list:
            if val != '':
                text_clean.append(val) # append string to list if it is not empty
                # text_clean is a list of strings in the original text with punctuation and spaces removed

        # check if trigger phrase is in the text string
        phrase_lower = self.phrase.lower()  # convert phrase to lower case for matching
        phrase_list = phrase_lower.split(' ')    # split phrase into list containing strings
        phrase_length = len(phrase_list)        # length of phrase. will use for iteration
        text_length = len(text_clean)

        for i in range(text_length): # iterate over clean text string.
            # looping using integer indices instead of iterating over list to avoid index errors
            if i > text_length - phrase_length:
                return False    # returns false if phrase is longer than remaining text string
            if text_clean[i] == phrase_list[0]: # if element matches first element of phrase
                match_list = []     # create empty list to hold possible matches
                match_count = 1      # set current match count
                for j in range(i, i +phrase_length):
                    match_list.append(text_clean[j])    # create list containing strings to match
                for k in range(1, phrase_length):   # check if remaining elements of text string match phrase
                    if match_list[k] != phrase_list[k]:
                        break   # break out of loop if strings don't match
                    else:
                        match_count += 1
                if match_count == phrase_length:
                    return True     # return true if all strings match

        return False    # if loop ends (no match was found)


# Problem 3
class TitleTrigger(PhraseTrigger):
    """
    Subclass of PhraseTrigger. It has one attribute, a method evaluate()
    which checks for a phrase in the title of  a NewsStory object.

    Special print method prints the trigger text.
    """
    # I don't think an init method or getters setters are needed. This class can use the
    # PhaseTrigger init method and call is_phrase_in()

    def evaluate(self, story):  # note that story is  NewsStory object
       return self.is_phrase_in(story.title)


# Problem 4

class DescriptionTrigger(PhraseTrigger):
    """
    Subclass of PhraseTrigger. It has one attribute, a method evaluate()
    which checks for a phrase in the description of  a NewsStory object.

     """
    def evaluate(self, story):
        return self.is_phrase_in(story.description)


# TIME TRIGGERS

# Problem 5
#
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.

class TimeTrigger(Trigger):
    """
    Subclass of Trigger. Has one attribute, a date and time in EST
    formatted as a datetime object.

    """

    def __init__(self,date_time):
        self.date_time_str = date_time  # date_time text as a string for printing
        date_time = datetime.strptime(date_time, '%d %b %Y %H:%M:%S') # convert to date_time class
        self.date_time = date_time.replace(tzinfo=pytz.timezone("EST")) # set time zone to eastern


# Problem 6

class BeforeTrigger(TimeTrigger):

    """
    BeforeTrigger is a trigger that checks whether a story is published before a certain time.

    """

    def evaluate(self, story):
        return story.pubdate < self.date_time # return True if publish time is earlier than time trigger


class AfterTrigger(TimeTrigger):

    """
    AfterTrigger is a trigger that checks whether a story is published after a certain time.

    """
    def evaluate(self, story):
        return story.pubdate > self.date_time # return True if publish time is later than time trigger


# COMPOSITE TRIGGERS

# Problem 7

class NotTrigger(Trigger):

    """
    NotTrigger fires when a trigger is not true. Note that it is not
    a PhraseTrigger subclass. It is written to preserve the polymorphism
    of the evaluate() method.

    """
    def __init__(self, trigger):
        self.trigger = trigger


    def evaluate(self, story):
        return not self.trigger.evaluate(story)


# Problem 8

class AndTrigger(Trigger):

    """
    AndTrigger is a trigger that fires when two triggers are both true.
    Note that it is not a PhraseTrigger subclass. It is written to preserve
    the polymorphism of the evaluate() method.
    """

    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2

    def evaluate(self, story):
        return self.trigger1.evaluate(story) and self.trigger2.evaluate(story)


# Problem 9

class OrTrigger(Trigger):

    """
    OrTrigger is a trigger that fires when at least one of two trig is detected.
    Note that it is no a PhraseTrigger subclass. It is written to preserve the polymorphism
    of the evaluate() method.
    """

    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2

    def evaluate(self, story):
        return self.trigger1.evaluate(story) or self.trigger2.evaluate(story)


#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """

    filtered_stories = []   # initialize list to hold stories
    for story in stories:   # iterate over NewsStory-s
        for trigger in triggerlist:  # iterate over triggers
            if trigger.evaluate(story):
                filtered_stories.append(trigger)    # add story to list if trigger is true
                break                               # break out of loop and move to next story

    return filtered_stories         # return list of filtered stories



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)


    # line is the list of lines that you need to parse and for which you need
    # to build triggers

    trigger_list = []
    trigger_dict = dict()       # dict to hold key:value pair for trigger--  name:(subclass, arg1,arg2)
    for text in lines:
        trig_parse = text.split(',')    # split string

        # if block below creates a dictionary
        if trig_parse[0] != 'ADD':      # check for lines not adding triggers
            i = 1                       # index to track length of trig info list. starts at 1 since index 0 will be dict key
            dict_key_tup = tuple()      # create empty tuple
            while i < len(trig_parse):  # loop over trigger info
                dict_key_tup += (trig_parse[i],) # add all but first element to tuple key

                i += 1                  # increment index
            trigger_dict[trig_parse[0]] = dict_key_tup # create key:val pair of trigger-- name:(subclass, constructor arg)
            # dict value is a tuple. index 0 is trigger subclass. remaining indices are constructor arguments

        # else block creates triggers as indicated and adds them to trigger list
        else:               # assumes trigger definitions precede add lines so that trigger_dict is not empty

            def create_trigger(trigger_name):     # helper function that creates a non-composite trigger instance
                trig_subclass = trigger_dict[trigger_name][0]
                assert trig_subclass in ['TITLE','DESCRIPTION','AFTER','BEFORE']    # require non-composite subclass
                trig_arg = trigger_dict[trigger_name][1]        #  constructor argument of trigger (e.g. phrase, date, etc)
                if trig_subclass == 'TITLE':
                    created_trig = TitleTrigger(trig_arg)  # create title trigger and append to list
                    #trigger_list.append('TitleTrigger(trig_arg)')

                elif trig_subclass == 'DESCRIPTION':
                    created_trig = DescriptionTrigger(trig_arg)   # trig arg is a phrase

                elif trig_subclass == 'AFTER':
                    created_trig = AfterTrigger(trig_arg)     # trig arg is a date_time string

                else:
                    created_trig = BeforeTrigger(trig_arg)    # trig arg is a date_time string

                return created_trig


            trig2_add = trig_parse[1:]     # subset list of trigger names to add
            for new_trig in trig2_add:
                trig_subclass = trigger_dict[new_trig][0]   # subclass of trigger
                if trig_subclass in ['TITLE','DESCRIPTION','AFTER','BEFORE']:   # check if subclass is non-composite
                    trigger_list.append(create_trigger(new_trig))       # create trigger and append to list

                elif trig_subclass == 'NOT':  # not trigger
                    trig_und_name = trigger_dict[new_trig][1]  # underlying non-composite trigger name
                    trig_und = create_trigger(trig_und_name) # create underlying trigger
                    trigger_list.append(NotTrigger(trig_und)) # create trigger. assumes non-composite underlying trigger


                elif trigger_dict[new_trig][0] == 'AND':  # and trigger
                    trig_und_name1 = trigger_dict[new_trig][1]  # underlying non-composite trigger #1 name
                    trig_und_name2 = trigger_dict[new_trig][2]  # underlying non-composite trigger #2 name
                    trig_und1 = create_trigger(trig_und_name1)  # create underlying trigger #1
                    trig_und2 = create_trigger(trig_und_name2)  # create underlying trigger #2
                    trigger_list.append(AndTrigger(trig_und1, trig_und2))  # create trigger. assumes non-composite underlying trigger

                else:                                       # or trigger
                    trig_und_name1 = trigger_dict[new_trig][1]  # underlying non-composite trigger #1 name
                    trig_und_name2 = trigger_dict[new_trig][2]  # underlying non-composite trigger #2 name
                    trig_und1 = create_trigger(trig_und_name1)  # create underlying trigger #1
                    trig_und2 = create_trigger(trig_und_name2)  # create underlying trigger #2
                    trigger_list.append(OrTrigger(trig_und1, trig_und2))  # create trigger. assumes non-composite underlying trigger

    #print(lines) # for now, print it so you see what it contains!
    #print(trigger_list)
    return trigger_list



SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        triggerlist = read_trigger_config('triggers.txt')
        for trig in triggerlist:
            print(triggerlist)
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

