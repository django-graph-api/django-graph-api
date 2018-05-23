# coding: utf-8

from django_graph_api import RelatedField
from django_graph_api.graphql.utils import GraphQLError


def validate_args(node):
    if node is None:
        return
    for field_name, field in node.fields.items():
        for arg_name, arg_type in field.arguments.items():
            validate_arg(arg_name, arg_type, field_name, field)
        if isinstance(field, RelatedField):
            obj_instance = field.get_object_instance()
            validate_args(obj_instance)


def validate_arg(arg_name, arg, field_name, field):
    if not arg.null:
        if arg_name not in field.selection_arguments:
            raise GraphQLError(
                "Required argument '{}' on '{}' is missing".format(arg_name, field_name)
            )

    arg_value = field.selection_arguments.get(arg_name)
    if not is_arg_valid(arg, arg_value):
        raise GraphQLError("Argument '{}' on '{}' is invalid".format(arg_name, field_name))


def is_arg_valid(arg_type, value):
    if not arg_type.null and value is None:
        return False
    elif value is None:
        return True

    if arg_type.kind == 'LIST':
        if len(value) == 0:
            return is_arg_valid(arg_type.type_, None)
        else:
            for item in value:
                if not is_arg_valid(arg_type.type_, item):
                    return False
    return True
