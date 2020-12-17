import json

from fhir_types import FHIR_Quantity

# from .helpers import get_example_values_bundle, get_example_values_bundle_proto
from google.fhir.r4.json_format import json_fhir_string_to_proto
from proto.google.fhir.proto.r4.core import datatypes_pb2

from fhir_helpers.resources.quantity import QuantityDict, QuantityProto


def test_quantity_match() -> None:
    quantity: FHIR_Quantity = {
        "value": 25.5,
        "unit": "kg/m2",
        "system": "http://unitsofmeasure.org",
        "code": "kg/m2",
    }

    quantity_dict = QuantityDict(quantity)
    quantity_proto = QuantityProto(
        json_fhir_string_to_proto(json.dumps(quantity), datatypes_pb2.Quantity)
    )

    assert quantity_dict.match(comparator=">", value_num=20)
    assert not quantity_dict.match(comparator="<", value_num=20)
    assert quantity_proto.match(comparator=">", value_num=20)
    assert not quantity_proto.match(comparator="<", value_num=20)

    assert quantity_dict.match(comparator=">", value_num=20, unit_str="kg/m2")
    assert not quantity_dict.match(comparator=">", value_num=20, unit_str="m2")
    assert quantity_proto.match(comparator=">", value_num=20, unit_str="kg/m2")
    assert not quantity_proto.match(comparator=">", value_num=20, unit_str="m2")

    assert quantity_dict.match(comparator=">", value_num=20, code_str="kg/m2")
    assert not quantity_dict.match(comparator=">", value_num=20, code_str="m2")
    assert quantity_proto.match(comparator=">", value_num=20, code_str="kg/m2")
    assert not quantity_proto.match(comparator=">", value_num=20, code_str="m2")

    assert quantity_dict.match(
        comparator=">", value_num=20, system_str="http://unitsofmeasure.org"
    )
    assert not (
        quantity_dict.match(comparator=">", value_num=20, system_str="http://.org")
    )
    assert quantity_proto.match(
        comparator=">", value_num=20, system_str="http://unitsofmeasure.org"
    )
    assert not (
        quantity_proto.match(comparator=">", value_num=20, system_str="http://.org")
    )


def test_empty_quantity_match() -> None:
    quantity_dict = QuantityDict({})
    assert not quantity_dict.match(comparator=">", value_num=20)
