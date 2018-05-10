# coding: utf-8
from graphql.ast import Variable

from django_graph_api import RelatedField
from django_graph_api.graphql.utils import GraphQLError


def validate_args(node):
    if node is None:
        return
    for field_name, field in node.fields.items():
        for arg_name, arg in field.arguments.items():
            validate_arg(arg_name, arg, field_name, field)
        if isinstance(field, RelatedField):
            obj_instance = field.get_object_instance()
            validate_args(obj_instance)


def get_arg_value(arg_name, field):
    query_arguments = {arg.name: arg.value for arg in field.selection.arguments}
    input_value = query_arguments.get(arg_name)

    def resolve_variables(value):
        if isinstance(value, Variable):
            variable_name = value.name
            default_value = field.obj.variable_definitions[variable_name].default_value
            value = field.obj.variables.get(variable_name, default_value)
        if isinstance(value, list):
            return [resolve_variables(item) for item in value]
        return value

    return resolve_variables(input_value)


def validate_arg(arg_name, arg, field_name, field):
    query_arguments = {arg.name: arg.value for arg in field.selection.arguments}

    if not arg.null:
        if arg_name not in query_arguments:
            raise GraphQLError(
                "Required argument '{}' on '{}' is missing".format(arg_name, field_name)
            )

    arg_value = get_arg_value(arg_name, field)
    if not is_arg_valid(arg, arg_value):
        raise GraphQLError("Argument '{}' on '{}' is invalid".format(arg_name, field_name))


def is_arg_valid(arg, arg_value):
    if not arg.null and arg_value is None:
        return False
    elif arg_value is None:
        return True
    if arg.kind == 'LIST':
        if len(arg_value) == 0:
            return is_arg_valid(arg.type_, None)
        else:
            for item in arg_value:
                if not is_arg_valid(arg.type_, item):
                    return False
    return True
