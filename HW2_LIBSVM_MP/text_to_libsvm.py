__author__ = 'Balry - Michael Perez'
# Homework 2 program to convert provided documents into LIBSVM format .txt files.
import textmining

# February 2017
# NLP Homework 2 program to convert train & test text data to libsvm format -> <label> <index>:<value> <index>:<value>
# Program requires users to download textmining pip and pre-process text by removing stopwords and stemming words.
# Furthermore text files must be formatted as follows:
# <class-label> \t <text-document> \n
# Make sure to edit the class_label_to_number switcher categories to your class-labels and file paths
#
# VERY IMPORTANT LAST STEP: textmining -> __init__.py -> def rows(self, cutoff=2) must be edited as follows:
# line 315: #yield words
# The textmining files are located at "\Lib\site-packages\textmining" inside your Python root folder

# Python dictionary as switch statement.
def class_label_to_number(cat):
    switcher = {
        "student": 1,
        "faculty": 2,
        "project": 3,
        "course": 4
    }
    return switcher.get(cat, "0")

# Function that reads datasets formatted as follows:
# <class-label> \t <text-document> \n
# args: file_path -> string
#       libsvm -> list
#       docs -> list
#       tdm -> TermDocumentMatrix()
def read_file_text(file_path, libsvm, docs, tdm):
    # File not found error handle.
    try:
        # Read file line by line.
        with open(file_path) as input_file:
            for doc in input_file:
                # Split the first word from the rest of the document.
                temp_doc = doc.partition('\t')
                # Add numeralized class labels to the libsvm.
                libsvm.append(str(class_label_to_number(temp_doc[0])))
                # Strip label and \t leading tokens and place on docs object.
                temp_doc = temp_doc[2].strip('\n') + '\n'
                # Add text content to docs object
                docs.append(temp_doc)
                # Add text content to term-document matrix
                tdm.add_doc(temp_doc)
    except:
        error_message = 'File ' + input_path[0] + ' not found.'
        exit(error_message)
    input_file.close()

# Create lists for input and output file paths.
input_paths = []
output_paths = []

# Insert file paths into lists.
input_paths.append('./hw2_files/Datasets/webkb-train-stemmed.txt')
input_paths.append('./hw2_files/Datasets/webkb-test-stemmed.txt')
output_paths.append('./hw2_files/Output/webkb-train-libsvm.txt')
output_paths.append('./hw2_files/Output/webkb-test-libsvm.txt')

# Lists containing documents separated by training and testing file
docs_tr = []
docs_ts = []

# Lists that will contain the libsvm formatted documents separated by training and testing file
libsvm_tr = []
libsvm_ts = []

# Initialize class to create term-document matrix
tdm = textmining.TermDocumentMatrix()

# Use function to process files
read_file_text(input_paths[0], libsvm_tr, docs_tr, tdm)
read_file_text(input_paths[1], libsvm_ts, docs_ts, tdm)

# Offset for test data output
offset_ts = len(docs_tr)
# get tdm rows -> MAKE SURE TO EDIT textmining __init__.py as instructed above
tdm_rows = tdm.rows(cutoff=1)

# Converting training and testing text data to libsvm format
for tdm_rows_index, row in enumerate(tdm_rows):
    for row_index, term_frequency in enumerate(row):
        if (term_frequency >= 1) and (tdm_rows_index<len(docs_tr)):
            libsvm_tr[tdm_rows_index] += " " + str(row_index + 1) + ":" + str(term_frequency)
        if (term_frequency >= 1) and (tdm_rows_index>=len(docs_tr)):
            libsvm_ts[tdm_rows_index - offset_ts] += " " + str(row_index + 1) + ":" + str(term_frequency)

# Output files to specified path
with open(output_paths[0], 'w') as output_file:
    for item in libsvm_tr:
        output_file.write(item + '\n')
    output_file.close()
with open(output_paths[1], 'w') as output_file:
    for item in libsvm_ts:
        output_file.write(item + '\n')
    output_file.close()