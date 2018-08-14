from __future__ import print_function
from flask import Flask, render_template, redirect, url_for, request
from nltk import sent_tokenize
from werkzeug import secure_filename
import rnlp
import os
import sys
import string
import bash
from util import *

block_size = 2

train_document_src = ""
test_document_src = ""

#Preparing files

train_pos_src = ""
test_pos_src = "files/pos_test_examples.txt"
train_pos_file = 0
test_pos_file = 0


app = Flask(__name__)

@app.route("/")
def index():
	#Renders index page with file uploads
	load_packages()
	return render_template("index.html")

@app.route("/addTextTrain/<jsdata>")
def add_positive_example(jsdata):
	#Adds phrase as positive example to file (train)
	global train_pos_file
	train_pos_file.write(jsdata+"\n")
	return jsdata

@app.route("/addTextTest/<jsdata>")
def add_positive_example_test(jsdata):
	#Adds phrase as positive example to file (test)
	global test_pos_file
	test_pos_file.write(jsdata+"\n")
	return jsdata


@app.route("/result", methods = ["POST","GET"])
def result():
	#Render results page
	global test_document_src, block_size
	text = ""
	scores = get_scores("test/results_sentenceContainsTarget.db", block_size)
	sentences = sent_tokenize(open(test_document_src,"r").read())
	sentences = [s for s in sentences if s!= ""]
	#Generates html labels with color-value based on score
	for i in range(len(scores)):
		if scores[i]["neg"] == True:
			text+="<label style = \"background-color:rgb("+str(int(scores[i]["score"]*255))+",0,0); color:white;\">"+sentences[i]+"</label>"
		else:
			text+="<label style = \"background-color:rgb(0,"+str(int(scores[i]["score"]*255))+",0); color:white;\">"+sentences[i]+"</label>"
	return render_template("result.html").format(text)

@app.route("/filesAdded", methods = ["POST","GET"])
def filesAdded():
	#Adds files to local "files" directory and renders "files added" page
	global train_document_src
	global test_document_src
	global train_pos_src, train_pos_file, test_pos_file

	if request.method == 'POST':
		f = request.files['trainFile']
		train_document_src = "files/"+secure_filename(f.filename)
		f.save(train_document_src)

		f = request.files['testFile']
		test_document_src = "files/"+secure_filename(f.filename)
		f.save(test_document_src) 

		#Creating files to be used for adding selected examples from annotator
		train_pos_src = "files/pos_"+train_document_src.split('/')[1]
		train_pos_file = open(train_pos_src,'a')
		test_pos_file = open(test_pos_src, 'a')


	return render_template("filesAdded.html")


@app.route("/interface/", methods = ["POST","GET"])
def interface():
	#Create and render interface page
	global train_document_src
	global test_document_src

	#Displays file's text in textboxes
	return render_template("interface.html").format(open(train_document_src,"r").read(),open(test_document_src,"r").read())

@app.route("/learn/")
def learn():
	#Train model using files created
	global train_document_src
	global train_pos_file
	global train_pos_src
	#Copy train document data/docs folder
	bash.store_train_doc(train_document_src)

	#Process positive examples and create required files for training
	examples = get_pos_examples(train_pos_file, train_pos_src)
	document, examples = get_doc_posExamples(examples)
	line_list = sent_tokenize(document)
	pos_lines = get_pos_lines(line_list,examples)
	create_files(document,pos_lines)

	#Copy train positive examples file to data/annotations
	bash.store_train_pos(train_pos_src)
	#Train model
	bash.train()
	print("Training complete!!\n")
	return ""


@app.route("/test/")
def test():
	#Test model
	global test_document_src
	global test_pos_file
	global test_pos_src

	#Process positive examples and create files required for testing
	document = open(test_document_src,'r').read()
	examples = get_pos_examples(test_pos_file, test_pos_src)
	line_list = sent_tokenize(document)
	pos_lines = get_pos_lines(line_list,examples)
	create_files(document,pos_lines)
	
	#Test model
	bash.test()
	print("Testing done!!")
	return ""
	

if __name__ == '__main__':
	app.run(debug =True)