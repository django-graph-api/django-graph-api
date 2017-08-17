from .parse import parse


class Schema(object):
    def __init__(self, query_node):
        self.query_node = query_node

    def execute(self, document):
        parsed = parse(document)
        return self.query_node.get_value(data=parsed)
