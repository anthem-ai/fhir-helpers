from datetime import datetime
from typing import Callable, Generic, List, Optional, TypeVar

from ..utils import check_after_date, check_before_date
from .resource import Resource

T = TypeVar("T", bound=Resource)


class ResourceList(Generic[T]):
    # https://mypy.readthedocs.io/en/stable/more_types.html#precise-typing-of-alternative-constructors
    TResourceList = TypeVar("TResourceList", bound="ResourceList[T]")

    def __init__(self, items: List[T] = []):
        self._items: List[T] = items or []

    def all(self) -> List[T]:
        return [item for item in self._items]

    def add(self, item: T) -> None:
        self._items.append(item)

    def get(self, index: int) -> T:
        return self._items[index]

    def exists(self) -> bool:
        return len(self._items) > 0

    def first(self) -> Optional[T]:
        if not len(self._items):
            return None
        return self._items[0]

    def last(self) -> Optional[T]:
        if not len(self._items):
            return None
        return self._items[-1]

    def filter(self: TResourceList, filter_func: Callable[[T], bool]) -> TResourceList:
        return self.__class__(list(filter(filter_func, self._items)))

    def union(
        self: TResourceList,
        *args: TResourceList,
    ) -> TResourceList:
        item_set = set(self._items)
        for arg in args:
            item_set.update(arg._items)
        return self.__class__(list(item_set))

    def or_(
        self: TResourceList,
        *args: Callable[[TResourceList], TResourceList],
    ) -> TResourceList:
        item_set = set()
        for arg in args:
            item_set.update(arg(self)._items)
        return self.__class__(list(item_set))

    def find_by_text_match(self: TResourceList, search_str: str) -> TResourceList:
        return self.filter(lambda r: r.search_text(search_str))

    def find_after_date(self: TResourceList, after_date: datetime) -> TResourceList:
        return self.filter(lambda r: check_after_date(after_date, r._sort_date))

    def find_before_date(self: TResourceList, before_date: datetime) -> TResourceList:
        return self.filter(lambda r: check_before_date(before_date, r._sort_date))

    def sort_by_date(self: TResourceList, reverse: bool = False) -> TResourceList:
        return self.__class__(
            sorted(self._items, key=lambda r: r._sort_date, reverse=reverse)
        )

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self: TResourceList) -> TResourceList:
        self._index = 0
        return self

    def __next__(self) -> T:
        if self._index < len(self._items):
            ret_val = self._items[self._index]
            self._index += 1
            return ret_val
        else:
            raise StopIteration

    # def find_by_text_match(self, search_str: str) -> TResourceList:
    #     return Conditions(self._filter(lambda co: co.search_text(search_str)))
