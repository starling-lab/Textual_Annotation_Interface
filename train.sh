bash ./train_setup.sh

java -jar v1-0.jar -l -train train -target sentenceContainsTarget -trees 25 > train.log 2> train-error.log

bash ./train_cleanup.sh