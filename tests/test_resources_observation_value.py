from fhir_types import FHIR_Observation

from fhir_helpers.resources.observation_value import ObservationValue


def test_observation_quantity_value_match() -> None:
    observation: FHIR_Observation = {
        "resourceType": "Observation",
        "id": "6e80a07a-16d2-4663-ba58-e0bfc6b0f174",
        "status": "final",
        "code": {
            "coding": [
                {
                    "system": "http://loinc.org",
                    "code": "39156-5",
                    "display": "Body Mass Index",
                }
            ],
            "text": "Body Mass Index",
        },
        "subject": {"reference": "urn:uuid:822f82f3-3d03-4ce1-8c2b-14764c244fcf"},
        "encounter": {"reference": "urn:uuid:b88dd693-d876-4853-9904-2847caa9886d"},
        "effectiveDateTime": "2010-03-29T15:17:19-04:00",
        "issued": "2010-03-29T15:17:19.272-04:00",
        "valueQuantity": {
            "value": 25.5,
            "unit": "kg/m2",
            "system": "http://unitsofmeasure.org",
            "code": "kg/m2",
        },
    }

    ob_value = ObservationValue.build_from_dict(observation)

    assert ob_value.match({"comparator": ">", "quantity_value": 20})
    assert not ob_value.match({"comparator": "<", "quantity_value": 20})
    assert ob_value.match({"comparator": ">=", "quantity_value": 25.5})
    assert ob_value.match(
        {"comparator": ">", "quantity_value": 20, "quantity_unit": "kg/m2"}
    )
    assert not (
        ob_value.match({"comparator": ">", "quantity_value": 20, "quantity_unit": "m2"})
    )


def test_observation_codeable_quanity_value_match() -> None:
    observation: FHIR_Observation = {
        "resourceType": "Observation",
        "id": "c25e0768-60a4-4cf4-b85a-a0581e8bb894",
        "status": "final",
        "code": {
            "coding": [
                {
                    "system": "http://loinc.org",
                    "code": "72166-2",
                    "display": "Tobacco smoking status NHIS",
                }
            ],
            "text": "Tobacco smoking status NHIS",
        },
        "subject": {"reference": "urn:uuid:822f82f3-3d03-4ce1-8c2b-14764c244fcf"},
        "encounter": {"reference": "urn:uuid:59319a2c-89bf-4b21-9329-b3cfcb42cc04"},
        "effectiveDateTime": "2013-04-15T15:17:19-04:00",
        "issued": "2013-04-15T15:17:19.272-04:00",
        "valueCodeableConcept": {
            "coding": [
                {
                    "system": "http://snomed.info/sct",
                    "code": "266919005",
                    "display": "Never smoker",
                }
            ],
            "text": "Never smoker",
        },
    }

    ob_value = ObservationValue.build_from_dict(observation)
    assert ob_value.match({"codeable_concept_code": "266919005"})
    assert ob_value.match(
        {
            "codeable_concept_code": "266919005",
            "codeable_concept_system": "http://snomed.info/sct",
        }
    )
    assert not (
        ob_value.match(
            {
                "codeable_concept_code": "266919005",
                "codeable_concept_system": "o/sct",
            }
        )
    )


def test_empty_value() -> None:
    observation: FHIR_Observation = {
        "resourceType": "Observation",
        "id": "6e80a07a-16d2-4663-ba58-e0bfc6b0f174",
        "status": "final",
        "code": {
            "coding": [
                {
                    "system": "http://loinc.org",
                    "code": "39156-5",
                    "display": "Body Mass Index",
                }
            ],
            "text": "Body Mass Index",
        },
        "subject": {"reference": "urn:uuid:822f82f3-3d03-4ce1-8c2b-14764c244fcf"},
        "encounter": {"reference": "urn:uuid:b88dd693-d876-4853-9904-2847caa9886d"},
        "effectiveDateTime": "2010-03-29T15:17:19-04:00",
        "issued": "2010-03-29T15:17:19.272-04:00",
    }

    ob_value = ObservationValue.build_from_dict(observation)

    assert not ob_value.match({})
