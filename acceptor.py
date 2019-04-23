from cell import Cell

rules = ['S -> NP VP',
 'PP -> P NP',
 'NP -> Det N',
 'NP -> X1 PP',
 'X1 -> Det N',
 "NP -> 'I'",
 'VP -> V NP',
 'VP -> VP PP',
 "Det -> 'an'",
 "Det -> 'my'",
 "N -> 'elephant'",
 "N -> 'pajamas'",
 "V -> 'shot'",
 "P -> 'in'"]

tokens = "I shot an elephant in my pajamas".split()

def initialise_matrix(sentence, grammar):
    """
    """
    tokens = sentence.split()

    no_tokens = len(tokens)

    matrix = [[None for i in range(no_tokens+1)] for j in range(no_tokens+1)]

    for i in range(no_tokens):
        category = get_tokens_category(tokens[i], grammar)
        # tutaj powinienem jakoś zatrzymać informację o słowie (np. 'shot')
        # może trzeba użyć nltk.Tree
        matrix[i][i+1] = Cell(category)

    return matrix

def get_tokens_category(token, grammar):
    """
    # TODO: napisać opis pod ostateczną implemetancję
    """
    # # TODO: kiedy już będziesz miał działającą zamienę na CFG na CNF zmienić
    # implementację tej funkcji na taką, która będzie przyjmowała słownik
    # parametryzowany listą i zwracała kategorię (kategorie to klucze)
    # czas dostępu będzie O(n*m) (przy liście jest O(n)), gdzie n to liczba kluczy
    # a m to długość listy pod kluczem (zazwyczaj 1)
    for rule in rules:
        if "'" in rule:
            LHS, RHS = rule.split(" -> ")
            RHS = RHS.replace("'", "")
            if token == RHS:
                return LHS

def init_wfst(tokens, grammar):
    numtokens = len(tokens)
    wfst = [[None for i in range(numtokens+1)] for j in range(numtokens+1)]
    for i in range(numtokens):
        category = get_tokens_category(tokens[i], grammar)
        wfst[i][i+1] = category
    return wfst

def display(wfst):
    print('\nWFST ' + ' '.join(("%-4d" % i) for i in range(1, len(wfst))))
    for i in range(len(wfst)-1):
        print("%d   " % i, end=" ")
        for j in range(1, len(wfst)):
            print("%-4s" % (wfst[i][j] or '.'), end=" ")
        print()

def complete_wfst(wfst, tokens, grammar, trace=False):
    index = dict((p.rhs(), p.lhs()) for p in grammar.productions())
    numtokens = len(tokens)
    for span in range(2, numtokens+1):
        for start in range(numtokens+1-span):
            end = start + span
            for mid in range(start+1, end):
                nt1, nt2 = wfst[start][mid], wfst[mid][end]
                if nt1 and nt2 and (nt1,nt2) in index:
                    wfst[start][end] = index[(nt1,nt2)]
                    if trace:
                        print("[%s] %3s [%s] %3s [%s] ==> [%s] %3s [%s]" % \
                        (start, nt1, mid, nt2, end, start, index[(nt1,nt2)], end))
    return wfst



if __name__ == "__main__":
    # print(get_tokens_category('my', rules))
    # print(get_tokens_category('elephant', rules))
    # print(get_tokens_category('pajamas', rules))
    # print(init_wfst(tokens, rules))
    # initialised_wfst = init_wfst(tokens, rules)
    # display(initialised_wfst)
    macierz = initialise_matrix("I shot an elephant in my pajamas", rules)
    print(macierz)
