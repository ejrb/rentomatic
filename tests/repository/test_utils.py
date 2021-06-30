from rentomatic.repository.utils import DictFilter


def test_dict_filter_should_filter():

    df = DictFilter()

    items = [{'foo': 'bar'}]
    assert list(df.apply(items)) == items


def test_dict_filter_from_queries():

    df = DictFilter.from_queries({
        'foo__eq': 'bar'
    })

    items = [{'foo': 'bar'},
             {'foo': 'baz'}]

    filtered_items = list(df.apply(items))

    assert len(filtered_items) == 1
    assert filtered_items[0]['foo'] == 'bar'
