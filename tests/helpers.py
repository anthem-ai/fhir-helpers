import json
from functools import lru_cache
from pathlib import Path
from typing import cast

from fhir_types import FHIR_Bundle, FHIR_Bundle_Entry, FHIR_MedicationDispense
from google.fhir.r4.json_format import json_fhir_string_to_proto
from proto.google.fhir.proto.r4.core.resources.bundle_and_contained_resource_pb2 import (  # noqa: E501
    Bundle,
)


def get_example_bundle_by_filename(filename: str) -> FHIR_Bundle:
    syn_path = Path("./tests/data", filename)
    bundle = cast(FHIR_Bundle, json.loads(syn_path.read_text()))
    return bundle


@lru_cache
def get_example_bundle() -> FHIR_Bundle:
    # This patient is dead.
    return get_example_bundle_by_filename("synthea_1.json")


@lru_cache
def get_example_bundle_proto() -> Bundle:
    bundle_dict = get_example_bundle()
    return json_fhir_string_to_proto(json.dumps(bundle_dict), Bundle)


@lru_cache
def get_example_values_bundle() -> FHIR_Bundle:
    return get_example_bundle_by_filename("synthea_observation_values.json")


@lru_cache
def get_example_values_bundle_proto() -> Bundle:
    bundle_dict = get_example_values_bundle()
    return json_fhir_string_to_proto(json.dumps(bundle_dict), Bundle)


@lru_cache
def get_example_allergy_intolerance_bundle() -> FHIR_Bundle:
    # This patient is not dead.
    return get_example_bundle_by_filename(
        "synthea_patient_with_allergy_intolerances.json"
    )


@lru_cache
def get_example_allergy_intolerance_bundle_proto() -> Bundle:
    bundle_dict = get_example_allergy_intolerance_bundle()
    return json_fhir_string_to_proto(json.dumps(bundle_dict), Bundle)


@lru_cache
def get_example_bundle_not_dead() -> FHIR_Bundle:
    return get_example_allergy_intolerance_bundle()


@lru_cache
def get_example_bundle_not_dead_proto() -> Bundle:
    return get_example_allergy_intolerance_bundle_proto()


@lru_cache
def get_example_bundle_deceased_boolean() -> FHIR_Bundle:
    bundle = get_example_bundle()
    del bundle["entry"][0]["resource"]["deceasedDateTime"]
    return bundle


@lru_cache
def get_example_bundle_deceased_boolean_proto() -> Bundle:
    bundle_dict = get_example_bundle_deceased_boolean()
    return json_fhir_string_to_proto(json.dumps(bundle_dict), Bundle)


@lru_cache
def get_example_bundle_medication_dispense() -> FHIR_Bundle:
    bundle = get_example_bundle()
    medication_dispense: FHIR_MedicationDispense = {
        "resourceType": "MedicationDispense",
        "id": "36e7d845-ad82-6d4a-9e95-e4cc6de6f827",
        "status": "completed",
        "medicationCodeableConcept": {
            "coding": [
                {
                    "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
                    "code": "1014676",
                    "display": "cetirizine hydrochloride 5 MG Oral Tablet",
                }
            ],
            "text": "cetirizine hydrochloride 5 MG Oral Tablet",
        },
        "subject": {"reference": "urn:uuid:85e52038-4d69-50e9-9e46-e379b8d830af"},
        "whenHandedOver": "2009-12-22T20:35:35-07:00",
        "dosageInstruction": [
            {"sequence": 1, "text": "Take as needed.", "asNeededBoolean": True}
        ],
    }

    bundle_entry: FHIR_Bundle_Entry = {
        "fullUrl": "urn:uuid:36e7d845-ad82-6d4a-9e95-e4cc6de6f827",
        "resource": medication_dispense,
    }

    bundle["entry"].append(bundle_entry)
    return bundle


@lru_cache
def get_example_bundle_medication_dispense_proto() -> Bundle:
    bundle_dict = get_example_bundle_medication_dispense()
    return json_fhir_string_to_proto(json.dumps(bundle_dict), Bundle)
