from flask import Flask, render_template
from nltk import sent_tokenize
import rnlp

pos_examples_file_src = "files/pos_examples.txt"
document_src = "files/document.txt"

pos_examples_file = open(pos_examples_file_src,'a')

app = Flask(__name__)

@app.route("/addText/<jsdata>")
#Change this to post to improve security
def add_positive_example(jsdata):
	global pos_examples_file
	pos_examples_file.write(jsdata+"\n")
	return jsdata

def get_pos_examples():
	global pos_examples_file
	global pos_examples_file_src
	pos_examples_file.close()
	pos_examples_file = open(pos_examples_file_src, "r")
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



@app.route("/learn/")
def learn():
	global document_src
	document = open(document_src, 'r').read()
	examples = get_pos_examples()
	line_list = document_to_lines(document)
	pos_lines = get_pos_lines(line_list,examples)
	create_files(document,pos_lines)
	print "Created files from labeled data\n"
	return ""


@app.route("/")
def index():
   return render_template("index.html")

if __name__ == '__main__':
   app.run()