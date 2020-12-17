from abc import abstractmethod
from datetime import datetime
from typing import Optional

from fhir_types import FHIR_MedicationDispense
from proto.google.fhir.proto.r4.core.resources import medication_dispense_pb2

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


class MedicationDispense(Resource):
    @property
    @abstractmethod
    def when_handed_over(self) -> Optional[datetime]:
        pass  # pragma: no cover

    @property
    @abstractmethod
    def medication_codeable_concept(self) -> CodeableConcept:
        pass  # pragma: no cover

    @property
    @abstractmethod
    def status(self) -> str:
        pass  # pragma: no cover

    @property
    def _sort_date(self) -> datetime:
        return ensure_non_null_date(self.when_handed_over)


class MedicationDispenseDict(MedicationDispense):
    def __init__(self, data: FHIR_MedicationDispense) -> None:
        self.data = data

    @property
    def when_handed_over(self) -> Optional[datetime]:
        return parse_iso_datetime(self.data.get("whenHandedOver", ""))

    @property
    def medication_codeable_concept(self) -> CodeableConcept:
        return CodeableConceptDict(self.data.get("medicationCodeableConcept", {}))

    @property
    def status(self) -> str:
        return self.data.get("status", "")

    def search_text(self, search_str: str) -> bool:
        return search(self.data, search_str)


class MedicationDispenseProto(MedicationDispense):
    def __init__(
        self, medication_dispense: medication_dispense_pb2.MedicationDispense
    ) -> None:
        self.medication_dispense = medication_dispense

    @property
    def when_handed_over(self) -> Optional[datetime]:
        return convert_proto_date_time(self.medication_dispense.when_handed_over)

    @property
    def medication_codeable_concept(self) -> CodeableConcept:
        return CodeableConceptProto(
            self.medication_dispense.medication.codeable_concept
        )

    @property
    def status(self) -> str:
        # There's no easy to get the string out of protobuf. It looks like this:
        # "value: COMPLETED\n"
        return str(self.medication_dispense.status).split(" ")[1].strip().lower()

    def search_text(self, search_str: str) -> bool:
        return search_proto(self.medication_dispense, search_str)


class MedicationDispenses(ResourceList[MedicationDispense]):
    def find_by_coding(
        self, code: str = "", system: str = "", display: str = ""
    ) -> "MedicationDispenses":
        return self.filter(
            lambda mr: mr.medication_codeable_concept.has_coding(code, system, display)
        )
