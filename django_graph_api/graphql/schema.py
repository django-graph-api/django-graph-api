# coding: utf-8
from collections import OrderedDict

from django_graph_api.graphql import introspection
from django_graph_api.graphql.types import (
    Object,
    RelatedField,
    String,
)
from django_graph_api.graphql.utils import GraphQLError


class BaseQueryRoot(Object):
    """
    Provides basic functionality related to introspection.
    The query root for a graphql view should be a subclass of BaseQueryRoot.
    """
    introspection_fields = OrderedDict((
        ('__schema', RelatedField(introspection.Schema)),
        ('__type', RelatedField(
            introspection.Type,
            arguments={'name': String()},
        )),
    ))

    def get___schema(self):
        return self.__class__

    def get___type(self, name):
        schema = introspection.Schema(None, self.__class__, None)
        for type_ in schema.get_types():
            if type_.object_name == name:
                return type_
        return None


class Schema(object):
    def __init__(self, query_root_class=BaseQueryRoot):
        self.query_root_class = query_root_class

    def execute(self, request):
        query_root = self.query_root_class(
            ast=request.operation,
            data=None,
            fragments=request.fragments,
            variable_definitions={
                definition.name: definition
                for definition in request.operation.variable_definitions
            },
            variables=request.variables,
        )

        errors = self.validate(request)
        if errors:
            return None, errors

        return query_root.execute()

    def validate(self, request):
        query_root = self.query_root_class(
            ast=request.operation,
            data=None,
            fragments=request.fragments,
            variable_definitions={
                definition.name: definition
                for definition in request.operation.variable_definitions
            },
            variables=request.variables,
        )

        try:
            from django_graph_api.graphql.validation import validate_args
            validate_args(query_root)
        except (GraphQLError, ValueError) as e:
            return [e]
