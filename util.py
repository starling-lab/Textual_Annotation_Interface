from flask import Flask, render_template, redirect, url_for, request
from nltk import sent_tokenize
from werkzeug import secure_filename
import rnlp
import os
import sys
import string
import bash
from util import *

# Helper functions -------------------------
	
def prepare_files(train_document_src, train_pos_file, test_pos_file):
	#Creates files to be used for adding selected examples from annotator

	train_pos_src = "files/pos_"+train_document_src.split('/')[1]

	train_pos_file = open(train_pos_src,'a')

	test_pos_file = open(test_pos_src, 'a')

def get_scores(file_src, block_size):
	# Input: Path of the file containing the results (results_sentenceContainsTarget.db)
	# Output: Returns the list of dictionaries. Each dictionary corresponds to a sentence in the test doc. Each dict has fields, neg (boolean: is example negative?), score (regression score for match), block_id, sentence_id
	file = open(file_src, "r")
	sentences = file.read().split('\n')
	dict_list = []
	for sentence in sentences:
		if sentence!= "":
			dict = {}
			if sentence[0]=='!':
				dict["neg"] = True
			else :
				dict["neg"] = False
			terms = sentence.split(' ')
			dict["score"] = float(terms[1])
			i1 = terms[0].find('(') + 2
			i2 = terms[0].find(')')	- 1
			dict["block_id"] = int(terms[0][i1:i2].split('_')[0])
			dict["sentence_id"] = int(terms[0][i1:i2].split('_')[1])
			dict_list.append(dict)
	#Re-arranging dict list in order of sentences in doc
	lst = []
	block_id = 1
	sentence_id = 1

	for i in range(len(dict_list)):
		dict = [d for d in dict_list if d["block_id"] == block_id and d["sentence_id"] == sentence_id]
		lst.append(dict[0])
		sentence_id +=1
		if sentence_id>block_size:
			block_id+=1
			sentence_id =1
	
	return lst	

def get_doc_posExamples(examples):
	#Input: positive examples selected by user for current doc
	#Returns corpus: String of all documents (stored in data/docs, joined with current)
	#	all_examples: List of all positive examples (stored in data/annotations, extended with current doc's)
	corpus = ""
	for doc_name in os.listdir("./data/docs"):
		if doc_name!= "README.md":
			corpus+=open("./data/docs/"+doc_name,"r").read()+'\n'
	if len(corpus)>0:
		corpus = corpus[:-1]
	examples_string = ""
	for file_name in os.listdir("./data/annotations"):
		if file_name!= "README.md":
			examples_string+= "\n"+open("./data/annotations/"+file_name,"r").read()
	all_examples = examples_string.split('\n')
	all_examples.extend(examples)


	all_examples = [e.strip() for e in all_examples if e!=""]
	return corpus,all_examples

def get_pos_examples(pos_examples_file, pos_examples_src):
	#Returns a list of positive examples read from file
	pos_examples_file.close()
	pos_examples_file = open(pos_examples_src, "r")
	pos_examples = pos_examples_file.read().split('\n')
	pos_examples = [e for e in pos_examples if e != '']
	return pos_examples

def get_pos_lines(document, examples):
	
	#Input: document (list of lines/sentences), examples (phrases selected by user (string))
	#Returns the lines in document containing the example phrases
	'''Assumptions: 1. Examples are given in top-down order in the document.
		2. Multiple examples can be given for a single line in document (The line is added only once)
		3. If the same example is encountered again, it is marked again. 
		4. If the same line appears in the document containing example/s, it will be added again. 
	'''
	pos_lines = []
	temp = []
	line_index = 0
	example_index = 0
 

	while(example_index < len(examples)):
		while(line_index< len(document)):
			if (example_index >=len(examples)):
				break
			example = examples[example_index]
			line = document[line_index]
			if example in line:
				if len(pos_lines)>0 and pos_lines[-1] == line:
					#The next example is also present in previous line or same line repeats
					example_index+=1
				else:
					temp.append(line)
					example_index+=1
			else:
				line_index+=1
		example_index+=1
	for t in temp:
		pos_line = t.strip()
		pos_lines.append(pos_line)
	return pos_lines

def remove_punctuation(str):
	#Removes punctuation in string, str
	s_new = ""
	for c in str:
		if c not in string.punctuation:
			s_new+=c

	return s_new


def create_files(corpus, labelled_positive):
	#Input: corpus (single string of documents combined), labelled_positive (full sentences labelled as positive examples)
	#Creates files required for training/testing the model
	example_corpus = corpus.split('\n')
	corpus_string = ""
	for sentence in example_corpus:
	    corpus_string += sentence + ' '
	# Convert 'corpus_string' into a set of predicates.
	rnlp.converter(corpus_string)

	# Read the contents of sentenceIDs.txt to find the ID numbers.
	# NOTE: Super not-optimal!!! :

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


	    # sentences = remove_punctuation(sentences)
	    for s in sentences:

	        if s in labelled_positive:
	            # If this current sentence was labelled positve, create predicate.
	            s_new = remove_punctuation(s)
	            positive.append('sentenceContainsTarget(' + mapping[s_new.replace('.', '')] + ').')
	        else:
	            s_new = remove_punctuation(s)
	            negative.append('sentenceContainsTarget(' + mapping[s_new.replace('.', '')] + ').')

	# Write everything to files.
	with open('pos.txt', 'w') as f:
	    for p in positive:
	        f.write(p + '\n')

	with open('neg.txt', 'w') as f:
	    for n in negative:
	        f.write(n + '\n')


# End of helper functions -------------------------------------