# coding: utf-8

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
            raise GraphQLError("Required non-null argument '{}' on '{}' is null".format(arg_name, field_name))


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
