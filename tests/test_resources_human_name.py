import json

from fhir_types import FHIR_HumanName
from google.fhir.r4.json_format import json_fhir_string_to_proto
from proto.google.fhir.proto.r4.core import datatypes_pb2

from fhir_helpers.resources.human_name import HumanNameDict, HumanNameProto


def test_human_name() -> None:

    test_name: FHIR_HumanName = {
        "use": "official",
        "family": "Rempel203",
        "given": ["Tawny381"],
        "prefix": ["Mrs."],
        "suffix": ["PHD"],
    }

    name_dict = HumanNameDict(test_name)
    name_proto = HumanNameProto(
        json_fhir_string_to_proto(json.dumps(test_name), datatypes_pb2.HumanName)
    )

    for name in [name_dict, name_proto]:
        assert name.use == "official"
        assert name.family == "Rempel203"
        assert name.given == ["Tawny381"]
        assert name.prefix == ["Mrs."]
        assert name.suffix == ["PHD"]
        assert name.display_name == "Tawny381 Rempel203 (official)"


def test_text_name() -> None:

    test_name: FHIR_HumanName = {
        "use": "official",
        "text": "Mr John Smith",
        "family": "Rempel203",
        "given": ["Tawny381"],
    }

    name_dict = HumanNameDict(test_name)
    name_proto = HumanNameProto(
        json_fhir_string_to_proto(json.dumps(test_name), datatypes_pb2.HumanName)
    )

    assert name_dict.text == "Mr John Smith"
    assert name_proto.text == "Mr John Smith"

    assert name_dict.display_name == "Mr John Smith (official)"
    assert name_proto.display_name == "Mr John Smith (official)"
