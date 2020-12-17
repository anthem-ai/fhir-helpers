from abc import abstractmethod
from datetime import datetime
from typing import Optional

from fhir_types import FHIR_Procedure
from proto.google.fhir.proto.r4.core.resources import procedure_pb2

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


class Procedure(Resource):
    @property
    @abstractmethod
    def performed_datetime(self) -> Optional[datetime]:
        pass  # pragma: no cover

    @property
    @abstractmethod
    def code(self) -> CodeableConcept:
        pass  # pragma: no cover

    @property
    def _sort_date(self) -> datetime:
        return ensure_non_null_date(self.performed_datetime)


class ProcedureDict(Procedure):
    def __init__(self, data: FHIR_Procedure) -> None:
        self.data = data

    # Check 2 possible locations for start_date in procedure
    @property
    def performed_datetime(self) -> Optional[datetime]:
        return parse_iso_datetime(
            self.data.get("performedDateTime", "")
        ) or parse_iso_datetime(self.data.get("performedPeriod", {}).get("start", ""))

    @property
    def code(self) -> CodeableConcept:
        return CodeableConceptDict(self.data.get("code", {}))

    def search_text(self, search_str: str) -> bool:
        return search(self.data, search_str)


class ProcedureProto(Procedure):
    def __init__(self, procedure: procedure_pb2.Procedure) -> None:
        self.procedure = procedure

    # Check 2 possible locations for start_date in procedure
    @property
    def performed_datetime(self) -> Optional[datetime]:
        return convert_proto_date_time(
            self.procedure.performed.date_time
        ) or convert_proto_date_time(self.procedure.performed.period.start)

    @property
    def code(self) -> CodeableConcept:
        return CodeableConceptProto(self.procedure.code)

    def search_text(self, search_str: str) -> bool:
        return search_proto(self.procedure, search_str)


class Procedures(ResourceList[Procedure]):
    def find_by_coding(
        self, code: str = "", system: str = "", display: str = ""
    ) -> "Procedures":
        return self.filter(lambda proc: proc.code.has_coding(code, system, display))
