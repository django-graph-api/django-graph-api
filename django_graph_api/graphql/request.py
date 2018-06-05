from graphql.ast import (
    FragmentDefinition,
    OperationDefinition,
)
from graphql.parser import GraphQLParser

from django_graph_api.graphql.utils import GraphQLError
from .validation import Validation


class Request(object):
    def __init__(self, document, schema, variables=None, operation_name=None):
        self.document = document
        self.variables = variables or {}
        self.operation_name = operation_name
        self.schema = schema
        self._validated = False
        self._errors = []
        parser = GraphQLParser()

        if not self.document:
            self._errors.append(GraphQLError('Must provide query string.'))
        else:
            try:
                self.ast = parser.parse(self.document)
            except Exception as e:
                self.ast = None
                self._errors.append(GraphQLError('Parse error: {}'.format(e)))

        # Additional errors are meaningless if we couldn't parse the document
        if self._errors:
            self._validated = True

    @property
    def errors(self):
        if self._validated:
            return self._errors

        self.validate()
        return self._errors

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
        if self._validated:
            return

        self._validated = True
        validation = Validation(self, self.schema)
        validation.validate()
        self._errors.extend(validation.errors)

    def execute(self):
        query_root = self.schema.get_query_root(self)
        data, errors = query_root.execute()
        self._errors.extend(errors)
        return data, errors
