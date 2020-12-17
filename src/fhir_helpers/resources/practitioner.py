from abc import abstractmethod
from datetime import datetime
from typing import List, Optional

from fhir_types import FHIR_Practitioner
from google.fhir import codes
from proto.google.fhir.proto.r4.core import codes_pb2
from proto.google.fhir.proto.r4.core.resources import practitioner_pb2

from ..utils import ensure_non_null_date, search, search_proto
from .human_name import HumanName, HumanNameDict, HumanNameProto
from .resource import Resource
from .resource_list import ResourceList


class Practitioner(Resource):
    @property
    @abstractmethod
    def id(self) -> str:
        pass  # pragma: no cover

    @property
    @abstractmethod
    def name(self) -> List[HumanName]:
        pass  # pragma: no cover

    @property
    @abstractmethod
    def gender(self) -> str:
        pass  # pragma: no cover

    @property
    def _sort_date(self) -> datetime:
        return ensure_non_null_date(None)


class PractitionerDict(Practitioner):
    def __init__(self, data: FHIR_Practitioner) -> None:
        self.data = data

    @property
    def id(self) -> str:
        return self.data.get("id", "")

    @property
    def name(self) -> List[HumanName]:
        human_names = self.data.get("name", [])
        return list(map(lambda n: HumanNameDict(n), human_names))

    @property
    def gender(self) -> str:
        return self.data.get("gender", "")

    def search_text(self, search_str: str) -> bool:
        return search(self.data, search_str)


class PractitionerProto(Practitioner):
    def __init__(self, practitioner: practitioner_pb2.Practitioner) -> None:
        self.practitioner = practitioner

    @property
    def id(self) -> str:
        return self.practitioner.id.value

    @property
    def name(self) -> List[HumanName]:
        return list(map(lambda n: HumanNameProto(n), self.practitioner.name))

    @property
    def gender(self) -> str:
        # Is there a better way to do this?
        descriptor = (
            codes_pb2.AdministrativeGenderCode.Value.DESCRIPTOR.values_by_number[
                self.practitioner.gender.value
            ]
        )
        return codes.enum_value_descriptor_to_code_string(descriptor)

    def search_text(self, search_str: str) -> bool:
        return search_proto(self.practitioner, search_str)


class Practitioners(ResourceList[Practitioner]):
    def find_by_id(self, id: str) -> Optional["Practitioner"]:
        practicioners = self.filter(lambda prac: prac.id == id)
        if not practicioners:
            return None
        # if more than one practicioner there is an issue
        return practicioners.get(0)
