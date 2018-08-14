import os
import platform
import sys

def store_train_doc(train_document_src):
	#Stores train document in data/docs
	if platform.system() == "Linux":
		os.system("cp "+train_document_src+" data/docs")

	elif platform.system() == "Windows":
		train_document_src = train_document_src.replace("/", "\\")
		os.system("copy "+train_document_src+" data\\docs")

def store_train_pos(train_pos_src):
	#Stores annotations file for train doc in data/annotations
	if platform.system() == "Linux":
		os.system("cp "+train_pos_src+" data/annotations/")

	elif platform.system() == "Windows":
		train_pos_src = train_pos_src.replace("/", "\\")
		os.system("copy "+train_pos_src+" data\\annotations")


def test():
	test_setup()
	if platform.system() == "Linux":
		os.system("java -jar v1-0.jar -i -model train/models/ -test test/ -target sentenceContainsTarget -trees 25 -aucJarPath . > test.log 2> test-error.log")
	elif platform.system() == "Windows":
		os.system("java -jar v1-0.jar -i -model train\\models -test test -target sentenceContainsTarget -trees 25 -aucJarPath .\\")

def test_setup():
	if platform.system() == "Linux":
		os.system("mv facts.txt test/test_facts.txt")
		os.system("mv neg.txt test/test_neg.txt")
		os.system("mv pos.txt test/test_pos.txt")
	elif platform.system() == "Windows":
		os.system("move facts.txt test\\test_facts.txt")
		os.system("move neg.txt test\\test_neg.txt")
		os.system("move pos.txt test\\test_pos.txt")

def train_setup():
	if platform.system() == "Linux":
		os.system("mv facts.txt train/train_facts.txt")
		os.system("mv neg.txt train/train_neg.txt")
		os.system("mv pos.txt train/train_pos.txt")
	elif platform.system() == "Windows":
		os.system("move facts.txt train\\train_facts.txt")
		os.system("move neg.txt train\\train_neg.txt")
		os.system("move pos.txt train\\train_pos.txt")

def train_cleanup():
	if platform.system() == "Linux":
		os.system("rm bk.txt")
		os.system("rm blockIDs.txt")
		os.system("rm sentenceIDs.txt")
		os.system("rm wordIDs.txt")
	elif platform.system() == "Windows":
		os.system("del bk.txt")
		os.system("del blockIDs.txt")
		os.system("del sentenceIDs.txt")
		os.system("del wordIDs.txt")

def train():
	train_setup()
	if platform.system() == "Linux":
		os.system("java -jar v1-0.jar -l -train train -target sentenceContainsTarget -trees 25 > train.log 2> train-error.log")
	elif platform.system() == "Windows":	
		os.system("java -jar v1-0.jar -l -train train -target sentenceContainsTarget -trees 25")
	train_cleanup()

def plot_models():
	#Plots first two models into image directory
	#NOTE: Problem of inner "" need to be resolved in dot files before plotting
	os.system("mkdir images")
	os.system("cd train/models/bRDNs/dotFiles")
	#Plot first two models
	os.system("dot -Tpng WILLTreeFor_sentenceContainsTarget0.dot -o ../../../../images/0.png")
	os.system("dot -Tpng WILLTreeFor_sentenceContainsTarget1.dot -o ../../../../images/1.png")

def cleanup():
	#Cleans up all unrequired files for re-running the program with new document
	if platform.system() == "Linux":
		os.system("rm files/pos*")
		os.system("rm bk.txt")
		os.system("rm blockIDs.txt")
		os.system("rm sentenceIDs.txt")
		os.system("rm wordIDs.txt")
		os.system("rm train.log")
		os.system("rm train-error.log")
		os.system("rm test.log")
		os.system("rm test-error.log")

		os.system("cp train/train_bk.txt ./")
		os.system("rm -r train/models")
		os.system("rm train/*")
		os.system("mv train_bk.txt train/train_bk.txt")

		os.system("cp test/test_bk.txt ./")
		os.system("rm -r test/AUC")
		os.system("rm test/*")
		os.system("mv test_bk.txt test/test_bk.txt")
	elif platform.system() == "Windows":
		os.system("del files\\pos* /q")
		os.system("del bk.txt")
		os.system("del blockIDs.txt")
		os.system("del sentenceIDs.txt")
		os.system("del wordIDs.txt")


		os.system("copy train\\train_bk.txt .\\")
		os.system("rmdir train\\models /s /q")
		os.system("del train\\* /q")
		os.system("move train_bk.txt train\\train_bk.txt")

		os.system("copy test\\test_bk.txt .\\")
		os.system("rmdir test\\AUC /s /q")
		os.system("del test\\* /q")
		os.system("move test_bk.txt test\\test_bk.txt")