rm files/pos*
rm bk.txt
rm blockIDs.txt
rm sentenceIDs.txt
rm wordIDs.txt
rm *.log
rm *.pyc

cp train/train_bk.txt ./
rm -r train/models
rm train/*
mv train_bk.txt train/train_bk.txt

cp test/test_bk.txt ./
rm -r test/AUC
rm test/*
mv test_bk.txt test/test_bk.txt