"""
Functions and globals that are useful for the project.
"""

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

