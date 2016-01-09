from template import expr_node
from template.node import Node


class ForNode(Node):
    def __init__(self, var, constraint):
        self.constraint = constraint
        self.var = var
        self.children = []

    def eval(self, context):
        results = []
        for i in eval(self.constraint, {}, context):
            context[self.var] = i
            for child in self.children:
                results.append(child.eval(context))
        return ''.join(results)