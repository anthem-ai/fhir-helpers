import json
from datetime import datetime

from google.fhir.r4.json_format import json_fhir_string_to_proto
from proto.google.fhir.proto.r4.core.resources.bundle_and_contained_resource_pb2 import (  # noqa: E501
    Bundle,
)

from fhir_helpers.resources.lpr import LPR

from .helpers import (
    get_example_bundle,
    get_example_bundle_by_filename,
    get_example_bundle_proto,
)


def test_condition_find() -> None:
    lpr_dict = LPR(get_example_bundle())
    lpr_proto = LPR(get_example_bundle_proto())

    assert len(lpr_dict.conditions) == 12
    assert len(lpr_proto.conditions) == 12

    conditions_dict = lpr_dict.conditions.find_by_coding("232353008")
    conditions_proto = lpr_proto.conditions.find_by_coding("232353008")
    assert len(conditions_dict) == 1
    assert len(conditions_proto) == 1

    three_years_ago = datetime(year=2018, month=3, day=6)

    conditions_dict = lpr_dict.conditions.find_after_date(three_years_ago)
    conditions_proto = lpr_proto.conditions.find_after_date(three_years_ago)
    assert len(conditions_dict) == 8
    assert len(conditions_proto) == 8

    conditions_dict = lpr_dict.conditions.find_before_date(three_years_ago)
    conditions_proto = lpr_proto.conditions.find_before_date(three_years_ago)
    assert len(conditions_dict) == 4
    assert len(conditions_proto) == 4


def test_condition_search() -> None:
    lpr_dict = LPR(get_example_bundle())
    lpr_proto = LPR(get_example_bundle_proto())

    assert len(lpr_dict.conditions.find_by_text_match("rhinitis")) == 1
    assert len(lpr_proto.conditions.find_by_text_match("rhinitis")) == 1


def test_procedure_sort() -> None:
    lpr_dict = LPR(get_example_bundle())
    lpr_proto = LPR(get_example_bundle_proto())

    sorted_dict = lpr_dict.conditions.sort_by_date()
    sorted_proto = lpr_proto.conditions.sort_by_date()
    sorted_dict_reverse = lpr_dict.conditions.sort_by_date(reverse=True)
    sorted_proto_reverse = lpr_proto.conditions.sort_by_date(reverse=True)

    dates = sorted([co.recorded_date for co in sorted_dict if co.recorded_date])
    dates_reverse = sorted(dates, reverse=True)

    for i in range(len(dates)):
        assert sorted_dict.get(i).recorded_date == dates[i]
        assert sorted_proto.get(i).recorded_date == dates[i]
        assert sorted_dict_reverse.get(i).recorded_date == dates_reverse[i]
        assert sorted_proto_reverse.get(i).recorded_date == dates_reverse[i]


def test_condtion_date() -> None:
    bundle_dict = get_example_bundle_by_filename("synthea_condition_date.json")
    lpr_dict = LPR(bundle_dict)
    lpr_proto = LPR(json_fhir_string_to_proto(json.dumps(bundle_dict), Bundle))

    condition_dict = lpr_dict.conditions.first()
    constion_proto = lpr_proto.conditions.first()
    assert condition_dict and condition_dict.onset_datetime
    assert constion_proto and constion_proto.onset_datetime
