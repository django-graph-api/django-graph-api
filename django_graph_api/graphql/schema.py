from collections import OrderedDict

from django_graph_api.graphql import introspection
from django_graph_api.graphql.types import (
    Object,
    RelatedField,
    String,
)


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
