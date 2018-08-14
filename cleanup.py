import os
import platform
import sys

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

if __name__ == "__main__":
	cleanup()