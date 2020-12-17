from typing import Optional, TypedDict, Union

from fhir_types import FHIR_Observation, FHIR_Observation_Component
from proto.google.fhir.proto.r4.core.resources import observation_pb2

from ..utils import ComparatorType
from .codeable_concept import CodeableConcept, CodeableConceptDict, CodeableConceptProto
from .quantity import Quantity, QuantityDict, QuantityProto

ValueType = Union[Quantity, CodeableConcept, float, str, bool, None]


# A TypedDict that provides the properties needed to query values in various ways
class ValueQuery(TypedDict, total=False):
    # quantity type
    quantity_value: float
    quantity_unit: str
    quantity_system: str
    quantity_code: str
    # codeable_concept type
    codeable_concept_code: str
    codeable_concept_system: str
    codeable_concept_display: str
    # primitive types
    string_value: str
    integer_value: float
    # operator for numeric types only
    comparator: ComparatorType


# Only one value can be used at a time
# https://www.hl7.org/fhir/observation-definitions.html#Observation.value_x_

# Not implemented
# valueRange, valueRatio, valueTime, valueSampledData, valueBoolean, valuePeriod
class ObservationValue:
    def __init__(
        self,
        value_quantity: Quantity,
        value_codeable_concept: CodeableConcept,
        value_int: Optional[float] = None,
        value_string: Optional[str] = None,
        value_boolean: Optional[bool] = None,
    ) -> None:
        self.value_quantity = value_quantity
        self.value_codeable_concept = value_codeable_concept
        self.value_int = value_int
        self.value_string = value_string
        self.value_boolean = value_boolean

    # def get_value(self) -> ValueType:
    #     if self.value_quantity:
    #         return self.value_quantity
    #     if self.value_codeable_concept:
    #         return self.value_codeable_concept
    #     if self.value_int:
    #         return self.value_int
    #     if self.value_string:
    #         return self.value_string
    #     if self.value_boolean:
    #         return self.value_boolean
    #     return None

    def match(self, value_query: ValueQuery = {}) -> bool:
        if not self.value_quantity.empty():
            return self.value_quantity.match(
                comparator=value_query.get("comparator", "="),
                value_num=value_query["quantity_value"],  # Required
                unit_str=value_query.get("quantity_unit", ""),
                system_str=value_query.get("quantity_system", ""),
                code_str=value_query.get("quantity_code", ""),
            )
        if not self.value_codeable_concept.empty():
            return self.value_codeable_concept.has_coding(
                code_str=value_query.get("codeable_concept_code", ""),
                system_str=value_query.get("codeable_concept_system", ""),
                display_str=value_query.get("codeable_concept_display", ""),
            )
        return False

    @classmethod
    def build_from_dict(
        cls, observation: Union[FHIR_Observation, FHIR_Observation_Component]
    ) -> "ObservationValue":
        return ObservationValue(
            value_quantity=QuantityDict(observation.get("valueQuantity", {})),
            value_codeable_concept=CodeableConceptDict(
                observation.get("valueCodeableConcept", {})
            ),
            value_int=observation.get("valueInteger", None),
            value_string=observation.get("valueString", None),
        )

    @classmethod
    def build_from_proto(
        cls,
        observation: Union[
            observation_pb2.Observation, observation_pb2.Observation.Component
        ],
    ) -> "ObservationValue":

        return ObservationValue(
            value_quantity=QuantityProto(observation.value.quantity),
            value_codeable_concept=CodeableConceptProto(
                observation.value.codeable_concept
            ),
            value_int=observation.value.integer.value,
            value_string=observation.value.string_value.value,
        )
