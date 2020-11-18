"""
Functions and globals that are useful for the project.
"""
import nltk, re
import numpy as np

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
    reduced_chap_string = chap_string.replace('CHAPTER ', '').replace('.','').strip()
    num_to_chap_title = {}
    for i,word in enumerate(reduced_chap_string.split(' ')):
        if word.isnumeric():
            current_key = int(word)
            num_to_chap_title[current_key] = ''
        else:
            num_to_chap_title[current_key] = num_to_chap_title[current_key] + word + ' '
    num_to_chap_title = {k:v.strip() for k,v in num_to_chap_title.items()}
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

def getWordFreqDistn(clean_text):
    """
    For counting the occurances of each word in some given clean text.
    Arguments:  clean_text, the text in which to count words, should be clean already
    Returns:    word_freq_distn, nltk.FreqDist object, like a dictionary but with extra nice functions.
    """
    all_words = nltk.word_tokenize(clean_text)
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

def getCharacterCounts(clean_text, character_list):
    """
    For getting counts of the number of times each character is mentioned.
    Arguments:  clean_text, the text to search for the names
                character_list, the list of characters to search for.
    Returns:    character_count_dict, dictionary, character_name => count
    """
    character_count_dict = {}
    for character in character_list:
        character_count_dict[character] = len(findMultiple(clean_text, character))
    double_names = {' I ':'Ishmael', 'White Whale':'Moby Dick', 'Moby-Dick':'Moby Dick', 'Parsee':'Fedallah', 'Dough-boy':'Dough-Boy'}
    for k,v in double_names.items():
        if (k in list(character_count_dict)) & (v in list(character_count_dict)):
            character_count_dict[v] += character_count_dict[k]
            del character_count_dict[k]
    return character_count_dict

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
