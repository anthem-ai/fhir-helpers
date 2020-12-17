from abc import ABC, abstractmethod
from typing import List

from fhir_types import FHIR_CodeableConcept
from proto.google.fhir.proto.r4.core import datatypes_pb2

from .coding import Coding, CodingDict, CodingProto


class CodeableConcept(ABC):
    @property
    @abstractmethod
    def coding(self) -> List[Coding]:
        pass  # pragma: no cover

    def empty(self) -> bool:
        return len(self.coding) == 0

    def has_coding(
        self, code_str: str = "", system_str: str = "", display_str: str = ""
    ) -> bool:
        for coding in self.coding:
            if code_str and coding.code != code_str:
                continue
            if system_str and coding.system != system_str:
                continue
            if display_str and coding.display != display_str:
                continue
            return True
        return False


class CodeableConceptDict(CodeableConcept):
    def __init__(self, data: FHIR_CodeableConcept) -> None:
        self.data = data

    @property
    def coding(self) -> List[Coding]:
        return list(map(lambda c: CodingDict(c), self.data.get("coding", [])))


class CodeableConceptProto(CodeableConcept):
    def __init__(
        self,
        concept: datatypes_pb2.CodeableConcept,
    ) -> None:
        self.concept = concept

    @property
    def coding(self) -> List[Coding]:
        return list(map(lambda c: CodingProto(c), self.concept.coding))
