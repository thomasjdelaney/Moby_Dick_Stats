"""
For loading in the text and extracting some interesting stats and networks.
"""
import os, sys, argparse, re, nltk
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
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

# make a bar chart of the top n most used words (already sorted)
num_words = 20
noun_freq_distn = {noun:word_freq_distn.get(noun) for noun in unique_nouns}
fig,ax = plt.subplots(nrows=1, ncols=1)
ax.bar(x=range(num_words), height=list(noun_freq_distn.values())[:num_words])
ax.grid(axis='y', alpha=0.25)
ax.set_xlim(-1,num_words)
ax.set_xticks(range(num_words))
ax.set_xticklabels(list(noun_freq_distn.keys())[:num_words])
ax.tick_params(axis='both', labelsize='large')
[tick.set_rotation(45) for tick in ax.get_xticklabels()]
ax.set_ylabel('Num. occurances', fontsize='x-large')
ax.set_xlabel('Word', fontsize='x-large')
[ax.spines[s].set_visible(False) for s in ['top', 'right']]
ax.set_title(str(num_words) + ' most common nouns in Moby Dick', fontsize='large')
plt.tight_layout()

# pos_tag_meaning_dict = getPOSTagMeaningDict()
# TODO: Unit test file
#       Extract proper nouns
#       Link for understanding 'part-of-speech' tags: https://www.guru99.com/pos-tagging-chunking-nltk.html
