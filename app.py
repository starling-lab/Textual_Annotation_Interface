from flask import Flask, render_template

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

def load_document_from_file(document_src):
	#Loads the document (as a list of lines) from files directory.
	lines = []
	document = open(document_src, 'r')
	paras = document.read().split('\n')
	for para in paras:
		lines.extend(para.split('.'))
	return lines

def get_pos_lines(document, examples):

	#Returns the lines in document containing the example phrases
	'''Assumptions: 1. Examples are given in top-down order in the document.
		2. Multiple examples can be given for a single line in document (The line is added only once)
		3. If the same example is encountered again, it is marked again. 
		4. If the same line appears in the document containing example/s, it will be added again. 
	'''
	pos_lines = []
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
					pos_lines.append(line)
					example_index+=1
			else:
				line_index+=1
	return pos_lines


@app.route("/learn/")
def learn():
	global document_src
	document = load_document_from_file(document_src)
	examples = get_pos_examples()
	print "Identified positive lines : \n"
	print get_pos_lines(document, examples)
	return ""



@app.route("/")
def index():
   return render_template("index.html")

if __name__ == '__main__':
   app.run()