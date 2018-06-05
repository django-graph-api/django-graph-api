# coding: utf-8
from graphql.ast import (
    FragmentDefinition,
    OperationDefinition,
)

from django_graph_api import RelatedField
from django_graph_api.graphql.utils import GraphQLError


def validate_object_arguments(obj):
    if obj is None:
        return
    for field_name, field in obj.fields.items():
        validate_non_null_args(field_name, field)

        if isinstance(field, RelatedField):
            obj_instance = field.get_object_instance()
            validate_object_arguments(obj_instance)


def validate_non_null_args(field_name, field):
    """
    NonNull arguments are required and cannot be null
    """
    for arg_name, arg_type in field.arguments.items():
        if not arg_type.null and arg_name not in field.selection_arguments:
            raise GraphQLError("Required argument '{}' on '{}' is missing".format(arg_name, field_name))

        arg_value = field.selection_arguments.get(arg_name)
        if not non_null_arg_provided(arg_type, arg_value):
            raise GraphQLError("Non-null argument '{}' on '{}' is null".format(arg_name, field_name))


def non_null_arg_provided(arg_type, value):
    if not arg_type.null and value is None:
        return False
    elif value is None:
        return True

    if arg_type.kind == 'LIST':
        if len(value) == 0:
            return non_null_arg_provided(arg_type.type_, None)
        else:
            for item in value:
                if not non_null_arg_provided(arg_type.type_, item):
                    return False
    return True


def perform_operation_validation(request):
    errors = []
    operations = {}
    fragments = {}
    for definition in request.ast.definitions:
        if isinstance(definition, OperationDefinition):
            if definition.name in operations:
                raise GraphQLError('Non-unique operation name: {}'.format(definition.name))
            else:
                operations[definition.name] = definition
        elif isinstance(definition, FragmentDefinition):
            if definition.name in fragments:
                raise GraphQLError('Non-unique fragment name: {}'.format(definition.name))
            else:
                fragments[definition.name] = definition

    if request.operation_name:
        if request.operation_name not in operations:
            raise GraphQLError('No operation found called `{}`'.format(request.operation_name))
    else:
        if len(operations) > 1:
            raise GraphQLError('Multiple operations provided but no operation name')
        elif len(operations) == 0:
            raise GraphQLError('At least one operation must be provided')

    return errors


def perform_argument_validation(query_root):
    validate_object_arguments(query_root)


class Validation(object):
    def __init__(self, request, schema):
        self.request = request
        self.schema = schema
        self.errors = []
        self._validated = False

    def validate(self):
        if self._validated:
            return
        self._validated = True

        try:
            self.errors.extend(perform_operation_validation(self.request))

            query_root = self.schema.get_query_root(self.request)
            perform_argument_validation(query_root)

        except Exception as e:
            if not isinstance(e, GraphQLError):
                e = GraphQLError(e)
            self.errors.append(e)
