from django_graph_api.graphql.utils import (
    GraphQLError
)
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

    @property
    def errors(self):
        if not hasattr(self, '_errors'):
            self.validate()
        return self._errors

    def validate(self):
        self.operations = {}
        self.operation = None
        self.fragments = {}
        self._errors = []

        parser = GraphQLParser()

        try:
            self.ast = parser.parse(self.document)
        except Exception as e:
            self._errors.append('Parse error: {}'.format(e))
            # Additional errors are meaningless if we couldn't parse the document
            return

        for definition in self.ast.definitions:
            if isinstance(definition, OperationDefinition):
                if definition.name in self.operations:
                    self._errors.append('Non-unique operation name: {}'.format(definition.name))
                else:
                    self.operations[definition.name] = definition
            elif isinstance(definition, FragmentDefinition):
                if definition.name in self.fragments:
                    self._errors.append('Non-unique fragment name: {}'.format(definition.name))
                else:
                    self.fragments[definition.name] = definition

        if self.operation_name:
            try:
                self.operation = self.operations[self.operation_name]
            except KeyError:
                self._errors.append('No operation found called `{}`'.format(self.operration_name))
        else:
            if len(self.operations) > 1:
                self._errors.append('Multiple operations provided but no operation name')
            elif len(self.operations) == 0:
                self._errors.append('At least one operation must be provided')
            else:
                self.operation = list(self.operations.values())[0]

        if self.operation:
            self.variable_definitions = {
                definition.name: definition
                for definition in self.operation.variable_definitions
            }
            self.query_root = self.query_root_class(
                ast=self.operation,
                data=None,
                fragments=self.fragments,
                variable_definitions=self.variable_definitions,
                variables=self.variables,
            )

    def execute(self):
        if self.errors:
            return None, self.errors
        return self.query_root.serialize(), self.query_root.errors
