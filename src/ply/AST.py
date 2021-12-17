class ASTNode:
    def __init__(self, type, *childs):
        self.type = type
        self.childs = list(childs)

    def print(self, depth = 0):
        """
        递归打印节点与子节点

        :param depth int: 深度值（默认为0）
        :raises RuntimeError: 子节点类型不为ASTNode
        """
        print('\t' * depth, end = '')
        print(self.type)
        for child in self.childs:
            if not isinstance(child, ASTNode):
                raise RuntimeError(child)
            child.print(depth = depth+1)
        
