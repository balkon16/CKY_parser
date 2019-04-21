import os

class CFG_Error(Exception):
    def __init__(self, inconsistency, location):

        message = inconsistency + " Please check the line no. {}".format(location)
        # Call the base class constructor with the parameters it needs
        super().__init__(message)


def read_grammar_from_file(file_with_grammar):
    """
    Given a text file with rules in CFG form the function returns
    a dictionary indexed by the right-hand side and the left-hand side as
    corresponding values.

    The dictionary is based on CFG transformed into a grammar in Chomsky Normal
    Form.

    It is assumed that the file is stored in the project's directory at the top
    level. Each line must contain at most one rule. Each rule must be in the
    following form:
        NP -> Det N
        N -> "I"
        NP -> Det N PP

    It is allowed that the right-hand side contains an alternative. The example
    listed above can be summarised as follows:
        NP -> Det N PP | Det N
        N -> "I"

    Empty lines are ignored; incorrect lines raise an error. A line is considered
    incorrect if it fulfills at least one of the following conditions:
        a. contains either 0 or more than one arrows ("->")
        b. left-hand side is comprised of more than one non-terminals
        c. left-hand side contains a terminal symbol
        d. right-hand side is empty
    """

    try:
        if os.stat(file_with_grammar).st_size > 0:
           print("File has contents.")
        else:
           print("File is empty.")
    except OSError:
        print("No file {} found!".format(file_with_grammar))

    # create empty dict that the rules will be stored in
    rules = dict()

    print("Before with")
    with open(file_with_grammar, 'r') as file:
        for line_number, line in enumerate(file):
            # lines end with the new-line character "\n" - remove it
            line = line.rstrip()
            if line == "":
                # ignoring an empty line
                continue
            else:
                if "->" not in line:
                    raise CFG_Error("Rule must contain at least one arrow. ", \
                    line_number + 1)

                try:
                    lhs, rhs = line.split("->")
                except ValueError:
                    # the situation in which there are more than one arrow
                    # in the rule
                    raise CFG_Error("Rule must not contain more than one arrow. ", \
                    line_number + 1)

                # delete the trailing whitespace
                lhs = lhs.rstrip()

                lhs_list = lhs.split(" ")
                if len(lhs_list) > 1:
                    # left-hand side contains more than one symbol
                    # the symbol can be either terminal or non-terminal
                    terminals, non_terminals = 0, 0
                    for symbol in lhs_list:
                        if "'" in symbol:
                            terminals += 1
                        else:
                            non_terminals += 1

                    raise CFG_Error("The rule must contain exactly one " \
                    "non-terminal symbol on the left-hand side. {} terminal " \
                    "and {} non-terminal symbols were given.".format(terminals, \
                    non_terminals), line_number + 1)

                if rhs.rstrip() == "":
                    # right-hand side is empty
                    raise CFG_Error("Right-hand side is empty.", line_number + 1)
