from abc import ABC, abstractmethod

from fhir_types import FHIR_Reference
from proto.google.fhir.proto.r4.core import datatypes_pb2


class Reference(ABC):
    @property
    @abstractmethod
    def reference(self) -> str:
        pass  # pragma: no cover

    @property
    @abstractmethod
    def display(self) -> str:
        pass  # pragma: no cover


class ReferenceDict(Reference):
    def __init__(self, data: FHIR_Reference) -> None:
        self.data = data

    @property
    def reference(self) -> str:
        return self.data.get("reference", "")

    @property
    def display(self) -> str:
        return self.data.get("display", "")


class ReferenceProto(Reference):
    def __init__(self, data_proto: datatypes_pb2.Reference) -> None:
        self.data_proto = data_proto

    @property
    def reference(self) -> str:
        return self.data_proto.uri.value

    @property
    def display(self) -> str:
        return self.data_proto.display.value
