from datetime import datetime

from dateutil.parser import parse

from fhir_helpers.resources.lpr import LPR

from .helpers import get_example_bundle_medication_dispense as get_example_bundle
from .helpers import (
    get_example_bundle_medication_dispense_proto as get_example_bundle_proto,
)


def test_medication_dispense_find() -> None:
    lpr_dict = LPR(get_example_bundle())
    lpr_proto = LPR(get_example_bundle_proto())
    assert len(lpr_dict.medication_dispenses) == 1
    assert len(lpr_proto.medication_dispenses) == 1

    assert len(lpr_dict.medication_dispenses.find_by_coding("1014676")) == 1
    assert len(lpr_proto.medication_dispenses.find_by_coding("1014676")) == 1

    two_thousand_nine = datetime(year=2009, month=1, day=1)

    medication_dispenses_dict = lpr_dict.medication_dispenses.find_after_date(
        two_thousand_nine
    )
    medication_dispenses_proto = lpr_proto.medication_dispenses.find_after_date(
        two_thousand_nine
    )
    assert len(medication_dispenses_dict) == 1
    assert len(medication_dispenses_proto) == 1

    medication_dispenses_dict = lpr_dict.medication_dispenses.find_before_date(
        two_thousand_nine
    )
    medication_dispenses_proto = lpr_proto.medication_dispenses.find_before_date(
        two_thousand_nine
    )
    assert len(medication_dispenses_dict) == 0
    assert len(medication_dispenses_proto) == 0


def test_medication_dispense_search() -> None:
    lpr_dict = LPR(get_example_bundle())
    lpr_proto = LPR(get_example_bundle_proto())

    assert len(lpr_dict.medication_dispenses.find_by_text_match("cetirizine")) == 1
    assert len(lpr_proto.medication_dispenses.find_by_text_match("cetirizine")) == 1


def test_procedure_sort() -> None:
    lpr_dict = LPR(get_example_bundle())
    lpr_proto = LPR(get_example_bundle_proto())

    sorted_dict = lpr_dict.medication_dispenses.sort_by_date()
    sorted_proto = lpr_proto.medication_dispenses.sort_by_date()
    sorted_dict_reverse = lpr_dict.medication_dispenses.sort_by_date(reverse=True)
    sorted_proto_reverse = lpr_proto.medication_dispenses.sort_by_date(reverse=True)

    dates = sorted([mr.when_handed_over for mr in sorted_dict if mr.when_handed_over])
    dates_reverse = sorted(dates, reverse=True)

    for i in range(len(dates)):
        assert sorted_dict.get(i).when_handed_over == dates[i]
        assert sorted_proto.get(i).when_handed_over == dates[i]
        assert sorted_dict_reverse.get(i).when_handed_over == dates_reverse[i]
        assert sorted_proto_reverse.get(i).when_handed_over == dates_reverse[i]


def test_date() -> None:
    lpr_dict = LPR(get_example_bundle())
    lpr_proto = LPR(get_example_bundle_proto())

    # This matches synthea. Just an extra sanity test
    dt = "2009-12-22T20:35:35-07:00"

    assert lpr_dict.medication_dispenses.get(0).when_handed_over == parse(dt)
    assert lpr_proto.medication_dispenses.get(0).when_handed_over == parse(dt)


def test_status() -> None:
    lpr_dict = LPR(get_example_bundle())
    lpr_proto = LPR(get_example_bundle_proto())

    assert lpr_dict.medication_dispenses.get(0).status == "completed"
    assert lpr_proto.medication_dispenses.get(0).status == "completed"
