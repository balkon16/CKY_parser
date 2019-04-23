class Cell:
    """
    # # TODO: napisać opis
    """
    def __init__(self, symbol, child1, child2=None):
        self.symbol = symbol
        self.child1 = [child1]
        if child2:
            self.child2 = [child2]
        else:
            self.child2 = []

    def __repr__(self):
        return self.symbol

    def add_children(self, first_child=None, second_child=None):
        if first_child:
            self.child1.append(first_child)
        if second_child:
            self.child2.append(second_child)

if __name__ == "__main__":
    cell0 = Cell("AB", 'string')
    cell1 = Cell("V", cell0)
    cell2 = Cell("VP", cell0, cell1)
    print(cell1)
    print(cell2)
    cell2.add_children(cell1)
