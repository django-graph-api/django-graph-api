from graphql.ast import (
    Field,
    FragmentSpread,
    InlineFragment,
)


def get_selections(selections, fragments, object_type):
    _selections = []

    for selection in selections:
        if isinstance(selection, Field):
            _selections.append(selection)
            continue

        if isinstance(selection, FragmentSpread):
            fragment = fragments[selection.name]
        elif isinstance(selection, InlineFragment):
            fragment = selection

        if fragment.type_condition.name != object_type.object_name:
            continue

        _selections += get_selections(fragment.selections, fragments, object_type)

    return _selections
