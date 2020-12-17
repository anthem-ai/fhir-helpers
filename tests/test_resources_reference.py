import json

from fhir_types import FHIR_Reference
from google.fhir.r4.json_format import json_fhir_string_to_proto
from proto.google.fhir.proto.r4.core import datatypes_pb2

from fhir_helpers.resources.reference import ReferenceDict, ReferenceProto


def test_reference() -> None:
    ref_data: FHIR_Reference = {
        "reference": "urn:uuid:ed3630e0-cdaa-3d90-b52b-2b1a15247493",
        "display": "Dr. Bernard308 Carter549",
    }

    reference_dict = ReferenceDict(ref_data)
    reference_dict_proto = ReferenceProto(
        json_fhir_string_to_proto(json.dumps(ref_data), datatypes_pb2.Reference)
    )

    assert reference_dict.reference == "urn:uuid:ed3630e0-cdaa-3d90-b52b-2b1a15247493"
    assert (
        reference_dict_proto.reference
        == "urn:uuid:ed3630e0-cdaa-3d90-b52b-2b1a15247493"
    )

    assert reference_dict.display == "Dr. Bernard308 Carter549"
    assert reference_dict_proto.display == "Dr. Bernard308 Carter549"
