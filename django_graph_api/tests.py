class MySchema(Schema):
    hello = StringField(default='world')


def test_execute_query(schema):
    query_str = '''
    {
        hello
    }
    '''
    assert MySchema().execute(query_str) == {'hello': 'world'}


