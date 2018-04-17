# coding: utf-8
from graphql.ast import Variable

from django_graph_api import (
    RelatedField,
    ManyRelatedField,
)
from django_graph_api.graphql.utils import GraphQLError


def validate_args(node):
    if node is None:
        return
    for field_name, field in node.fields.items():
        query_arguments = {arg.name: arg.value for arg in field.selection.arguments}
        for arg_name, arg in field.arguments.items():
            if not arg.null:
                if arg_name not in query_arguments:
                    raise GraphQLError(
                        "Required argument '{}' on '{}' is missing".format(arg_name, field_name)
                    )
                else:
                    input_value = query_arguments[arg_name]
                    if isinstance(input_value, Variable):
                        variable_name = input_value.name
                        default_value = field.obj.variable_definitions[variable_name].default_value
                        input_value = field.obj.variables.get(variable_name, default_value)
                    if input_value is None:
                        raise GraphQLError(
                            "Required argument '{}' on '{}' cannot be null".format(arg_name, field_name)
                        )
        if isinstance(field, ManyRelatedField):
            try:
                obj_instances = field.get_objects()
            except:
                return
            if obj_instances:
                for obj in obj_instances:
                    validate_args(obj)
        elif isinstance(field, RelatedField):
            try:
                obj_instance = field.get_object()
            except:
                return
            validate_args(obj_instance)
