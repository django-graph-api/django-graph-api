from traceback import format_exc

from django.conf import settings
from graphql.ast import (
    Field,
    FragmentSpread,
    InlineFragment,
)
from graphql.error.format_error import format_error as graphql_core_format_error
from graphql.error.base import GraphQLError as GraphQLCoreError


def get_selections(selections, fragments, object_type, seen_fragments=None):
    _selections = []

    if seen_fragments is None:
        seen_fragments = set()

    for selection in selections:
        if isinstance(selection, Field):
            _selections.append(selection)
            continue

        if isinstance(selection, FragmentSpread):
            fragment = fragments[selection.name]
        elif isinstance(selection, InlineFragment):
            fragment = selection

        # If the fragment doesn't apply to the current object, don't
        # add its selections. This could happen for example if this is
        # a union of different object types with different fields for
        # each type.
        if fragment.type_condition.name != object_type.object_name:
            continue

        # Skip fragments we've already seen to avoid recursion issues.
        if hasattr(fragment, 'name'):
            if fragment.name in seen_fragments:
                continue
            else:
                seen_fragments.add(fragment.name)

        _selections += get_selections(
            selections=fragment.selections,
            fragments=fragments,
            object_type=object_type,
            seen_fragments=seen_fragments,
        )

    return _selections


def format_error(error):
    formatted_error = graphql_core_format_error(error)

    if settings.DEBUG:
        formatted_error['traceback'] = error.traceback
    return formatted_error


class GraphQLError(GraphQLCoreError):
    def __init__(self, *args, **kwargs):
        super(GraphQLError, self).__init__(*args, **kwargs)
        if settings.DEBUG:
            self.traceback = format_exc().split('\n')
