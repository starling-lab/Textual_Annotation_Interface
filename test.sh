bash ./test_setup.sh

java -jar v1-0.jar -i -model train/models/ -test test/ -target sentenceContainsTarget -trees 25 -aucJarPath . > test.log 2> test_error.log