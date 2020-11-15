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

# try to count how many times each word is used. Need to do some formatting first
# might need to extract all the proper nouns also
novel_text = novel_text.replace('“', '')
novel_text = novel_text.replace('”', '')
novel_text = novel_text.replace(';', '')
novel_text = novel_text.replace(',', '')
novel_text = novel_text.replace('.', '')
novel_text = novel_text.replace('!', '')
novel_text = novel_text.replace('?', '')
novel_text = novel_text.replace(':', '')
novel_text = novel_text.replace('*', '')
novel_text = novel_text.replace('(', '')
novel_text = novel_text.replace(')', '')
novel_text = novel_text.replace("’s", '')
novel_text = novel_text.replace("’ ", ' ')
novel_text = novel_text.replace('—', ' ')
# novel_text = novel_text.replace('-', ' ')
while novel_text.find('  ') != -1:
    novel_text = novel_text.replace('  ',  ' ')
# Text is clean here, put the above in a function.

# From here downwards can go in the counting function. (May have to find character names differently, maybe not)
all_words = nltk.word_tokenize(novel_text)

# delete non-words
# use re to match for strings that contain only number and letters. 

word_freq_distn = nltk.FreqDist(all_words)
unique_words = list(word_freq_distn)

# TODO: Unit test file
#       Write a proper function for cleaning up text
#       Clean up all caps words
#       Extract proper nouns
#       get list of all characters from somewhere.
#       Deal with 'White Whale' phrase
#       Link for understanding 'part-of-speech' tags: https://www.guru99.com/pos-tagging-chunking-nltk.html

