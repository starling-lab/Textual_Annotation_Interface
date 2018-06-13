rm files/pos_examples.txt
rm bk.txt
rm blockIDs.txt
rm sentenceIDs.txt
rm wordIDs.txt
rm train.log
rm train-error.log

cp train/train_bk.txt ./
rm -r train/models
rm train/*
mv train_bk.txt train/train_bk.txt