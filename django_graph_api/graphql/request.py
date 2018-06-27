from graphql.ast import (
    FragmentDefinition,
    OperationDefinition,
)
from graphql import exceptions as graphql_exceptions
from graphql.parser import GraphQLParser

from django_graph_api.graphql.utils import GraphQLError
from .validation import (
    perform_operation_validation,
    perform_argument_validation
)


class Request(object):
    def __init__(self, document, schema, variables=None, operation_name=None):
        """
        Creates a Request object that can be validated and executed.

        :param document: The query string to execute.

            e.g. ``"query episodeNames { episodes { name } }"``

        :param schema: A Schema object to run the query against
        :param variables: A ``dict`` of variables to pass to the query (optional)
        :param operation_name: If the document contains multiple named queries,
            the name of the query to execute (optional)
        """
        self.document = document
        self.variables = variables or {}
        self.operation_name = operation_name
        self.schema = schema
        self._validated = False
        self._errors = []
        self.query_root = None
        parser = GraphQLParser()

        if not self.document:
            self._errors.append(GraphQLError('Must provide query string.'))
        else:
            try:
                self.ast = parser.parse(self.document)
            except (graphql_exceptions.LexerError, graphql_exceptions.SyntaxError) as e:
                self.ast = None
                self._errors.append(GraphQLError(
                    'Parse error: {}'.format(e),
                    line=e.line,
                    column=e.column,
                ))

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
        """
        Used to perform validation of a query before execution.
        Errors produced from validation can be accessed
        from ``request.errors``.

        If a Request object has been validated once,
        additional calls will not re-run validation.
        """
        if self._validated:
            return

        self._validated = True

        try:
            self._errors.extend(perform_operation_validation(self))
            if self._errors:  # If the request is invalid, stop validation
                return

            self.query_root = self.schema.get_query_root(self)
            self._errors.extend(perform_argument_validation(self.query_root))

        except Exception as e:
            if not isinstance(e, GraphQLError):
                e = GraphQLError(e)
            self.errors.append(e)

    def execute(self):
        """
        :return: data, errors
        """
        query_root = self.schema.get_query_root(self)
        data, errors = query_root.execute()
        self._errors.extend(errors)
        return data, errors
