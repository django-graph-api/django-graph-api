from collections import OrderedDict

from django.core.exceptions import ImproperlyConfigured

from django_graph_api.graphql import introspection
from django_graph_api.graphql.types import (
    Object,
    RelatedField,
    String,
)


class CombinedQueryRoot(Object):
    def __init__(self, query_root_classes=None, *args, **kwargs):
        super(CombinedQueryRoot, self).__init__(*args, **kwargs)
        self.query_roots = [
            cls(*args, **kwargs)
            for cls in (query_root_classes or [])
        ]

    def __getattr__(self, attr):
        # Delegate resolvers to the class that defined the field if they aren't
        # overridden on this class.
        if attr[:4] == 'get_':
            field_name = attr[4:]
            for query_root in self.query_roots:
                if field_name in query_root._declared_fields:
                    return getattr(query_root, attr)
        raise AttributeError('{} not found on {} or its query_root_classes'.format(
            attr,
            self.__class__.__name__,
        ))

    def get_declared_fields(self):
        _declared_fields = {}
        for query_root in self.query_roots:
            _declared_fields.update(query_root.get_declared_fields())
        return _declared_fields


class IntrospectionQueryRoot(Object):
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
    def __init__(self, query_root_classes=None):
        self.query_root_classes = [
            IntrospectionQueryRoot,
        ] + (query_root_classes or [])

        # Catch duplicate fields as early as possible.
        seen_fields = {}
        for cls in self.query_root_classes:
            for field_name in cls._declared_fields:
                seen_fields.setdefault(field_name, []).append(cls)

        if any(len(classes) > 1 for classes in seen_fields.values()):
            error_str = '\n'.join(
                '{} field is defined on multiple classes: {}'.format(
                    field_name,
                    ', '.join(cls.__name__ for cls in classes)
                )
                for field_name, classes in seen_fields.items()
                if len(classes) > 1
            )
            raise ImproperlyConfigured(error_str)

    def execute(self, request):
        query_root = CombinedQueryRoot(
            query_root_classes=self.query_root_classes,
            ast=request.operation,
            data=None,
            fragments=request.fragments,
            variable_definitions={
                definition.name: definition
                for definition in request.operation.variable_definitions
            },
            variables=request.variables,
        )
        return query_root.execute()
