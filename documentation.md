# Documentation
## Code layout
* The *data* folder contains the documents and files containing annotated phrases. After every session, the new document and annotation file are added to this folder by the program.
* *static, templates* folders along with app.py file form the flask application's components.
* *test* and *train* directories initially contain only background files. They are populated with required files when the application is run.
* *files* directory is where the test and train documents for the current session can be added and referred to when the program is run.
* *cleanup.sh* bash script can be used to remove all the unncessary files before the program is restarted.
* *plot_models.sh* can be used to plot the first two models after training. ("Note: Syntax errors need to be fixed in the .dot files before plotting")

## Documentation for app.py

* Program takes train and test documents paths as inputs through command line
* *index()* function renders the homepage for the app.
* Functions, *add_positive_example* and *add_positive_example_test* are used to get the selected text from Java Script.
* Function, *learn*, is called for training. All the documents in the data folder and all the positive phrases are combined (along with current document and phrases). The entire set is used for training. Current document and annotations file are stored in data folder.
* Function, *test*, is called for testing. The current test document and annotations file is used for testing.  
* *result* function is used to display the results page. Test results are extracted from file, "test/results_sentenceContainsTarget.db". The results are displayed in color-coded format. The sentences of test document which are labeled positive are in green and those labeled negative are red. Higher is the green intensity (RGB format) if the regression score is higher. Red is high if the regression score is more negative. 
* *create_files* function takes document and positive labels as inputs and converts them into files with predicates for training (using rnlp module).
* *get_pos_lines* function returns the lines from the document which have part of them labeled positive.
* *document_to_lines* function breaks down entire document into list of lines (Each line ends with '.').
* *get_pos_examples* returns a list of positive phrases read from file "train_pos_file".
* *get_doc_posExamples* puts together files in data directory to return a single document and list of positive phrases.
* *get_scores* function extracts scores of sentences in the test document from given file (Assuming has same format as "test/results_sentenceContainsTarget.db"). The scores for sentences are sorted in order in which they appear in the document.

## Documentation for  static/scripts/javascript.js
* *positiveSelectionTrain* function sends the text selected in the Text Editor for training to app.py via GET method.
* *positiveSelectionTest* function sends the text selected in the Text Editor for testing to app.py via GET method.