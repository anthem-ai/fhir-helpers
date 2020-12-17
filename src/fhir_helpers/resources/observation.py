from abc import abstractmethod
from datetime import datetime
from typing import List, Optional

from fhir_types import FHIR_Observation
from proto.google.fhir.proto.r4.core.resources import observation_pb2

from ..utils import (
    convert_proto_date_time,
    ensure_non_null_date,
    parse_iso_datetime,
    search,
    search_proto,
)
from .codeable_concept import CodeableConcept, CodeableConceptDict, CodeableConceptProto
from .observation_component import (
    ObservationComponent,
    ObservationComponentDict,
    ObservationComponentProto,
)
from .observation_value import ObservationValue, ValueQuery
from .resource import Resource
from .resource_list import ResourceList


class Observation(Resource):
    @property
    @abstractmethod
    def effective_datetime(self) -> Optional[datetime]:
        pass  # pragma: no cover

    @property
    @abstractmethod
    def code(self) -> CodeableConcept:
        pass  # pragma: no cover

    @property
    @abstractmethod
    def value(self) -> ObservationValue:
        pass  # pragma: no cover

    @property
    @abstractmethod
    def component(self) -> List[ObservationComponent]:
        pass  # pragma: no cover

    @property
    def _sort_date(self) -> datetime:
        return ensure_non_null_date(self.effective_datetime)


class ObservationDict(Observation):
    def __init__(self, data: FHIR_Observation) -> None:
        self.data = data

    @property
    def effective_datetime(self) -> Optional[datetime]:
        return parse_iso_datetime(self.data.get("effectiveDateTime", ""))

    @property
    def code(self) -> CodeableConcept:
        return CodeableConceptDict(self.data.get("code", {}))

    @property
    def value(self) -> ObservationValue:
        return ObservationValue.build_from_dict(self.data)

    @property
    def component(self) -> List[ObservationComponent]:
        return list(
            map(lambda c: ObservationComponentDict(c), self.data.get("component", []))
        )

    def search_text(self, search_str: str) -> bool:
        return search(self.data, search_str)


class ObservationProto(Observation):
    def __init__(self, observation: observation_pb2.Observation) -> None:
        self.observation = observation

    @property
    def effective_datetime(self) -> Optional[datetime]:
        return convert_proto_date_time(self.observation.effective.date_time)

    @property
    def code(self) -> CodeableConcept:
        return CodeableConceptProto(self.observation.code)

    @property
    def value(self) -> ObservationValue:
        return ObservationValue.build_from_proto(self.observation)

    @property
    def component(self) -> List[ObservationComponent]:
        return list(
            map(lambda c: ObservationComponentProto(c), self.observation.component)
        )

    def search_text(self, search_str: str) -> bool:
        return search_proto(self.observation, search_str)


class Observations(ResourceList[Observation]):
    def find_by_coding(
        self, code: str = "", system: str = "", display: str = ""
    ) -> "Observations":
        return self.filter(lambda ob: ob.code.has_coding(code, system, display))

    def find_by_value(self, value_query: ValueQuery = {}) -> "Observations":
        return self.filter(lambda ob: ob.value.match(value_query))

    def find_by_component_value(
        self,
        code: str = "",
        system: str = "",
        display: str = "",
        value_query: ValueQuery = {},
    ) -> "Observations":
        def filter_func(ob: Observation) -> bool:
            for component in ob.component:
                if component.codeable_concept.has_coding(
                    code, system, display
                ) and component.value.match(value_query):
                    return True
            return False

        return self.filter(filter_func)

    def eq(self, value_float: float) -> "Observations":
        return self.find_by_value({"comparator": "=", "quantity_value": value_float})

    def gt(self, value_float: float) -> "Observations":
        return self.find_by_value({"comparator": ">", "quantity_value": value_float})

    def lt(self, value_float: float) -> "Observations":
        return self.find_by_value({"comparator": "<", "quantity_value": value_float})

    def gte(self, value_float: float) -> "Observations":
        return self.find_by_value({"comparator": ">=", "quantity_value": value_float})

    def lte(self, value_float: float) -> "Observations":
        return self.find_by_value({"comparator": "<=", "quantity_value": value_float})
