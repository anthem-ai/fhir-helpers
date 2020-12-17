from abc import abstractmethod
from datetime import datetime
from typing import Optional

from fhir_types import FHIR_Condition
from proto.google.fhir.proto.r4.core.resources import condition_pb2

from ..utils import (
    convert_proto_date_time,
    ensure_non_null_date,
    parse_iso_datetime,
    search,
    search_proto,
)
from .codeable_concept import CodeableConcept, CodeableConceptDict, CodeableConceptProto
from .resource import Resource
from .resource_list import ResourceList


class Condition(Resource):
    @property
    @abstractmethod
    def recorded_date(self) -> Optional[datetime]:
        pass  # pragma: no cover

    @property
    @abstractmethod
    def onset_datetime(self) -> Optional[datetime]:
        pass  # pragma: no cover

    @property
    @abstractmethod
    def code(self) -> CodeableConcept:
        pass  # pragma: no cover

    @property
    def _sort_date(self) -> datetime:
        return ensure_non_null_date(self.recorded_date or self.onset_datetime)


class ConditionDict(Condition):
    def __init__(self, data: FHIR_Condition) -> None:
        self.data = data

    @property
    def recorded_date(self) -> Optional[datetime]:
        return parse_iso_datetime(self.data.get("recordedDate", ""))

    @property
    def onset_datetime(self) -> Optional[datetime]:
        return parse_iso_datetime(self.data.get("onsetDateTime", ""))

    @property
    def code(self) -> CodeableConcept:
        return CodeableConceptDict(self.data.get("code", {}))

    def search_text(self, search_str: str) -> bool:
        return search(self.data, search_str)


class ConditionProto(Condition):
    def __init__(self, condition: condition_pb2.Condition) -> None:
        self.condition = condition

    @property
    def recorded_date(self) -> Optional[datetime]:
        return convert_proto_date_time(self.condition.recorded_date)

    @property
    def onset_datetime(self) -> Optional[datetime]:
        return convert_proto_date_time(self.condition.onset.date_time)

    @property
    def code(self) -> CodeableConcept:
        return CodeableConceptProto(self.condition.code)

    def search_text(self, search_str: str) -> bool:
        return search_proto(self.condition, search_str)


class Conditions(ResourceList[Condition]):
    def find_by_coding(
        self, code: str = "", system: str = "", display: str = ""
    ) -> "Conditions":
        return self.filter(lambda ob: ob.code.has_coding(code, system, display))
