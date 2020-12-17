from abc import ABC, abstractmethod

from fhir_types import FHIR_Coding
from proto.google.fhir.proto.r4.core import datatypes_pb2


class Coding(ABC):
    @property
    @abstractmethod
    def code(self) -> str:
        pass  # pragma: no cover

    @property
    @abstractmethod
    def system(self) -> str:
        pass  # pragma: no cover

    @property
    @abstractmethod
    def display(self) -> str:
        pass  # pragma: no cover

    def __repr__(self) -> str:  # pragma: nocover
        return f"Code: {self.code} System: {self.system} Display: {self.display}"


class CodingDict(Coding):
    def __init__(self, data: FHIR_Coding) -> None:
        self.data = data

    @property
    def code(self) -> str:
        return self.data.get("code", "")

    @property
    def system(self) -> str:
        return self.data.get("system", "")

    @property
    def display(self) -> str:
        return self.data.get("display", "")


class CodingProto(Coding):
    def __init__(self, coding: datatypes_pb2.Coding) -> None:
        self.coding = coding

    @property
    def code(self) -> str:
        return self.coding.code.value

    @property
    def system(self) -> str:
        return self.coding.system.value

    @property
    def display(self) -> str:
        return self.coding.display.value
