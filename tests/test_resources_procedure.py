import json
from datetime import datetime

from fhir_types import FHIR_Procedure
from google.fhir.r4.json_format import json_fhir_string_to_proto
from proto.google.fhir.proto.r4.core.resources import procedure_pb2

from fhir_helpers.resources.lpr import LPR
from fhir_helpers.resources.procedure import ProcedureProto
from fhir_helpers.utils import parse_iso_datetime

from .helpers import get_example_bundle, get_example_bundle_proto


def test_procedures_find() -> None:
    lpr_dict = LPR(get_example_bundle())
    lpr_proto = LPR(get_example_bundle_proto())
    assert len(lpr_dict.procedures) == 41
    assert len(lpr_proto.procedures) == 41

    procedures_dict = lpr_dict.procedures.find_by_coding("180256009")
    procedures_proto = lpr_proto.procedures.find_by_coding("180256009")
    assert len(procedures_dict) == 30
    assert len(procedures_proto) == 30

    one_year_ago = datetime(year=2020, month=3, day=6)

    procedures_dict_temp = procedures_dict.find_after_date(one_year_ago)
    procedures_proto_temp = procedures_proto.find_after_date(one_year_ago)
    assert len(procedures_dict_temp) == 23
    assert len(procedures_proto_temp) == 23

    procedures_dict_temp = procedures_dict.find_before_date(one_year_ago)
    procedures_proto_temp = procedures_proto.find_before_date(one_year_ago)
    assert len(procedures_dict_temp) == 7
    assert len(procedures_proto_temp) == 7


def test_procedure_search() -> None:
    lpr_dict = LPR(get_example_bundle())
    lpr_proto = LPR(get_example_bundle_proto())

    assert len(lpr_dict.procedures.find_by_text_match("Subcutane")) == 30
    assert len(lpr_proto.procedures.find_by_text_match("Subcutane")) == 30


def test_procedure_performed_data() -> None:

    date_1 = "2012-11-17T20:35:35-07:00"
    date_2 = "2011-11-17T20:35:35-07:00"

    test_procedure: FHIR_Procedure = {
        "resourceType": "Procedure",
        "id": "1bb204b4-38f1-6fc7-eb17-fb64323d6e73",
        "status": "completed",
        "code": {
            "coding": [
                {
                    "system": "http://snomed.info/sct",
                    "code": "430193006",
                    "display": "Medication Reconciliation (procedure)",
                }
            ],
            "text": "Medication Reconciliation (procedure)",
        },
        "subject": {"reference": "urn:uuid:85e52038-4d69-50e9-9e46-e379b8d830af"},
        "encounter": {"reference": "urn:uuid:bcac71bf-6ff5-8eca-1422-e80aaea63cac"},
        "performedPeriod": {"start": date_1, "end": "2012-11-17T20:50:35-07:00"},
        "performedDateTime": date_2,
    }

    def get_procedure(data: FHIR_Procedure) -> ProcedureProto:
        return ProcedureProto(
            json_fhir_string_to_proto(json.dumps(data), procedure_pb2.Procedure)
        )

    assert get_procedure(test_procedure).performed_datetime == parse_iso_datetime(
        date_2
    )

    del test_procedure["performedDateTime"]
    assert get_procedure(test_procedure).performed_datetime == parse_iso_datetime(
        date_1
    )

    # Ensure proto dot notation procedure.performed.period.start
    # does not fail for non-existing entities
    del test_procedure["performedPeriod"]
    assert not get_procedure(test_procedure).performed_datetime


def test_procedure_sort() -> None:
    lpr_dict = LPR(get_example_bundle())
    lpr_proto = LPR(get_example_bundle_proto())

    sorted_dict = lpr_dict.procedures.sort_by_date()
    sorted_proto = lpr_proto.procedures.sort_by_date()
    sorted_dict_reverse = lpr_dict.procedures.sort_by_date(reverse=True)
    sorted_proto_reverse = lpr_proto.procedures.sort_by_date(reverse=True)

    dates = sorted([p.performed_datetime for p in sorted_dict if p.performed_datetime])
    dates_reverse = sorted(dates, reverse=True)

    for i in range(len(dates)):
        assert sorted_dict.get(i).performed_datetime == dates[i]
        assert sorted_proto.get(i).performed_datetime == dates[i]
        assert sorted_dict_reverse.get(i).performed_datetime == dates_reverse[i]
        assert sorted_proto_reverse.get(i).performed_datetime == dates_reverse[i]
