"""
For loading in the text and extracting some interesting stats and networks.
"""
import os, sys, argparse
import datetime as dt
import numpy as np
from moby_dick_functions import * 

proj_dir = os.path.join(os.environ.get('HOME'), 'Moby_Dick_Stats')
txt_dir = os.path.join(proj_dir, 'txt')
moby_dick_txt_file = os.path.join(txt_dir, 'moby_dick.txt')

with open(moby_dick_txt_file, 'r') as f:
    moby_dick_text = f.read()

num_to_chap_title = extractChapterTitleDict(moby_dick_text)

def getChapterText(moby_dick_text, num_to_chap_title, chapter_number_or_name, num_chapters=135):
    """
    For geting the text of the given chapter.
    Arguments:  moby_dick_text, the text
                num_to_chap_title, dictionary
                chapter_number_or_name, int, or string
    Returns:    the text of the given chapter, in a big string
    """
    # TODO Need something here for special chapters 'Extracts, Epilogue, etc'
    if int == type(chapter_number_or_name):
        chapter_number = chapter_number_or_name
    elif str == type(chapter_number_or_name):
        chapter_number = list(num_to_chap_title.values()).index(chapter_number_or_name) + 1
    else:
        print(dt.datetime.now().isoformat() + ' ERROR: ' + 'Unrecognised chapter identifier type! Exiting!')
        exit(1)
    chapter_title = num_to_chap_title.get(chapter_number)
    next_chapter_title = num_to_chap_title.get(chapter_number+1)
    chapter_start = findMultiple(moby_dick_text, 'CHAPTER ' + str(chapter_number) + '. ' + chapter_title)[1]
    chapter_end = findMultiple(moby_dick_text, 'CHAPTER ' + str(chapter_number+1) + '. ' + next_chapter_title)[1]
    # TODO need something to deal with the last chapter.
    chapter_text = moby_dick_text[chapter_start:chapter_end].strip()
    return chapter_text

all_section_titles = getAllSectionTitles(moby_dick_text)
loomings_text_1 = getChapterText(moby_dick_text, num_to_chap_title, 1)
loomings_text_2 = getChapterText(moby_dick_text, num_to_chap_title, 'Loomings')
chapter_2_text = getChapterText(moby_dick_text, num_to_chap_title, 2)

# TODO: Unit test file
#       Function to trim text of anything not in the story
