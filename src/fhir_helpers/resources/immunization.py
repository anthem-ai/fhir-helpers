from abc import abstractmethod
from datetime import datetime
from typing import Optional

from fhir_types import FHIR_Immunization
from proto.google.fhir.proto.r4.core.resources import immunization_pb2

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


class Immunization(Resource):
    @property
    @abstractmethod
    def occurrence_datetime(self) -> Optional[datetime]:
        pass  # pragma: no cover

    @property
    @abstractmethod
    def vaccine_code(self) -> CodeableConcept:
        pass  # pragma: no cover

    @property
    def _sort_date(self) -> datetime:
        return ensure_non_null_date(self.occurrence_datetime)


class ImmunizationDict(Immunization):
    def __init__(self, data: FHIR_Immunization) -> None:
        self.data = data

    @property
    def occurrence_datetime(self) -> Optional[datetime]:
        return parse_iso_datetime(self.data.get("occurrenceDateTime", ""))

    @property
    def vaccine_code(self) -> CodeableConcept:
        return CodeableConceptDict(self.data.get("vaccineCode", {}))

    def search_text(self, search_str: str) -> bool:
        return search(self.data, search_str)


class ImmunizationProto(Immunization):
    def __init__(self, data_proto: immunization_pb2.Immunization) -> None:
        self.data_proto = data_proto

    @property
    def occurrence_datetime(self) -> Optional[datetime]:
        return convert_proto_date_time(self.data_proto.occurrence.date_time)

    @property
    def vaccine_code(self) -> CodeableConcept:
        return CodeableConceptProto(self.data_proto.vaccine_code)

    def search_text(self, search_str: str) -> bool:
        return search_proto(self.data_proto, search_str)


class Immunizations(ResourceList[Immunization]):
    def find_by_coding(
        self, code: str = "", system: str = "", display: str = ""
    ) -> "Immunizations":
        return self.filter(
            lambda immunization: immunization.vaccine_code.has_coding(
                code, system, display
            )
        )
