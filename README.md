# Moby Dick Statistics; or, The Analysis

A project for doing some statistical analysis on the text of the novel 'Moby Dick; or, The Whale' by Herman Melville. In particular, I would like to apply the 'Spectral Rejection' community detection method developed by Mark Humpries to the characters of the novel. In the publication detailing the method, the method is applied to the text of 'Les Miserables' in order to 'communities' of characters that tend to get mentioned together in the course of a chapter.

## Requirements

Python 3.7 > 
numpy
re
nltk

## TODO

* Account for characters having more than one name

## Downloading & Extracting the Text

The ```py/download_and_extract_text.py``` script is used to download and extract the text of the novel into a useful format. This text is then saved in ```txt/moby_dick.txt```.

## 'Part-of-Speech' Tagging

The ```nltk``` package is used for POS tagging the text. The tagging codes can be found [here](https://www.guru99.com/pos-tagging-chunking-nltk.html).

## Taking measurements

The ```py/moby_dick_stats.py``` script is used to extract measurements and statistics from the text.

## Useful functions

The functions that are used in the repo are stored in ```py/moby_dick_functions.py```

## References

1. Mark D. Humphries, Javier A. Caballero, Mat Evans, Silvia Maggi, Abhinav Singh, *"Spectral rejection for testing hypotheses of structure in networks".* In: arXiv:1901.04747, (2019)

