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
character_list_file = os.path.join(txt_dir, 'character_list.txt')

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
# novel_text = cleanText(novel_text)
word_freq_distn = getWordFreqDistn(novel_text)
unique_words = list(word_freq_distn)
character_list_with_doubles = getCharacterList(character_list_file) # contains double names
character_count_dict = getCharacterCounts(novel_text, character_list_with_doubles)
loomings_character_count_dict = getCharacterCounts(loomings_text_1, character_list_with_doubles)
biographical_character_count_dict = getCharacterCounts(getChapterText(moby_dick_text, num_to_chap_title, 'Biographical'), character_list_with_doubles)
tagged_unique_words = posTagWords(unique_words)
unique_nouns = tagged_unique_words[[code in ['NN','NNS'] for code in tagged_unique_words[:,1]],0]


# pos_tag_meaning_dict = getPOSTagMeaningDict()
# TODO: Unit test file
#       Extract proper nouns
#       Link for understanding 'part-of-speech' tags: https://www.guru99.com/pos-tagging-chunking-nltk.html
