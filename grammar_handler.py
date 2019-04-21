import os

class CFG_Error(Exception):
    def __init__(self, inconsistency, location):

        message = inconsistency + " Please check the line no. {}".format(location)
        # Call the base class constructor with the parameters it needs
        super().__init__(message)


def read_grammar_from_file(file_with_grammar):
    """
    Given a text file with rules in CFG form the function returns a list of two
    dictionaries:
        1. terminals dictionary that contains (terminal, category) pairs
        2. rules dictionary by the right-hand side and the left-hand side as
        corresponding values.
    The dictionaries contain rules in Context Free Grammar.

    It is assumed that the file is stored in the project's directory at the top
    level. Each line must contain at most one rule. Each rule must be in the
    following form:
        NP -> Det N
        N -> 'I'
        NP -> Det N PP
    Please note the single quotes around non-terminal symbols.

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
           pass
        else:
           print("File is empty.")
    except OSError:
        print("No file {} found!".format(file_with_grammar))

    # create empty dict that the rules will be stored in; covers rules that
    # don't contain terminal symbols
    rules = dict()

    # create empty dict that stores the terminal symbols and their categories
    terminals = dict()

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
                # delete the leading whitespace
                rhs = rhs.lstrip()
                print(rhs)

                if "'" in lhs:
                    # left-hand side contains a terminal symbol
                    raise CFG_Error("The rule must not contain a terminal " \
                    "symbol on the left-hand side.", line_number + 1)

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

                if lhs.rstrip() == "":
                    # left-hand side is empty
                    raise CFG_Error("Left-hand side is empty.", line_number + 1)

                for rhs_elem in rhs.split("|"):
                    # if there is more than one right-hand side element then it is
                    # isolated with a pipe ("|")

                    rhs_elem = rhs_elem.strip()

                    if "'" in rhs_elem:
                        # terminal symbol on the right-hand side
                        rhs_elem = rhs_elem.replace("'", "")
                        terminals[rhs_elem] = lhs
                    else:
                        # non-terminal symbol
                        rules[rhs_elem] = lhs

        return [terminals, rules]
