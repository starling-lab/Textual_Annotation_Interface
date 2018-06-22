# Textual_Annotation_Interface
The interface lets experts annotate relations in textual data to build and test a model.
## About:
The software allows users to annotate relations in a training document to train a boosted SRL model (https://starling.utdallas.edu/software/boostsrl/). 
The relations in a test document can also be annotated to check the model's accuracy. 
The predictions of the model (in the results page) shows how correctly (bright green for high, dark green for low) the correct examples were predicted or how well (dark red for low, bright red for high) examples were classified as incorrect.
## Usage Instructions:
* Start Flask server by running "python app.py (train document path) (test document path)"
* Use "bash cleanup.sh" to delete the models, test results for restarting application.