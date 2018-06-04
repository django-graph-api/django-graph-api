from graphql.ast import (
    FragmentDefinition,
    OperationDefinition,
)
from graphql.parser import GraphQLParser


class Request(object):
    def __init__(self, document, variables=None, operation_name=None):
        self.document = document
        self.variables = variables or {}
        self.operation_name = operation_name
        self._validated = False

        self.errors = []
        parser = GraphQLParser()

        if not self.document:
            self.errors.append('Must provide query string.')
        else:
            try:
                self.ast = parser.parse(self.document)
            except Exception as e:
                self.ast = None
                self.errors.append('Parse error: {}'.format(e))

        # Additional errors are meaningless if we couldn't parse the document
        if self.errors:
            self._validated = True

    @property
    def operation(self):
        if not hasattr(self, '_operation'):
            self._set_operation_and_fragments()
        if self._operation is None:
            raise Exception('Request document has no valid operation')
        return self._operation

    @property
    def fragments(self):
        if not hasattr(self, '_fragments'):
            self._set_fragments_and_fragments()
        return self._fragments

    def _set_operation_and_fragments(self):
        # This is a bit duplicative, but allows accessing these properties
        # without running validation.
        if self.ast is None:
            raise Exception('Request document is unparseable')

        operations = {}
        self._fragments = {}

        for definition in self.ast.definitions:
            if isinstance(definition, OperationDefinition):
                operations[definition.name] = definition
            elif isinstance(definition, FragmentDefinition):
                self._fragments[definition.name] = definition

        try:
            if self.operation_name:
                self._operation = operations[self.operation_name]
            else:
                self._operation = list(operations.values())[0]
        except (KeyError, IndexError):
            self._operation = None

    def validate(self):
        # Only validate once
        if self._validated:
            return
        self._validated = True

        self.perform_operation_validation()

    def perform_operation_validation(self):
        operations = {}
        fragments = {}
        for definition in self.ast.definitions:
            if isinstance(definition, OperationDefinition):
                if definition.name in operations:
                    self.errors.append('Non-unique operation name: {}'.format(definition.name))
                else:
                    operations[definition.name] = definition
            elif isinstance(definition, FragmentDefinition):
                if definition.name in fragments:
                    self.errors.append('Non-unique fragment name: {}'.format(definition.name))
                else:
                    fragments[definition.name] = definition

        if self.operation_name:
            if self.operation_name not in operations:
                self.errors.append('No operation found called `{}`'.format(self.operation_name))
        else:
            if len(operations) > 1:
                self.errors.append('Multiple operations provided but no operation name')
            elif len(operations) == 0:
                self.errors.append('At least one operation must be provided')
