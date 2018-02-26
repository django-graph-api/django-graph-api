import copy

from graphql.ast import (
    FragmentDefinition,
    Query,
)
from graphql.parser import GraphQLParser
from django_graph_api.graphql.types import (
    BooleanField,
    CharField,
    Enum,
    ENUM,
    EnumField,
    INPUT_OBJECT,
    INTERFACE,
    List,
    LIST,
    ManyEnumField,
    ManyRelatedField,
    NON_NULL,
    Object,
    OBJECT,
    RelatedField,
    SCALAR,
    String,
    UNION,
    NonNull)
from django_graph_api.graphql.utils import (
    format_error,
    GraphQLError
)


class DirectiveLocationEnum(Enum):
    object_name = '__DirectiveLocation'
    values = (
        {
            'name': 'QUERY',
            'description': None,
            'isDeprecated': False,
            'deprecationReason': None,
        },
        {
            'name': 'MUTATION',
            'description': None,
            'isDeprecated': False,
            'deprecationReason': None,
        },
        {
            'name': 'FIELD',
            'description': None,
            'isDeprecated': False,
            'deprecationReason': None,
        },
        {
            'name': 'FRAGMENT_DEFINITION',
            'description': None,
            'isDeprecated': False,
            'deprecationReason': None,
        },
        {
            'name': 'FRAGMENT_SPREAD',
            'description': None,
            'isDeprecated': False,
            'deprecationReason': None,
        },
        {
            'name': 'INLINE_FRAGMENT',
            'description': None,
            'isDeprecated': False,
            'deprecationReason': None,
        },
    )


class TypeKindEnum(Enum):
    object_name = '__TypeKind'
    values = (
        {
            'name': SCALAR,
            'description': None,
            'isDeprecated': False,
            'deprecationReason': None,
        },
        {
            'name': OBJECT,
            'description': None,
            'isDeprecated': False,
            'deprecationReason': None,
        },
        {
            'name': INTERFACE,
            'description': None,
            'isDeprecated': False,
            'deprecationReason': None,
        },
        {
            'name': UNION,
            'description': None,
            'isDeprecated': False,
            'deprecationReason': None,
        },
        {
            'name': ENUM,
            'description': None,
            'isDeprecated': False,
            'deprecationReason': None,
        },
        {
            'name': INPUT_OBJECT,
            'description': None,
            'isDeprecated': False,
            'deprecationReason': None,
        },
        {
            'name': LIST,
            'description': None,
            'isDeprecated': False,
            'deprecationReason': None,
        },
        {
            'name': NON_NULL,
            'description': None,
            'isDeprecated': False,
            'deprecationReason': None,
        },
    )


class InputValueObject(Object):
    object_name = '__InputValue'
    name = CharField()
    description = CharField()
    type = RelatedField(lambda: TypeObject)
    defaultValue = CharField()

    def get_name(self):
        return self.data[0]

    def get_type(self):
        type_ = self.data[1]
        if isinstance(type_, List):
            return type_
        return type_.__class__


class DirectiveObject(Object):
    object_name = '__Directive'
    name = CharField()
    description = CharField()
    locations = ManyEnumField(DirectiveLocationEnum)
    args = ManyRelatedField(InputValueObject)


class FieldObject(Object):
    # self.data will be an item from a declared fields dict
    object_name = '__Field'
    name = CharField()
    description = CharField()
    type = RelatedField(lambda: TypeObject)
    args = ManyRelatedField(InputValueObject)
    isDeprecated = BooleanField()
    deprecationReason = CharField()

    def get_name(self):
        return self.data[0]

    def get_description(self):
        return getattr(self.data[1], 'description', None)

    def get_type(self):
        field = self.data[1]
        if isinstance(field, RelatedField):
            type_ = field.object_type
            if isinstance(field.type_, List):
                type_ = List(type_)
            elif not field.nullable:
                type_ = NonNull(type_)
        elif not field.nullable:
            type_ = NonNull(field.type_)
        else:
            type_ = field.type_
        return type_

    def get_args(self):
        return tuple(self.data[1].arguments.items())


class EnumValueObject(Object):
    object_name = '__EnumValue'
    name = CharField()
    description = CharField()
    isDeprecated = BooleanField()
    deprecationReason = CharField()


class TypeObject(Object):
    # self.data will be an object or scalar
    object_name = '__Type'
    kind = EnumField(TypeKindEnum)
    name = CharField()
    description = CharField()
    fields = ManyRelatedField(FieldObject)
    inputFields = ManyRelatedField(InputValueObject)
    interfaces = ManyRelatedField('self')
    possibleTypes = ManyRelatedField('self')
    enumValues = ManyRelatedField(EnumValueObject)
    ofType = RelatedField('self')

    def get_name(self):
        if self.data.kind in [LIST, NON_NULL]:
            return None
        return self.data.object_name

    def get_fields(self):
        if self.data.kind != OBJECT:
            return None
        return sorted(
            (
                (name, field)
                for name, field in self.data._declared_fields.items()
                if name[:2] != '__'
            ),
            key=lambda item: item[0],
        )

    def get_inputFields(self):
        if self.data.kind != INPUT_OBJECT:
            return None

        return []

    def get_interfaces(self):
        if self.data.kind != OBJECT:
            return None
        return []

    def get_possibleTypes(self):
        return None

    def get_enumValues(self):
        if self.data.kind != ENUM:
            return None

        return self.data.values

    def get_ofType(self):
        if self.data.kind in [LIST, NON_NULL]:
            return self.data.type_
        return None


class SchemaObject(Object):
    # self.data will be the query_root.
    object_name = '__Schema'
    types = ManyRelatedField(TypeObject)
    queryType = RelatedField(TypeObject)
    mutationType = RelatedField(TypeObject)
    directives = ManyRelatedField(DirectiveObject)

    def _collect_types(self, object_type, types=None):
        if types is None:
            types = set((object_type,))
        for field in object_type._declared_fields.values():
            if isinstance(field, RelatedField):
                object_type = field.object_type
                if object_type in types:
                    continue
                types.add(object_type)
                self._collect_types(object_type, types)
            elif isinstance(field, EnumField):
                enum_type = field.enum
                if enum_type in types:
                    continue
                types.add(enum_type)
            elif field.type_:
                types.add(field.type_)
        return types

    def _type_key(self, type_):
        object_name = type_.object_name
        # Sort: defined types, introspection types, scalars, and then by name.
        return (
            type_.kind == SCALAR,
            object_name.startswith('__'),
            object_name,
        )

    def get_types(self):
        types = self._collect_types(self.data)
        return sorted(types, key=self._type_key)

    def get_queryType(self):
        return self.data

    def get_mutationType(self):
        return None

    def get_directives(self):
        return []


class Schema(object):
    """
    Required for a GraphQL API.

    A schema is a set of nodes and edges with at least one query root to access the rest of
    the schema.

    To use:
    ::

        schema = Schema()

        @schema.register_query_root
        class QueryRoot(Object):
            hello = CharField()

            def get_hello(self):
                return 'world'

    Each GraphQLView is mapped to a single schema.
    ::

        urlpatterns = [
            url(r'^graphql$', GraphQLView.as_view(schema=schema)),
        ]
    """
    def __init__(self):
        self.query_root = None

    def register_query_root(self, BaseQueryRoot):
        class QueryRoot(BaseQueryRoot):
            def get___schema(self):
                return self.__class__

            def get___type(self, name):
                schema = SchemaObject(None, self.__class__, None)
                for type_ in schema.get_types():
                    if type_.object_name == name:
                        return type_
                return None
        QueryRoot._declared_fields = copy.deepcopy(BaseQueryRoot._declared_fields)
        QueryRoot._declared_fields['__schema'] = RelatedField(SchemaObject)
        QueryRoot._declared_fields['__type'] = RelatedField(
            TypeObject,
            arguments={'name': String()},
        )

        self.query_root = QueryRoot
        return QueryRoot

    def _extract_query(self, ast):
        queries = [
            definition for definition in ast.definitions
            if isinstance(definition, Query)
        ]
        assert len(queries) == 1, "Exactly one query must be defined"
        query = queries[0]
        return query

    def execute(self, document, variables=None):
        """
        Queries the schema in python.

        :param document: A GraphQL query string
        :return: JSON of returned data or errors

        e.g.
        ::

            query = '''
            {
                users {
                    name
                }
            }
            '''
            schema.execute(query)

        Might return
        ::

            {
                "data": {
                    "users": [
                        {"name": "Buffy Summers"},
                        {"name": "Willow Rosenberg"},
                        {"name": "Xander Harris"}
                    ]
                }
            }
        """
        errors = []
        ast = None
        query = None
        data = None
        parser = GraphQLParser()
        try:
            ast = parser.parse(document)
        except Exception as e:
            errors.append(GraphQLError('Parse error: {}'.format(e)))

        if ast:
            try:
                query = self._extract_query(ast)
            except AssertionError as e:
                errors.append(GraphQLError('Document error: {}'.format(e)))

        if query and ast:
            fragments = {
                definition.name: definition
                for definition in ast.definitions
                if isinstance(definition, FragmentDefinition)
            }

            variable_definitions = {
                definition.name: definition
                for definition in query.variable_definitions
            }

            try:
                query = self.query_root(
                    ast=query,
                    data=None,
                    fragments=fragments,
                    variable_definitions=variable_definitions,
                    variables=variables
                )
                data = query.serialize()
                errors.extend(query.errors)
            except Exception as e:
                errors.append(GraphQLError('Unexpected query error: {}'.format(e)))

        result = {}
        if data:
            result['data'] = data

        if len(errors) > 0:
            result['errors'] = [format_error(error) for error in errors]

        return result


schema = Schema()
