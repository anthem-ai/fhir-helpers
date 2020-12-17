from abc import abstractmethod
from datetime import datetime
from typing import Optional

from fhir_types import FHIR_AllergyIntolerance
from proto.google.fhir.proto.r4.core.resources import allergy_intolerance_pb2

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


class AllergyIntolerance(Resource):
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
        return ensure_non_null_date(self.onset_datetime)

    def __repr__(self) -> str:  # pragma: nocover
        return f"Onset: {self.onset_datetime} Code: {self.code.coding}"


class AllergyIntoleranceDict(AllergyIntolerance):
    def __init__(self, data: FHIR_AllergyIntolerance) -> None:
        self.data = data

    @property
    def onset_datetime(self) -> Optional[datetime]:
        return parse_iso_datetime(self.data.get("onsetDateTime", ""))

    @property
    def code(self) -> CodeableConcept:
        return CodeableConceptDict(self.data.get("code", {}))

    def search_text(self, search_str: str) -> bool:
        return search(self.data, search_str)


class AllergyIntoleranceProto(AllergyIntolerance):
    def __init__(self, data_proto: allergy_intolerance_pb2.AllergyIntolerance) -> None:
        self.data_proto = data_proto

    @property
    def onset_datetime(self) -> Optional[datetime]:
        return convert_proto_date_time(self.data_proto.onset.date_time)

    @property
    def code(self) -> CodeableConcept:
        return CodeableConceptProto(self.data_proto.code)

    def search_text(self, search_str: str) -> bool:
        return search_proto(self.data_proto, search_str)


class AllergyIntolerances(ResourceList[AllergyIntolerance]):
    def find_by_coding(
        self, code: str = "", system: str = "", display: str = ""
    ) -> "AllergyIntolerances":
        return self.filter(
            lambda allergy_intolerance: allergy_intolerance.code.has_coding(
                code, system, display
            )
        )
