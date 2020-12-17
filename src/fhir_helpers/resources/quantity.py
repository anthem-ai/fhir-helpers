from abc import ABC, abstractmethod
from typing import Optional

from fhir_types import FHIR_Quantity
from proto.google.fhir.proto.r4.core import datatypes_pb2

from ..utils import ComparatorFunc, ComparatorType


class Quantity(ABC):
    @property
    @abstractmethod
    def value(self) -> Optional[float]:
        pass  # pragma: no cover

    @property
    @abstractmethod
    def unit(self) -> str:
        pass  # pragma: no cover

    @property
    @abstractmethod
    def code(self) -> str:
        pass  # pragma: no cover

    @property
    @abstractmethod
    def system(self) -> str:
        pass  # pragma: no cover

    def empty(self) -> bool:
        return self.value is None

    def match(
        self,
        comparator: ComparatorType,
        value_num: float,
        unit_str: str = "",
        system_str: str = "",
        code_str: str = "",
    ) -> bool:
        if self.empty():
            return False
        if unit_str and self.unit != unit_str:
            return False
        if system_str and self.system != system_str:
            return False
        if code_str and self.code != code_str:
            return False
        return ComparatorFunc[comparator](self.value, value_num) is True


class QuantityDict(Quantity):
    def __init__(self, data: FHIR_Quantity) -> None:
        self.data = data

    @property
    def value(self) -> Optional[float]:
        return self.data.get("value", None)

    @property
    def unit(self) -> str:
        return self.data.get("unit", "")

    @property
    def code(self) -> str:
        return self.data.get("code", "")

    @property
    def system(self) -> str:
        return self.data.get("system", "")


class QuantityProto(Quantity):
    def __init__(self, quantity: datatypes_pb2.Quantity) -> None:
        self.quantity = quantity

    @property
    def value(self) -> Optional[float]:
        # This is a string type in protobuf. Could use Decimal?
        return float(self.quantity.value.value) if self.quantity.value.value else None

    @property
    def unit(self) -> str:
        return self.quantity.unit.value

    @property
    def code(self) -> str:
        return self.quantity.code.value

    @property
    def system(self) -> str:
        return self.quantity.system.value
