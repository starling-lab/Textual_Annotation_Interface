# Copyright (c) 2018 StARLinG Lab.

"""
predicates
==========

An example script for converting a set of documents into a set of relational
predicates.

.. note:: This is created as a way to show how the present design of rnlp
          may be used to perform this function. It is not implied that the
          design of rnlp is *optimal* for performing this function.

Example:

$ pip install -r annotate/requirements.txt
>>> import annotate.predicates
"""

from __future__ import print_function

from nltk import sent_tokenize
import rnlp

# Consider an example_corpus, where each string represents a document.
example_corpus = [
    'This is the first sentence. Sheep are mammals. McDonalds sells burgers.',
    'Waffle House sells waffles. This is the second sentence. Dogs are cool.',
    'I sometimes wear slippers. Shoes go on your feet. Dominoes makes pizza.'
]

# This corpus contains positive examples annotated by the user.
labeled_positive = [
    'McDonalds sells burgers.',
    'Waffle House sells waffles.',
    'Dominoes makes pizza.'
]

# Join the corpus into a single string.
corpus_string = ""
for sentence in example_corpus:
    corpus_string += sentence + ' '

# Convert 'corpus_string' into a set of predicates.
rnlp.converter(corpus_string)

# Read the contents of sentenceIDs.txt to find the ID numbers.
# NOTE: Super not-optimal!!! :O

with open('sentenceIDs.txt', 'r') as f:
    sids = f.read().splitlines()

mapping = {}
for line_index in range(len(sids)):
    if 'sentenceID:' in sids[line_index]:
        mapping[sids[line_index+1].replace('sentence string: ', '')] = sids[line_index].split(' ')[1]

# Initialize lists of positive and negative examples (which will be written
# to files in the end).
positive, negative = [], []

for document in example_corpus:

    # Tokenize the document into a list of sentences.
    sentences = sent_tokenize(document)

    for s in sentences:
        if s in labeled_positive:
            # If this current sentence was labelled positve, create predicate.
            positive.append('sentenceContainsTarget(' + mapping[s.replace('.', '')] + ').')
        else:
            negative.append('sentenceContainsTarget(' + mapping[s.replace('.', '')] + ').')

# Write everything to files.
with open('pos.txt', 'w') as f:
    for p in positive:
        f.write(p + '\n')

with open('neg.txt', 'w') as f:
    for n in negative:
        f.write(n + '\n')
