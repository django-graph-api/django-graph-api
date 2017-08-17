class Field(object):
    # Tracks each time a Field instance is created. Used to retain order.
    creation_counter = 0

    def __init__(self):
        # Increase the creation counter, and save our local copy.
        self.creation_counter = Field.creation_counter
        Field.creation_counter += 1

    def get_value(self, arguments=None, fields=None):
        raise NotImplementedError

    def bind(self, name, node):
        self.name = name
        self.node = node
