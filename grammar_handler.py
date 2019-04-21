import os

def read_grammar_from_file(file_with_grammar):
    """
    Given a text file with rules in Chomsky Normal Form the function returns
    a dictionary indexed by the right-hand side and the left-hand side as
    corresponding values.

    It is assumed that the file is stored in the project's directory at the top
    level.
    """

    try:
        if os.stat(file_with_grammar).st_size > 0:
           print("File has contents.")
        else:
           print("File is empty.")
    except OSError:
        print("No file {} found!".format(file_with_grammar))
