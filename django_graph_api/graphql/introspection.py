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
    UNION,
    NonNull,
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


class InputValue(Object):
    object_name = '__InputValue'
    name = CharField()
    description = CharField()
    type = RelatedField(lambda: Type)
    defaultValue = CharField()

    def get_name(self):
        return self.data[0]

    def get_type(self):
        type_ = self.data[1]
        if not type_.null:
            return NonNull(type_)
        elif isinstance(type_, List):
            return type_
        return type_.__class__


class Directive(Object):
    object_name = '__Directive'
    name = CharField()
    description = CharField()
    locations = ManyEnumField(DirectiveLocationEnum)
    args = ManyRelatedField(InputValue)


class Field(Object):
    # self.data will be an item from a declared fields dict
    object_name = '__Field'
    name = CharField()
    description = CharField()
    type = RelatedField(lambda: Type)
    args = ManyRelatedField(InputValue)
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
            if not field.null:
                type_ = NonNull(type_)
        elif not field.null:
            type_ = NonNull(field.type_)
        else:
            type_ = field.type_
        return type_

    def get_args(self):
        return tuple(self.data[1].arguments.items())


class EnumValue(Object):
    object_name = '__EnumValue'
    name = CharField()
    description = CharField()
    isDeprecated = BooleanField()
    deprecationReason = CharField()


class Type(Object):
    # self.data will be an object or scalar
    object_name = '__Type'
    kind = EnumField(TypeKindEnum)
    name = CharField()
    description = CharField()
    fields = ManyRelatedField(Field)
    inputFields = ManyRelatedField(InputValue)
    interfaces = ManyRelatedField('self')
    possibleTypes = ManyRelatedField('self')
    enumValues = ManyRelatedField(EnumValue)
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
        if self.data.kind in [NON_NULL, LIST]:
            type_ = self.data.type_
            # Don't return NonNull if self is already NonNull
            if self.data.kind is not NON_NULL and not getattr(type_, 'null', True):
                return NonNull(type_)
            return type_
        return None


class Schema(Object):
    # self.data will be the query_root.
    object_name = '__Schema'
    types = ManyRelatedField(Type)
    queryType = RelatedField(Type)
    mutationType = RelatedField(Type)
    directives = ManyRelatedField(Directive)

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
            elif isinstance(field.type_, List):
                field = field.type_
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
        types = self._collect_types(self.data.query_root_class)
        return sorted(types, key=self._type_key)

    def get_queryType(self):
        return self.data.query_root_class

    def get_mutationType(self):
        return None

    def get_directives(self):
        return []
