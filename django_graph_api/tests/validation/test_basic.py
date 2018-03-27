from django_graph_api.graphql.request import Request


def test_blank_query(starwars_data):
    document = ''
    request = Request(document)
    request.validate()
    assert request.errors == [
        'Parse error: Unexpected end of input',
    ]
