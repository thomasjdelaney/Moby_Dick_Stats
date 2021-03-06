"""
Functions and globals that are useful for the project.
"""
import nltk, re
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import networkx as nx
from itertools import combinations

def findMultiple(string, substring):
    """
    For finding the starting indices of substring in string.
    Arguments:  string, The string to search
                substring, the string to search for
    Returns:    the starting indices of substring within string, or empty list if not found
    """
    starting_inds = [string.find(substring)]
    while starting_inds[-1] != -1:
        next_starting_ind = string.find(substring, starting_inds[-1]+1)
        starting_inds.append(next_starting_ind)
    return starting_inds[:-1]

def extractChapterTitleDict(moby_dick_text):
    """
    For extracting a dictionary of chapter number => chapter title
    Arguments:  moby_dick_text, the text
    Returns:    num_to_chap_title, dict,
    """
    chap_start = moby_dick_text.find('CHAPTER 1')
    chap_end = moby_dick_text.find('Epilogue')
    chap_string = moby_dick_text[chap_start:chap_end]
    reduced_chap_string = chap_string.replace('CHAPTER ', '').strip()
    num_to_chap_title = {}
    for i,word in enumerate(reduced_chap_string.split(' ')):
        if word.replace('.','').isnumeric():
            current_key = int(word.replace('.',''))
            num_to_chap_title[current_key] = ''
        else:
            num_to_chap_title[current_key] = num_to_chap_title[current_key] + word + ' '
    num_to_chap_title = {k:v.strip()[:-1] for k,v in num_to_chap_title.items()}
    return num_to_chap_title

def getAllSectionTitles(moby_dick_text):
    """
    For getting a list of all the section titles.
    Arguments:  moby_dick_text, str, the text
    Returns:    list of str
    """
    num_to_chap_title = extractChapterTitleDict(moby_dick_text)
    all_section_titles = ['CONTENTS', 'ETYMOLOGY', 'EXTRACTS'] + list(num_to_chap_title.values()) + ['Epilogue']
    return all_section_titles

def getSpecialSectionText(moby_dick_text, section_title):
    """
    For getting the text of a given special section.
    Arguments:  moby_dick_text, the text
                section_title, the title of the sections
    Returns:    the text of the section
    """
    title_to_end_phrase = {'CONTENTS':'Original Transcriber', 'ETYMOLOGY':'EXTRACTS. (Supplied by a',
            'EXTRACTS':'CHAPTER 1. Loomings. Call me Ishmael.', 'Epilogue':'End of Project Gutenberg'}
    if not section_title in list(title_to_end_phrase.keys()):
        print(dt.datetime.now().isoformat() + ' ERROR: ' + 'Unrecognised special section title! Exiting.')
        exit(1)
    title_mention_inds = findMultiple(moby_dick_text, section_title)
    section_start = title_mention_inds[len(title_mention_inds) > 1]
    section_end = moby_dick_text.find(title_to_end_phrase.get(section_title))
    return moby_dick_text[section_start:section_end].strip()

def getChapterText(moby_dick_text, num_to_chap_title, chapter_number_or_name, num_chapters=135):
    """
    For geting the text of the given chapter.
    Arguments:  moby_dick_text, the text
                num_to_chap_title, dictionary
                chapter_number_or_name, int, or string
    Returns:    the text of the given chapter, in a big string
    """
    special_sections = ['CONTENTS', 'ETYMOLOGY', 'EXTRACTS', 'Epilogue']
    if int == type(chapter_number_or_name):
        chapter_number = chapter_number_or_name
    elif str == type(chapter_number_or_name):
        if chapter_number_or_name in special_sections:
            return getSpecialSectionText(moby_dick_text, chapter_number_or_name)
        if chapter_number_or_name == 'Knights and Squires':
            raise ValueError(dt.datetime.now().isoformat() + ' ERROR: ' + 'Two different chapters have this title. You must specify the chapter number in this case.')
        chapter_number = list(num_to_chap_title.values()).index(chapter_number_or_name) + 1
    else:
        print(dt.datetime.now().isoformat() + ' ERROR: ' + 'Unrecognised chapter identifier type! Exiting!')
        exit(1)
    chapter_title = num_to_chap_title.get(chapter_number)
    next_chapter_title = 'CHAPTER ' + str(chapter_number+1) + '. ' + num_to_chap_title.get(chapter_number+1) if chapter_number < num_chapters else 'Epilogue'
    chapter_start = findMultiple(moby_dick_text, 'CHAPTER ' + str(chapter_number) + '. ' + chapter_title)[1]
    chapter_end = findMultiple(moby_dick_text, next_chapter_title)[1]
    chapter_text = moby_dick_text[chapter_start:chapter_end].strip()
    return chapter_text

def getNovelText(moby_dick_text):
    """
    For getting the text without the parts referring to licensing or the list of contents.
    Arguments:  moby_dick_text, the text
    Returns:    the novel text, as described above
    """
    novel_start = findMultiple(moby_dick_text, 'ETYMOLOGY')[1]
    novel_end = moby_dick_text.find('End of Project Gutenberg')
    return moby_dick_text[novel_start:novel_end].strip()

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
    return text_to_clean # it is clean now

def getWordFreqDistn(text_to_search):
    """
    For counting the occurances of each word in some given clean text.
    Arguments:  text_to_search, the text in which to count words, should be clean already
    Returns:    word_freq_distn, nltk.FreqDist object, like a dictionary but with extra nice functions.
    """
    text_to_search = text_to_search.replace('CHAPTER','') # chapter is being over counted
    all_words = nltk.word_tokenize(text_to_search)
    all_words = [word for word in all_words if re.search('^[a-zA-Z0-9]*$',  word)]
    word_freq_distn = nltk.FreqDist(all_words)
    # deal with capitalized words here
    unique_words = list(word_freq_distn)
    upper_case_repeated_words = [word for word in unique_words if (word.isupper()) and (word.lower() in unique_words)]
    title_case_repeated_words = [word for word in unique_words if (word.istitle()) and (word.lower() in unique_words)]
    for word in upper_case_repeated_words + title_case_repeated_words:
        word_freq_distn[word.lower()] += word_freq_distn[word]
        del word_freq_distn[word]
    return word_freq_distn

def getCharacterList(character_list_file):
    """
    For getting a list of names, of the characters.
    Arguments:  character_list_file, string,
    Returns:    character_list, a list of str
    """
    with open(character_list_file,'r') as f:
        character_list = f.readlines()
    return [character.replace('\n','') for character in character_list]

def getCharacterCounts(text_to_search, character_list, include_fpp=False):
    """
    For getting counts of the number of times each character is mentioned.
    Arguments:  text_to_search, the text to search for the names
                character_list, the list of characters to search for.
    Returns:    character_count_dict, dictionary, character_name => count
    """
    character_count_dict = {}
    for character in character_list:
        character_count_dict[character] = len(findMultiple(text_to_search, character))
    double_names = {'White Whale':'Moby Dick', 'Moby-Dick':'Moby Dick', 'Parsee':'Fedallah', 'Dough-boy':'Dough-Boy'}
    for k,v in double_names.items():
        if (k in list(character_count_dict)) & (v in list(character_count_dict)):
            character_count_dict[v] += character_count_dict[k]
            del character_count_dict[k]
    if include_fpp:
        character_count_dict['Ishmael'] += countFirstPersonPluralMentions(text_to_search)
    return character_count_dict

def countFirstPersonPluralMentions(text_to_search):
    """
    For counting the number of occurances of the first person plural in the text except for mentions within dialogue.
    Arguments:  text_to_search, str
    Returns:    num_fpp, int
    """
    quote_starts = np.array(findMultiple(text_to_search, '“'))
    quote_ends = np.array(findMultiple(text_to_search, '”'))
    num_fpp = 0 # number of first person plurals
    start_ind = 0
    end_ind = text_to_search.find('“')
    while start_ind < len(text_to_search):
        num_fpp += len(findMultiple(text_to_search[start_ind:end_ind], ' I '))
        num_fpp += len(findMultiple(text_to_search[start_ind:end_ind], ' I.'))
        start_ind = quote_ends[quote_ends > end_ind].min(initial=len(text_to_search))
        end_ind = quote_starts[quote_starts > start_ind].min(initial=len(text_to_search))
    return num_fpp

def posTagWords(words):
    """
    For pos tagging words. Using nltk at first, then ad-hoc fixing.
    Arguments:  words, list or array or str
    Returns:    pos_tagged_words, array of words, tags
    """
    words = np.array(words) if type(words) != np.ndarray else words
    words_tags = np.array(nltk.pos_tag(words))
    corrected_pos_tag_dict = {'upon':'IN',
        'thou':'PRP',
        'thy':'PRP$'}
    words_to_correct = np.intersect1d(words, list(corrected_pos_tag_dict.keys()))
    if words_to_correct.size > 0:
        for word in words_to_correct:
            words_tags[np.flatnonzero(words == word),1] = corrected_pos_tag_dict.get(word)
    return words_tags

def getNumMentionsFrame(character_list, num_to_chap_title, moby_dick_text, character_list_with_doubles):
    """
    For getting a frame showing the number of times each character is mentioned in each chapter.
    Arguments:  character_list, list of str,
                num_to_chap_title, dictionary number => chapter_title
                moby_dick_text, the text,
                character_list_with_doubles, all the character names
    Returns:    pandas dataframe
    """
    num_characters = len(character_list)
    chapter_names = list(num_to_chap_title.values())
    num_chapters = len(chapter_names)
    character_mentions_frame = pd.DataFrame(columns=['chapter_num', 'chapter_name'] + character_list)
    for i in range(num_chapters):
        chapter_num = i+1
        chapter_name = num_to_chap_title.get(chapter_num)
        chapter_text = getChapterText(moby_dick_text, num_to_chap_title, chapter_num)
        chapter_character_count_dict = getCharacterCounts(chapter_text, character_list_with_doubles)
        chapter_character_count_dict['chapter_num'] = chapter_num
        chapter_character_count_dict['chapter_name'] = chapter_name
        character_mentions_frame = character_mentions_frame.append(chapter_character_count_dict, ignore_index=True)
    special_sections = ['ETYMOLOGY', 'EXTRACTS', 'Epilogue']
    special_nums = [-1, 0, 136]
    for chapter_name, chapter_num in zip(special_sections, special_nums):
        chapter_text = getSpecialSectionText(moby_dick_text, chapter_name)
        chapter_character_count_dict = getCharacterCounts(chapter_text, character_list_with_doubles)
        chapter_character_count_dict['chapter_num'] = chapter_num
        chapter_character_count_dict['chapter_name'] = chapter_name
        character_mentions_frame = character_mentions_frame.append(chapter_character_count_dict, ignore_index=True)
    return character_mentions_frame

def ishmaelIsChapterNarrator(chapter_name):
    """
    Is Ishmael the narrator of the given chapter?
    Arguments:  chapter_name, str
    Returns:    boolean
    """
    different_narrator_chapters = ['Sunset', 'Dusk', 'First Night-Watch', 'Midnight, Forecastle']
    return not chapter_name in different_narrator_chapters

def getCharacterCoMentions(character_list, num_to_chap_title, moby_dick_text, character_list_with_doubles, narrator_ishmael):
    """
    A function for getting a matrix of 'co-mentions' for the characters.
    That is, a matrix of the number of times each pair of charcters are
    mentioned in the same chapter.
    Arguments:  character_list, list of str,
                num_to_chap_title, dictionary number => chapter_title
                moby_dick_text, the text,
                character_list_with_doubles, all the character names
                narrator_ishmael, boolean, include ishmael as the narrator or not.
    Returns:    numpy array int (num characters, num_characters)
                total_mentions, numpy array int (num_characters)
    """
    num_characters = len(character_list)
    chapter_names = list(num_to_chap_title.values())
    num_chapters = len(chapter_names)
    chapter_mentions = np.zeros([num_characters, num_characters], dtype=int)
    total_mentions = np.zeros(num_characters, dtype=int)
    for i in range(num_chapters):
        chapter_num = i+1
        chapter_name = num_to_chap_title.get(chapter_num)
        chapter_text = getChapterText(moby_dick_text, num_to_chap_title, chapter_num)
        chapter_character_count_dict = getCharacterCounts(chapter_text, character_list_with_doubles)
        if narrator_ishmael & ishmaelIsChapterNarrator(chapter_name):
            chapter_character_count_dict['Ishmael'] = 1
        mentioned_inds = np.flatnonzero(list(chapter_character_count_dict.values()))
        comention_inds = combinations(mentioned_inds, 2)
        total_mentions[mentioned_inds] += 1
        for c in comention_inds:
            chapter_mentions[c[0], c[1]] += 1
    chapter_mentions += chapter_mentions.T
    return chapter_mentions, total_mentions

def getNormedCharacterCoMentions(character_list, num_to_chap_title, moby_dick_text, character_list_with_doubles, narrator_ishmael):
    """
    A function for getting a matrix of normalised 'co-mentions' for the characters.
    That is, a matrix of the number of times each pair of charcters are
    mentioned in the same chapter, divided by the combined number of chapters
    in which each character is mentioned, divided by 2.
    Arguments:  character_list, list of str,
                num_to_chap_title, dictionary number => chapter_title
                moby_dick_text, the text,
                character_list_with_doubles, all the character names
                narrator_ishmael, boolean, include ishmael as the narrator or not.
    Returns:    normed_chapter_mentions, numpy array int (num characters, num_characters)
                total_mentions, numpy array int (num_characters)
    """
    num_characters = len(character_list)
    chapter_names = list(num_to_chap_title.values())
    num_chapters = len(chapter_names)
    chapter_mentions = np.zeros([num_characters, num_characters], dtype=int)
    total_mentions = np.zeros(num_characters, dtype=int)
    for i in range(num_chapters):
        chapter_num = i+1
        chapter_name = num_to_chap_title.get(chapter_num)
        chapter_text = getChapterText(moby_dick_text, num_to_chap_title, chapter_num)
        chapter_character_count_dict = getCharacterCounts(chapter_text, character_list_with_doubles)
        if narrator_ishmael & ishmaelIsChapterNarrator(chapter_name):
            chapter_character_count_dict['Ishmael'] = 1
        mentioned_inds = np.flatnonzero(list(chapter_character_count_dict.values()))
        total_mentions[mentioned_inds] += 1
        comention_inds = combinations(mentioned_inds, 2)
        for c in comention_inds:
            chapter_mentions[c[0], c[1]] += 1
    normed_chapter_mentions = np.zeros([num_characters, num_characters], dtype=float)
    for c in combinations(range(num_characters),2):
        normed_chapter_mentions[c[0],c[1]] = (2*chapter_mentions[c[0], c[1]])/(total_mentions[c[0]] + total_mentions[c[1]])
    normed_chapter_mentions += normed_chapter_mentions.T
    return normed_chapter_mentions, total_mentions

################################################################################
########################### PLOTTING FUNCTIONS #################################
################################################################################

def plotMostCommonWordsBar(sorted_dict, num_words=20, y_label='Num. occurances', x_label='Word', title=''):
    """
    For making a bar plot showing the most common words and how often they appear
    Arguments:  sorted_dict, sorted dictionary of 'word' => number of occurances
                num_words, how many words to include? top 20?
    Returns:    nothing
    """
    fig,ax = plt.subplots(nrows=1, ncols=1)
    ax.bar(x=range(num_words), height=list(sorted_dict.values())[:num_words])
    ax.grid(axis='y', alpha=0.25)
    ax.set_xlim(-1,num_words)
    ax.set_xticks(range(num_words))
    ax.set_xticklabels(list(sorted_dict.keys())[:num_words])
    ax.tick_params(axis='both', labelsize='large')
    [tick.set_rotation(45) for tick in ax.get_xticklabels()]
    ax.set_ylabel(y_label, fontsize='x-large') if y_label != '' else None
    ax.set_xlabel(x_label, fontsize='x-large') if x_label != '' else None
    [ax.spines[s].set_visible(False) for s in ['top', 'right']]
    ax.set_title(title, fontsize='large') if title != '' else None
    plt.tight_layout()

def plotChapterCoMentions(mentions_matrix, character_list, title='', figsize=(5,4)):
    """
    For plotting the matrix of chapter mentions, normalised or otherwise.
    Arguments:  mentions_matrix, numpy array (num_characters, num_characters)
                character_list, list of str
                title,
    Returns:    Nothing
    """
    num_characters = mentions_matrix.shape[0]
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=figsize)
    im = ax.imshow(mentions_matrix, cmap='Blues')
    ax.set_xticks(range(num_characters))
    ax.set_xticklabels(character_list)
    [tick.set_rotation(45) for tick in ax.get_xticklabels()]
    ax.set_yticks(range(num_characters))
    ax.set_yticklabels(character_list)
    [tick.set_rotation(45) for tick in ax.get_yticklabels()]
    ax.set_title(title, fontsize='large') if title != '' else None
    fig.colorbar(im)
    plt.tight_layout()

def plotMentionsNetworkGraph(mentions_matrix, character_list, figsize=(10,10)):
    """
    For plotting a network graph of the network formed by the mentions matrix.
    Arguments:  mentions_matrix, square matrix containing character comentions
                character_list, list of str
    Returns:    nothing
    """
    mention_edges = np.nonzero(np.triu(mentions_matrix))
    mention_edges_list = list(zip(mention_edges[0], mention_edges[1]))
    character_connections = nx.Graph()
    edge_weights = []
    for source, target in mention_edges_list:
        character_connections.add_edge(character_list[source], character_list[target], weight=mentions_matrix[source, target])
        edge_weights.append(mentions_matrix[source, target])
    nx.draw_circular(character_connections, with_labels=True, node_size=300, node_color='white', edge_cmap=cm.Blues, edge_color=edge_weights, font_weight='bold')

################################################################################
######## POS TAGGING DICT ######################################################
################################################################################

def getPOSTagMeaningDict():
    """
    For getting the dictionary of POS code => meaning.
    Returns: dictionary
    """
    pos_tag_meaning_dict = {#Abbreviation	Meaning
        'CC':'coordinating conjunction',
        'CD':'cardinal digit',
        'DT':'determiner',
        'EX':'existential there',
        'FW':'foreign word',
        'IN':'preposition/subordinating conjunction',
        'JJ':'adjective',
        'JJR':'adjective, comparative',
        'JJS':'adjective, superlative',
        'LS':'list market',
        'MD':'modal',
        'NN':'noun, singular',
        'NNS':'noun plural',
        'NNP':'proper noun, singular',
        'NNPS':'proper noun, plural',
        'PDT':'predeterminer',
        'POS':'possessive ending',
        'PRP':'personal pronoun',
        'PRP$':'possessive pronoun',
        'RB':'adverb',
        'RBR':'adverb, comparative',
        'RBS':'adverb, superlative',
        'RP':'particle',
        'TO':'infinite marker',
        'UH':'interjection',
        'VB':'verb',
        'VBG':'verb gerund',
        'VBD':'verb past tense',
        'VBN':'verb past participle',
        'VBP':'verb, present tense not 3rd person singular',
        'VBZ':'verb, present tense with 3rd person singular',
        'WDT':'wh-determiner',
        'WP':'wh-pronoun',
        'WRB':'wh-adverb'}
    return pos_tag_meaning_dict
