import json

from fhir_types import FHIR_CodeableConcept
from google.fhir.r4.json_format import json_fhir_string_to_proto
from proto.google.fhir.proto.r4.core import datatypes_pb2

from fhir_helpers.resources.codeable_concept import (
    CodeableConceptDict,
    CodeableConceptProto,
)


def test_get_codings() -> None:

    test_concept: FHIR_CodeableConcept = {
        "coding": [
            {
                "system": "loinc.org",
                "code": "14",
                "display": "Body1",
            },
            {
                "system": "oinc.org",
                "code": "45",
                "display": "Height",
            },
            {"system": "loinc.org", "code": "456", "display": "Body"},
        ],
        "text": "Body Height",
    }

    concept_dict = CodeableConceptDict(test_concept)
    concept_proto = CodeableConceptProto(
        json_fhir_string_to_proto(
            json.dumps(test_concept), datatypes_pb2.CodeableConcept
        )
    )

    assert concept_dict.has_coding("14")
    assert concept_proto.has_coding("14")
    assert not concept_dict.has_coding("X")
    assert not concept_proto.has_coding("X")

    assert concept_dict.has_coding("14", system_str="loinc.org")
    assert concept_proto.has_coding("14", system_str="loinc.org")
    assert not concept_dict.has_coding("14", system_str="C.org")
    assert not concept_proto.has_coding("14", system_str="C.org")

    assert concept_dict.has_coding("14", display_str="Body1")
    assert concept_proto.has_coding("14", display_str="Body1")
    assert not concept_dict.has_coding("1X", display_str="Body1")
    assert not concept_proto.has_coding("1X", display_str="Body1")

    assert not concept_dict.has_coding("14", display_str="Height")
    assert not concept_proto.has_coding("14", display_str="Height")
