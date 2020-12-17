from abc import abstractmethod
from datetime import datetime
from typing import List

from fhir_types import FHIR_Encounter
from proto.google.fhir.proto.r4.core.resources import encounter_pb2

from ..utils import ensure_non_null_date, search, search_proto
from .codeable_concept import CodeableConcept, CodeableConceptDict, CodeableConceptProto
from .period import Period, PeriodDict, PeriodProto
from .resource import Resource
from .resource_list import ResourceList


class Encounter(Resource):
    @property
    @abstractmethod
    def period(self) -> Period:
        pass  # pragma: no cover

    @property
    @abstractmethod
    def type(self) -> List[CodeableConcept]:
        pass  # pragma: no cover

    @property
    def _sort_date(self) -> datetime:
        return ensure_non_null_date(self.period.start)


class EncounterDict(Encounter):
    def __init__(self, data: FHIR_Encounter) -> None:
        self.data = data

    @property
    def period(self) -> Period:
        return PeriodDict(self.data.get("period", {}))

    @property
    def type(self) -> List[CodeableConcept]:
        return [CodeableConceptDict(reason) for reason in self.data.get("type", [])]

    def search_text(self, search_str: str) -> bool:
        return search(self.data, search_str)


class EncounterProto(Encounter):
    def __init__(self, data_proto: encounter_pb2.Encounter) -> None:
        self.data_proto = data_proto

    @property
    def period(self) -> Period:
        return PeriodProto(self.data_proto.period)

    @property
    def type(self) -> List[CodeableConcept]:
        return [CodeableConceptProto(reason) for reason in self.data_proto.type]

    def search_text(self, search_str: str) -> bool:
        return search_proto(self.data_proto, search_str)


class Encounters(ResourceList[Encounter]):
    def find_by_coding(
        self, code: str = "", system: str = "", display: str = ""
    ) -> "Encounters":
        def has_coding(encounter: Encounter) -> bool:
            for reason in encounter.type:
                if reason.has_coding(code, system, display):
                    return True

            return False

        return self.filter(has_coding)
