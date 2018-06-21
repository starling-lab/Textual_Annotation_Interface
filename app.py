from flask import Flask, render_template, redirect, url_for
from nltk import sent_tokenize
import rnlp
import os
import sys


train_pos_src = "files/pos_train_examples.txt"
test_pos_src = "files/pos_test_examples.txt"

block_size = 2

if len(sys.argv) > 1:
	train_document_src = sys.argv[1]
	test_document_src = sys.argv[2]

	print "Path of train document: "+sys.argv[1]
	print "Path of test document: "+sys.argv[2]
else:
	print "Please enter path of train document: "
	train_document_src = raw_input()
	print "Please enter path of test document: "
	test_document_src = raw_input()


# train_document_src = "files/document.txt"
# test_document_src = "files/document5.txt"

train_pos_file = open(train_pos_src,'a')

test_pos_file = open(test_pos_src, 'a')

app = Flask(__name__)

@app.route("/addTextTrain/<jsdata>")
#Change this to post to improve security
def add_positive_example(jsdata):
	global train_pos_file
	train_pos_file.write(jsdata+"\n")
	return jsdata

@app.route("/addTextTest/<jsdata>")
#Change this to post to improve security
def add_positive_example_test(jsdata):
	global test_pos_file
	test_pos_file.write(jsdata+"\n")
	return jsdata

def get_scores(file_src):
	global block_size

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
	#Re-arranging dict list
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


def get_pos_examples(pos_examples_file, pos_examples_src):
	pos_examples_file.close()
	pos_examples_file = open(pos_examples_src, "r")
	pos_examples = pos_examples_file.read().split('\n')
	pos_examples = [e for e in pos_examples if e != '']
	return pos_examples

def document_to_lines(document):
	lines = []
	paras = document.split('\n')
	for para in paras:
		# lines.extend(para.split('.'))
		para_lines = para.split('.')
		for para_line in para_lines:
			para_line+="."
			lines.append(para_line)
	return lines



def get_pos_lines(document, examples):

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
	for t in temp:
		pos_line = t.strip()
		pos_lines.append(pos_line)
	return pos_lines



def create_files(corpus, labeled_positive):
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

@app.route("/result", methods = ["POST","GET"])
def result():
	global test_document_src
	text = ""
	scores = get_scores("test/results_sentenceContainsTarget.db")
	sentences = document_to_lines(open(test_document_src,"r").read())[:-1]
	for i in range(len(scores)):
		if scores[i]["neg"] == True:
			text+="<label style = \"background-color:rgb("+str(int(scores[i]["score"]*255))+",0,0); color:white;\">"+sentences[i]+"</label>"
			# print "background:red "+str(int(scores[i]["score"]*100))+"%;"
		else:
			text+="<label style = \"background-color:rgb(0,"+str(int(scores[i]["score"]*255))+",0); color:white;\">"+sentences[i]+"</label>"
			# print "background:green "+str(int(scores[i]["score"]*100))+"%;"
	return render_template("result.html").format(text)

@app.route("/learn/")
def learn():
	global train_document_src
	global train_pos_file
	global train_pos_src
	document = open(train_document_src, 'r').read()
	examples = get_pos_examples(train_pos_file, train_pos_src)
	line_list = document_to_lines(document)
	pos_lines = get_pos_lines(line_list,examples)
	create_files(document,pos_lines)
	os.system("bash train.sh")
	print "Training complete!!\n"
	return ""


@app.route("/test/")
def test():
	global test_document_src
	global test_pos_file
	global test_pos_src
	document = open(test_document_src, 'r').read()
	examples = get_pos_examples(test_pos_file, test_pos_src)
	line_list = document_to_lines(document)
	pos_lines = get_pos_lines(line_list,examples)
	create_files(document,pos_lines)
	os.system("bash test.sh")
	print "Testing done!!"
	return ""
	


@app.route("/")
def index():
	global train_document_src
	global test_document_src
	return render_template("index.html").format(open(train_document_src,"r").read(),open(test_document_src,"r").read())

if __name__ == '__main__':
	app.run(debug =True)