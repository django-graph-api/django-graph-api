from graphql.ast import (
    FragmentDefinition,
    OperationDefinition,
)
from graphql.parser import GraphQLParser

from django_graph_api.graphql.schema import BaseQueryRoot


class Request(object):
    def __init__(self, document, variables=None, query_root_class=BaseQueryRoot, operation_name=None):
        self.document = document
        self.variables = variables or {}
        self.operation_name = operation_name
        self.query_root_class = query_root_class
        self._validated = False

        self.errors = []
        parser = GraphQLParser()
        try:
            self.ast = parser.parse(self.document)
        except Exception as e:
            self.ast = None
            self.errors.append('Parse error: {}'.format(e))
            # Additional errors are meaningless if we couldn't parse the document
            self._validated = True

    def validate(self):
        # Only validate once
        if self._validated:
            return
        self._validated = True

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
                self.errors.append('No operation found called `{}`'.format(self.operration_name))
        else:
            if len(operations) > 1:
                self.errors.append('Multiple operations provided but no operation name')
            elif len(operations) == 0:
                self.errors.append('At least one operation must be provided')

    def get_operation(self):
        # This is a bit duplicative, but allows us to fully separate execution
        # from validation.
        if self.ast is None:
            raise Exception('get_operation called on an unparseable document')

        operations = {}
        fragments = {}

        for definition in self.ast.definitions:
            if isinstance(definition, OperationDefinition):
                operations[definition.name] = definition
            elif isinstance(definition, FragmentDefinition):
                fragments[definition.name] = definition

        if self.operation_name:
            operation = operations[self.operation_name]
        else:
            operation = list(operations.values())[0]

        if operation is None:
            raise Exception('get_operation called on a document with no valid operation')

        return self.query_root_class(
            ast=operation,
            data=None,
            fragments=fragments,
            variable_definitions={
                definition.name: definition
                for definition in operation.variable_definitions
            },
            variables=self.variables,
        )
