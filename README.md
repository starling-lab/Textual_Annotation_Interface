# Textual_Annotation_Interface
The interface lets experts annotate relations in textual data to build and test a model.
## About:
The software allows users to annotate relations in a training document to train a boosted SRL model (https://starling.utdallas.edu/software/boostsrl/). 
The relations in a test document can also be annotated to check the model's accuracy. 
The predictions of the model (in the results page) shows how correctly (bright green for high, dark green for low) the correct examples were predicted or how well (dark red for low, bright red for high) examples were classified as incorrect.
All the previously annotated files are stored and used for the next training. 
## Usage Instructions:
* Start Flask server by running "python app.py". (Use python 2.7)
* Add the files to be used for training and testing. Annotate and see results.
* Use "python cleanup.py" to delete the train, test files for restarting application.