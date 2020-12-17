from datetime import datetime

from fhir_helpers.resources.resource import Resource
from fhir_helpers.resources.resource_list import ResourceList


class ExampleResource(Resource):
    def __init__(
        self, sort_date: datetime = datetime(2019, 1, 1), is_true: bool = True
    ) -> None:
        self._date_time = sort_date
        self._is_true = is_true

    @property
    def _sort_date(self) -> datetime:
        return self._date_time

    @property
    def is_true(self) -> bool:
        return self._is_true

    def search_text(self, search_str: str) -> bool:
        return True


def test_resource_list() -> None:

    resource_list = ResourceList[ExampleResource]()

    assert not resource_list.exists()
    assert not resource_list.first()
    assert not resource_list.last()

    items = [
        ExampleResource(),
        ExampleResource(),
        ExampleResource(),
    ]

    for item in items:
        resource_list.add(item)

    assert resource_list.first() == items[0]
    assert resource_list.last() == items[2]

    assert len(resource_list) == len(items)
    assert len(resource_list.all()) == len(items)
    assert resource_list.exists()


def test_iterator() -> None:
    items = [
        ExampleResource(),
        ExampleResource(),
        ExampleResource(),
    ]

    resource_list = ResourceList[ExampleResource](items)

    for index, el in enumerate(resource_list):
        assert el == items[index]
        # Test get function
        assert el == resource_list.get(index)

    # Do twice to ensure properties are reset
    for index, el in enumerate(resource_list):
        assert el == items[index]


def test_date_functions() -> None:

    resource_a = ExampleResource(datetime(2018, 1, 1))
    resource_b = ExampleResource(datetime(2019, 1, 1))
    resource_c = ExampleResource(datetime(2020, 1, 1))

    resource_list = ResourceList[ExampleResource]([resource_b, resource_c, resource_a])

    assert len(resource_list.find_after_date(datetime(2018, 2, 1))) == 2
    assert len(resource_list.find_before_date(datetime(2018, 2, 1))) == 1

    sorted_resource_list = resource_list.sort_by_date()
    assert sorted_resource_list.get(0) == resource_a
    assert sorted_resource_list.get(1) == resource_b
    assert sorted_resource_list.get(2) == resource_c

    sorted_resource_list_reverse = resource_list.sort_by_date(reverse=True)
    assert sorted_resource_list_reverse.get(0) == resource_c
    assert sorted_resource_list_reverse.get(1) == resource_b
    assert sorted_resource_list_reverse.get(2) == resource_a


def test_filter_function() -> None:
    items = [
        ExampleResource(is_true=True),
        ExampleResource(is_true=True),
        ExampleResource(is_true=False),
    ]

    resource_list = ResourceList[ExampleResource](items)

    assert len(resource_list.filter(lambda i: i.is_true)) == 2


def test_union_function() -> None:

    resource_a = ExampleResource()
    resource_b = ExampleResource()
    resource_c = ExampleResource()

    resource_list_a = ResourceList[ExampleResource]([resource_a, resource_b])
    resource_list_b = ResourceList[ExampleResource]([resource_b, resource_c])

    union_1 = ResourceList[ExampleResource]().union(resource_list_a, resource_list_b)
    union_2 = resource_list_a.union(resource_list_b)

    assert len(union_1) == 3
    assert len(union_2) == 3


def test_or_function() -> None:

    resource_a = ExampleResource()
    resource_b = ExampleResource(is_true=False)
    resource_c = ExampleResource()

    resource_list_a = ResourceList[ExampleResource](
        [resource_a, resource_b, resource_c]
    )

    or_1 = resource_list_a.or_(lambda r_list: r_list.filter(lambda r: r.is_true))
    or_2 = resource_list_a.or_(
        lambda r_list: r_list.filter(lambda r: r.is_true),
        lambda r_list: r_list.filter(lambda r: not r.is_true),
    )
    # test filter duplicates
    or_3 = resource_list_a.or_(
        lambda r_list: r_list.filter(lambda r: r.is_true),
        lambda r_list: r_list.filter(lambda r: r.is_true),
        lambda r_list: r_list.filter(lambda r: not r.is_true),
    )

    assert len(or_1) == 2
    assert len(or_2) == 3
    assert len(or_3) == 3
