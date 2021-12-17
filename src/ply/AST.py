class ASTNode:
    def __init__(self, type, *childs):
        self.type = type
        self.childs = list(childs)

    def print(self, depth = 0):
        print('\t' * depth, end = '')
        print(self.type)
        for child in self.childs:
            if not isinstance(child, ASTNode):
                raise RuntimeError(child)
            child.print(depth = depth+1)
        
