import os
from collections import defaultdict

class CFG_Error(Exception):
    def __init__(self, inconsistency, location=None):

        message = inconsistency
        if location:
            message += " Please check the line no. {}".format(location)
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
        AP -> Adj
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
            raise CFG_Error("The file is empty")
    except OSError:
        print("No file {} found!".format(file_with_grammar))

    # create empty dict that the rules will be stored in; covers rules that
    # don't contain terminal symbols
    rules = defaultdict(list)

    # create empty dict that stores the terminal symbols and their categories
    terminals = defaultdict(list)

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

                if "'" in lhs:
                    # left-hand side contains a terminal symbol
                    raise CFG_Error("The rule must not contain a terminal " \
                    "symbol on the left-hand side.", line_number + 1)

                lhs_list = lhs.split(" ")
                if len(lhs_list) > 1:
                    # left-hand side contains more than one symbol
                    # the symbol can be either terminal or non-terminal
                    terminals_cnt, non_terminals_cnt = 0, 0
                    for symbol in lhs_list:
                        if "'" in symbol:
                            terminals_cnt += 1
                        else:
                            non_terminals_cnt += 1

                    raise CFG_Error("The rule must contain exactly one " \
                    "non-terminal symbol on the left-hand side. {} terminal " \
                    "and {} non-terminal symbols were given.".format(terminals_cnt, \
                    non_terminals_cnt), line_number + 1)

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
                        # terminals[rhs_elem].append(lhs)
                        terminals[lhs].append(rhs_elem)
                    else:
                        # non-terminal symbol
                        rules[rhs_elem].append(lhs)

        return [terminals, rules]

def transform_into_CNF(dicts):
    """
    Given a two-element list of dictionaries (each containing terminal and
    non-terminal portion of the CFG grammar) returns a list of those two
    dictionaries but in Chomsky Normal Form. Please note that dictionaries
    are transformed in-place.

    Each and every Context Free Grammar can be expressed in Chomsky Normal Form.
    There are three problematic situations:
        1. Right-hand side mixes terminals with non-terminals.
        2. Right-hand side is a single non-terminal.
        3. Right-hand side is of length greater than 2.

    Unit productions refer to situation no. 2. They are dealt with by finding
    such a rule producing a terminal symbol that:
        A -> B (unit production)
        B -> a
        ______
        A -> a (no unit production)

    Normalization is used in order to deal with a situaion described in step no.
    3. Let's assume the following rule:
        A -> B C D E
    By producing intermediary rules based on the left-most two strings of the
    RHS we can get to Chomksy Normal Form rule:
        step 1:
            A -> X1 D E
            X1 -> B C
        step 2:
            A -> X2 E
            X1 -> B C
            X2 -> X1 D

    Note: the current implementation does not cover the case in which a terminal
    part of the CFG contains a RHS with terminal and at least one non-terminal
    symbol. NotImplementedError is raised.
    """

    terminals, rules = dicts

    for terminal_LHS in terminals.keys():
        if len(terminal_LHS.split(" ")) > 1:
            raise NotImplementedError

    # variable used in order to track the use of intermediary rules (see
    # normalization)
    normalization_tracker = 0

    # it may be the case that the normaliztion process will produce a dictionary
    # items that start with the already existing keys. In order to avoid
    # overwriting the current key, value pair a temporary dictionary is created
    temporary_rules_dict = defaultdict(list)

    # Given the fact that the rules' dictionary has right-hand sides as the keys,
    # and that some RHS are too long for CFG, those RHS do not constitute a valid
    # key and thus must be deleted
    keys_to_remove = []

    # the list will be used to store unit productions, i.e. rules such as A -> B
    unit_productions = []

    for RHS, LHS in rules.items():
        # print(LHS, "->", RHS)

        RHS_symbols = RHS.split(" ")
        if len(RHS_symbols) == 1:
            # find a chain that leads the LHS to a terminal symbol
            # unit_productions.append(LHS, RHS)
            pass
            # zaimplementować: może być na sam koniec; jeżeli na koniec to
            # usuń regułę PP -> NP


        elif len(RHS_symbols) > 2:
            # normalization is needed

            keys_to_remove.append(RHS)

            while len(RHS_symbols) > 2:
                tmp_RHS_list = RHS_symbols[:2]
                tmp_LHS = "X" + str(normalization_tracker)

                temporary_rules_dict[" ".join(tmp_RHS_list)].append(tmp_LHS)

                RHS_symbols.pop(0)
                RHS_symbols[0] = tmp_LHS

                normalization_tracker += 1


            # this is the link between the original input dictionary and the
            # temporary dict
            # note that use the first and only element of the LHS list
            temporary_rules_dict[" ".join(RHS_symbols)].append(LHS[0])

    # integrate temporary dictionary with the original (input) one:
    for RHS_tmp, LHS_tmp in temporary_rules_dict.items():
        rules[RHS_tmp].append(LHS_tmp[0])

    # delete the rules that contain too long a right-hand side
    for key in keys_to_remove:
        rules.pop(key, None)

    return rules
