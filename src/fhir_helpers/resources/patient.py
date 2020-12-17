from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import List, Optional

from fhir_types import FHIR_Patient
from google.fhir import codes
from proto.google.fhir.proto.r4.core import codes_pb2
from proto.google.fhir.proto.r4.core.resources import patient_pb2

from ..utils import (  # search,; search_proto,
    convert_proto_date,
    convert_proto_date_time,
    get_years_since_date,
    parse_iso_date,
    parse_iso_datetime,
)
from .human_name import HumanName, HumanNameDict, HumanNameProto


class Patient(ABC):
    @property
    @abstractmethod
    def name(self) -> List[HumanName]:
        pass  # pragma: no cover

    @property
    @abstractmethod
    def gender(self) -> str:
        pass  # pragma: no cover

    @property
    @abstractmethod
    def birthdate(self) -> Optional[date]:
        pass  # pragma: no cover

    @property
    def display_name(self) -> str:
        if not len(self.name):
            return ""
        return self.name[0].display_name

    @property
    @abstractmethod
    def id(self) -> str:
        pass  # pragma: nocover

    @property
    def age(self) -> Optional[int]:
        if not self.birthdate:
            return None
        return get_years_since_date(self.birthdate)

    @property
    @abstractmethod
    def deceased_boolean(self) -> Optional[bool]:
        pass  # pragma: nocover

    @property
    @abstractmethod
    def deceased_datetime(self) -> Optional[datetime]:
        pass  # pragma: nocover

    @property
    def is_deceased(self) -> bool:
        return self.deceased_boolean or bool(self.deceased_datetime)


class PatientDict(Patient):
    def __init__(self, data: FHIR_Patient) -> None:
        self.data = data

    @property
    def name(self) -> List[HumanName]:
        human_names = self.data.get("name", [])
        return list(map(lambda n: HumanNameDict(n), human_names))

    @property
    def gender(self) -> str:
        return self.data.get("gender", "")

    @property
    def birthdate(self) -> Optional[date]:
        return parse_iso_date(self.data.get("birthDate", ""))

    @property
    def id(self) -> str:
        return self.data.get("id", "")

    @property
    def deceased_boolean(self) -> Optional[bool]:
        return self.data.get("deceasedBoolean", None)

    @property
    def deceased_datetime(self) -> Optional[datetime]:
        return parse_iso_datetime(self.data.get("deceasedDateTime", ""))


class PatientProto(Patient):
    def __init__(self, patient: patient_pb2.Patient) -> None:
        self.patient = patient

    @property
    def name(self) -> List[HumanName]:
        return list(map(lambda n: HumanNameProto(n), self.patient.name))

    @property
    def gender(self) -> str:
        # Is there a better way to do this?
        descriptor = (
            codes_pb2.AdministrativeGenderCode.Value.DESCRIPTOR.values_by_number[
                self.patient.gender.value
            ]
        )
        return codes.enum_value_descriptor_to_code_string(descriptor)

    @property
    def birthdate(self) -> Optional[date]:
        return convert_proto_date(self.patient.birth_date)

    @property
    def id(self) -> str:
        return self.patient.id.value

    @property
    def deceased_boolean(self) -> Optional[bool]:
        if self.patient.deceased.HasField("boolean"):
            return self.patient.deceased.boolean.value
        else:
            return None

    @property
    def deceased_datetime(self) -> Optional[datetime]:
        return convert_proto_date_time(self.patient.deceased.date_time)
