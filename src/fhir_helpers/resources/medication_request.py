from abc import abstractmethod
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from fhir_types import FHIR_MedicationRequest
from proto.google.fhir.proto.r4.core.resources import medication_request_pb2

from ..utils import (
    convert_proto_date_time,
    ensure_non_null_date,
    parse_iso_datetime,
    search,
    search_proto,
)
from .codeable_concept import CodeableConcept, CodeableConceptDict, CodeableConceptProto
from .practitioner import Practitioner
from .reference import Reference, ReferenceDict, ReferenceProto
from .resource import Resource
from .resource_list import ResourceList

if TYPE_CHECKING:  # pragma: no cover
    from .lpr import LPR


class MedicationRequest(Resource):
    @property
    @abstractmethod
    def authored_on(self) -> Optional[datetime]:
        pass  # pragma: no cover

    @property
    @abstractmethod
    def medication_codeable_concept(self) -> CodeableConcept:
        pass  # pragma: no cover

    @property
    @abstractmethod
    def requester(self) -> Reference:
        pass  # pragma: no cover

    @property
    def requester_practitioner(self) -> Optional[Practitioner]:
        requester_reference = self.requester.reference
        requester_id = requester_reference.split(":")[-1]
        return self.lpr.practitioners.find_by_id(requester_id)

    @property
    @abstractmethod
    def status(self) -> str:
        pass  # pragma: no cover

    @property
    def _sort_date(self) -> datetime:
        return ensure_non_null_date(self.authored_on)


class MedicationRequestDict(MedicationRequest):
    def __init__(self, data: FHIR_MedicationRequest, lpr: "LPR") -> None:
        self.data = data
        super().__init__(lpr)

    @property
    def authored_on(self) -> Optional[datetime]:
        return parse_iso_datetime(self.data.get("authoredOn", ""))

    @property
    def medication_codeable_concept(self) -> CodeableConcept:
        return CodeableConceptDict(self.data.get("medicationCodeableConcept", {}))

    @property
    def requester(self) -> Reference:
        return ReferenceDict(self.data.get("requester", {}))

    @property
    def status(self) -> str:
        return self.data.get("status", "")

    def search_text(self, search_str: str) -> bool:
        return search(self.data, search_str)


class MedicationRequestProto(MedicationRequest):
    def __init__(
        self, medication_request: medication_request_pb2.MedicationRequest, lpr: "LPR"
    ) -> None:
        self.medication_request = medication_request
        super().__init__(lpr)

    @property
    def authored_on(self) -> Optional[datetime]:
        return convert_proto_date_time(self.medication_request.authored_on)

    @property
    def medication_codeable_concept(self) -> CodeableConcept:
        return CodeableConceptProto(self.medication_request.medication.codeable_concept)

    @property
    def requester(self) -> Reference:
        return ReferenceProto(self.medication_request.requester)

    @property
    def status(self) -> str:
        # There's no easy to get the string out of protobuf. It looks like this:
        # "value: ACTIVE\n"
        return str(self.medication_request.status).split(" ")[1].strip().lower()

    def search_text(self, search_str: str) -> bool:
        return search_proto(self.medication_request, search_str)


class MedicationRequests(ResourceList[MedicationRequest]):
    def find_by_coding(
        self, code: str = "", system: str = "", display: str = ""
    ) -> "MedicationRequests":
        return self.filter(
            lambda mr: mr.medication_codeable_concept.has_coding(code, system, display)
        )
