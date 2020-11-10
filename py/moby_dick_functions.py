"""
Functions that are useful for the project.
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
