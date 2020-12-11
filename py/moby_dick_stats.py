"""
For loading in the text and extracting some interesting stats and networks.
"""
import os, sys, argparse, re, nltk, shutil
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import networkx as nx
from moby_dick_functions import *

np.set_printoptions(linewidth=shutil.get_terminal_size().columns)

proj_dir = os.path.join(os.environ.get('HOME'), 'Moby_Dick_Stats')
txt_dir = os.path.join(proj_dir, 'txt')
image_dir = os.path.join(proj_dir, 'images')
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
character_list = list(character_count_dict.keys())
character_mentions_frame = getNumMentionsFrame(character_list, num_to_chap_title, moby_dick_text, character_list_with_doubles)
num_characters = len(character_list)
loomings_character_count_dict = getCharacterCounts(loomings_text_1, character_list_with_doubles)
biographical_character_count_dict = getCharacterCounts(getChapterText(moby_dick_text, num_to_chap_title, 'Biographical'), character_list_with_doubles)
tagged_unique_words = posTagWords(unique_words)
unique_nouns = tagged_unique_words[[code in ['NN','NNS'] for code in tagged_unique_words[:,1]],0]
unique_singular_nouns = tagged_unique_words[[code == 'NN' for code in tagged_unique_words[:,1]],0]
unique_proper_nouns = tagged_unique_words[[code in ['NNP','NNPS'] for code in tagged_unique_words[:,1]],0]
nouns_dict = {noun:word_freq_distn.get(noun) for noun in unique_nouns}
singular_nouns_dict = {noun:word_freq_distn.get(noun) for noun in unique_singular_nouns}
sorted_character_count_dict = {key: value for key, value in sorted(character_count_dict.items(), key=lambda item: item[1], reverse=True)}
proper_nouns_dict = {noun:word_freq_distn.get(noun) for noun in unique_proper_nouns}
nouns_title = '20 most common nouns in Moby Dick'
singular_nouns_title = '20 most common singular nouns in Moby Dick'
character_title='Number of mentions of each character in Moby Dick'
proper_nouns_title='20 most common proper nouns in Moby Dick'
plotMostCommonWordsBar(nouns_dict, y_label='Num. occurances', x_label='Word', title=nouns_title)
plotMostCommonWordsBar(singular_nouns_dict, y_label='Num. occurances', x_label='Word', title=singular_nouns_title)
plotMostCommonWordsBar(sorted_character_count_dict, num_words=len(character_count_dict), y_label='Num. occurances', x_label='Character', title=character_title)
plotMostCommonWordsBar(proper_nouns_dict, num_words=len(character_count_dict), y_label='Num. occurances', x_label='Proper noun', title=proper_nouns_dict)

chapter_mentions = getCharacterCoMentions(character_list, num_to_chap_title, moby_dick_text, character_list_with_doubles)
normed_chapter_mentions, total_mentions = getNormedCharacterCoMentions(character_list, num_to_chap_title, moby_dick_text, character_list_with_doubles)
sorted_inds = np.argsort(total_mentions)
sorted_chapter_mentions = chapter_mentions[:,sorted_inds[::-1]]; sorted_chapter_mentions = sorted_chapter_mentions[sorted_inds[::-1],:]
sorted_normed_chapter_mentions = normed_chapter_mentions[:,sorted_inds[::-1]]; sorted_normed_chapter_mentions = sorted_normed_chapter_mentions[sorted_inds[::-1],:]
sorted_character_list = np.array(character_list)[sorted_inds[::-1]]
# show the matrix
plotChapterCoMentions(sorted_chapter_mentions, sorted_character_list, title='Number of chapters in which both characters of each pair are mentioned')
plotChapterCoMentions(sorted_normed_chapter_mentions, sorted_character_list, title='Normed chapter co-mentions')
plt.close('all')

sorted_character_edges = np.nonzero(np.triu(sorted_normed_chapter_mentions))
sorted_character_edges_list = list(zip(sorted_character_edges[0], sorted_character_edges[1]))

character_connections = nx.Graph()
edge_weights = []
for source, target in sorted_character_edges_list:
    character_connections.add_edge(sorted_character_list[source], sorted_character_list[target], weight=sorted_normed_chapter_mentions[source, target])
    edge_weights.append(sorted_normed_chapter_mentions[source, target])

nx.draw_circular(character_connections, with_labels=True, node_size=300, node_color='white', edge_cmap=cm.Blues, edge_color=edge_weights, font_weight='bold')
plt.show(block=False)
# positions = nx.circular_layout(character_connections
# nx.draw_networkx_nodes(character_connections, positions, alpha=0.35, node_size=100)
# nx.draw_networkx_edges(character_connections, positions, edge_cmap=cm.Blues, edge_color=edge_weights)
# nx.draw_networkx_labels(character_connections, positions)
# TODO: Apply Spectral detection to the normed chapter comentions matrix
#       Unit test file
#       Extract proper nouns
#       Link for understanding 'part-of-speech' tags: https://www.guru99.com/pos-tagging-chunking-nltk.html
