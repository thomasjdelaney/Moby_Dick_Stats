"""
For loading in the text and extracting some interesting stats and networks.
"""
import os, sys, argparse, re, nltk
import datetime as dt
import numpy as np
from moby_dick_functions import * 

proj_dir = os.path.join(os.environ.get('HOME'), 'Moby_Dick_Stats')
txt_dir = os.path.join(proj_dir, 'txt')
moby_dick_txt_file = os.path.join(txt_dir, 'moby_dick.txt')

with open(moby_dick_txt_file, 'r') as f:
    moby_dick_text = f.read()

num_to_chap_title = extractChapterTitleDict(moby_dick_text)
all_section_titles = getAllSectionTitles(moby_dick_text)

# these are unit tests
loomings_text_1 = getChapterText(moby_dick_text, num_to_chap_title, 1)
loomings_text_2 = getChapterText(moby_dick_text, num_to_chap_title, 'Loomings')
chapter_2_text = getChapterText(moby_dick_text, num_to_chap_title, 2)
chapter_135_text = getChapterText(moby_dick_text, num_to_chap_title, 135)
contents_text = getSpecialSectionText(moby_dick_text, 'CONTENTS')
epilogue_text = getSpecialSectionText(moby_dick_text, 'Epilogue')
novel_text = getNovelText(moby_dick_text)

def cleanText(text_to_clean):
    """
    For taking in some text and cleaning it up, i.e. removing parenthesis, question marks and so on.
    Arguments:  text_to_clean
    Returns:    the cleaned up text, all in one string
    """
    substrs_to_remove = ['“','”',';',',','.','!','?',':','*','(',')',"’s"]
    substrs_to_replace = ["’ ", '—']
    for to_remove in substrs_to_remove:
        text_to_clean = text_to_clean.replace(to_remove, '')
    for to_replace in substrs_to_replace:
        text_to_clean = text_to_clean.replace(to_replace, ' ')
    while text_to_clean.find('  ') != -1:
        text_to_clean = text_to_clean.replace('  ',  ' ')
    return text_to_clean

novel_text = cleanText(novel_text)

# From here downwards can go in the counting function. (May have to find character names differently, maybe not)
all_words = nltk.word_tokenize(novel_text)
all_words = [word for word in all_words if re.search('^[a-zA-Z0-9]*$',  word)]
word_freq_distn = nltk.FreqDist(all_words)
# deal with capitalized words here

unique_words = list(word_freq_distn)
tagged_unique_words = nltk.pos_tag(unique_words)

# TODO: Unit test file
#       Clean up all caps words
#       Extract proper nouns
#       Deal with 'White Whale' phrase
#       Link for understanding 'part-of-speech' tags: https://www.guru99.com/pos-tagging-chunking-nltk.html

