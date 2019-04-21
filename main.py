import pprint

from grammar_handler import *

pp = pprint.PrettyPrinter(indent=4)

terminals, rules = read_grammar_from_file("./dane_testowe/test_grammar.txt")

print("Terminals: ")
pp.pprint(terminals)
print("Rules: ")
pp.pprint(rules)
