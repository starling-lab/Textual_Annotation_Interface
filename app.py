from flask import Flask, render_template

pos_examples_file_src = "files/pos_examples.txt"

pos_examples_file = open(pos_examples_file_src,'a')

app = Flask(__name__)

@app.route("/getmethod/<jsdata>")
def add_positive_example(jsdata):
	global pos_examples_file
	pos_examples_file.write(jsdata+"\n")
	return jsdata

def get_pos_examples():
	global pos_examples_file
	pos_examples_file.close()
	pos_examples_file = open(pos_examples_file_src, "r")
	pos_examples = pos_examples_file.read().split('\n')
	pos_examples = [e for e in pos_examples if e != '']
	return pos_examples

@app.route("/getexamples/")
def print_pos_examples():
	print "Positive examples are : \n"
	print get_pos_examples()
	return ""

@app.route("/")
def index():
   return render_template("index.html")

if __name__ == '__main__':
   app.run()