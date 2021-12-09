class ASTNode:
    def __init__(self, type, *args):
        self.type = type
        self.l = [type] + list(args)

class AST:
    def __init__(self):
        self.root = ASTNode("pseudo")
        self.step = []

