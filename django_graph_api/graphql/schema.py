# coding: utf-8
from collections import OrderedDict
import copy

from django.core.exceptions import ImproperlyConfigured
import six

from django_graph_api.graphql import introspection
from django_graph_api.graphql.types import (
    Object,
    ObjectMetaclass,
    RelatedField,
    String,
)


class CombinedQueryRootMetaclass(ObjectMetaclass):
    def __new__(mcs, name, bases, attrs):
        cls = super(CombinedQueryRootMetaclass, mcs).__new__(mcs, name, bases, attrs)

        # Disallow explicit declared fields on combined query roots. They
        # must only "inherit" fields.
        if cls._declared_fields:
            raise ImproperlyConfigured('CombinedQueryRoot may not declare fields')

        # Disallow duplicate fields on query roots.
        query_root_classes = attrs.get('query_root_classes', [])
        seen_fields = {}
        for query_root_class in query_root_classes:
            for field_name in query_root_class._declared_fields:
                seen_fields.setdefault(field_name, []).append(query_root_class)

        if any(len(classes) > 1 for classes in seen_fields.values()):
            error_str = '\n'.join(
                '{} field is defined on multiple classes: {}'.format(
                    field_name,
                    ', '.join(query_root_class.__name__ for query_root_class in classes)
                )
                for field_name, classes in seen_fields.items()
                if len(classes) > 1
            )
            raise ImproperlyConfigured(error_str)

        # Collect declared fields from all query root classes.
        for query_root_class in query_root_classes:
            cls._declared_fields.update(copy.deepcopy(query_root_class._declared_fields))

        return cls


class CombinedQueryRoot(six.with_metaclass(CombinedQueryRootMetaclass, Object)):
    def __init__(self, *args, **kwargs):
        super(CombinedQueryRoot, self).__init__(*args, **kwargs)

        self.query_roots = [
            cls(*args, **kwargs)
            for cls in (self.query_root_classes or [])
        ]

    def __getattr__(self, attr):
        # Delegate resolvers to the class that defined the field if they aren't
        # overridden on this class.
        if attr[:4] == 'get_':
            field_name = attr[4:]
            for query_root in self.query_roots:
                if field_name in query_root._declared_fields:
                    return getattr(query_root, attr)
            raise AttributeError('{} resolver not found on {} or its query_root_classes'.format(
                attr,
                self.__class__.__name__,
            ))
        raise AttributeError("{} instance has no attribute '{}'".format(
            self.__class__.__name__,
            attr,
        ))


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
        return self.data

    def get___type(self, name):
        schema = introspection.Schema(None, self.data, None)
        for type_ in schema.get_types():
            if type_.object_name == name:
                return type_
        return None


class Schema(object):
    def __init__(self, query_root_classes=None):
        """
        Creates a schema that supports introspection.

        If multiple query root objects are passed in,
        their fields will be combined into the schema's root query.

        :param query_root_classes: an individual or list of query root objects
        """
        all_query_root_classes = [
            IntrospectionQueryRoot,
        ]
        if query_root_classes:
            try:
                all_query_root_classes.extend(query_root_classes)
            except TypeError:
                all_query_root_classes.append(query_root_classes)

        class QueryRoot(CombinedQueryRoot):
            query_root_classes = all_query_root_classes

        self.query_root_class = QueryRoot

    def get_query_root(self, request):
        return self.query_root_class(
            ast=request.operation,
            data=self,
            fragments=request.fragments,
            variable_definitions={
                definition.name: definition
                for definition in request.operation.variable_definitions
            },
            variables=request.variables,
        )
