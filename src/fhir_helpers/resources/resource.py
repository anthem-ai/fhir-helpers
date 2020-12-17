from abc import ABC, abstractmethod
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from .lpr import LPR


class Resource(ABC):
    def __init__(self, lpr: "LPR"):
        self.lpr = lpr

    # @property
    # @abstractmethod
    # def id(self) -> str:
    #     pass

    @property
    @abstractmethod
    def _sort_date(self) -> datetime:
        pass  # pragma: no cover

    @abstractmethod
    def search_text(self, search_str: str) -> bool:
        pass  # pragma: no cover
