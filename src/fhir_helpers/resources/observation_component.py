from abc import ABC, abstractmethod

from fhir_types import FHIR_Observation_Component
from proto.google.fhir.proto.r4.core.resources import observation_pb2

from .codeable_concept import CodeableConcept, CodeableConceptDict, CodeableConceptProto
from .observation_value import ObservationValue


class ObservationComponent(ABC):
    @property
    @abstractmethod
    def codeable_concept(self) -> CodeableConcept:
        pass  # pragma: no cover

    @property
    @abstractmethod
    def value(self) -> ObservationValue:
        pass  # pragma: no cover


class ObservationComponentDict(ObservationComponent):
    def __init__(self, data: FHIR_Observation_Component) -> None:
        self.data = data

    @property
    def codeable_concept(self) -> CodeableConcept:
        return CodeableConceptDict(self.data.get("code", {}))

    @property
    def value(self) -> ObservationValue:
        return ObservationValue.build_from_dict(self.data)


class ObservationComponentProto(ObservationComponent):
    def __init__(self, data: observation_pb2.Observation.Component) -> None:
        self.data = data

    @property
    def codeable_concept(self) -> CodeableConcept:
        return CodeableConceptProto(self.data.code)

    @property
    def value(self) -> ObservationValue:
        return ObservationValue.build_from_proto(self.data)
