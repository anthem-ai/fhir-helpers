from datetime import datetime

from dateutil.parser import parse

from fhir_helpers.resources.lpr import LPR

from .helpers import get_example_bundle, get_example_bundle_proto


def test_medication_request_find() -> None:
    lpr_dict = LPR(get_example_bundle())
    lpr_proto = LPR(get_example_bundle_proto())
    assert len(lpr_dict.medication_requests) == 6
    assert len(lpr_proto.medication_requests) == 6

    assert len(lpr_dict.medication_requests.find_by_coding("834061")) == 2
    assert len(lpr_proto.medication_requests.find_by_coding("834061")) == 2

    six_years_ago = datetime(year=2015, month=3, day=6)

    medication_requests_dict = lpr_dict.medication_requests.find_after_date(
        six_years_ago
    )
    medication_requests_proto = lpr_proto.medication_requests.find_after_date(
        six_years_ago
    )
    assert len(medication_requests_dict) == 3
    assert len(medication_requests_proto) == 3

    medication_requests_dict = lpr_dict.medication_requests.find_before_date(
        six_years_ago
    )
    medication_requests_proto = lpr_proto.medication_requests.find_before_date(
        six_years_ago
    )
    assert len(medication_requests_dict) == 3
    assert len(medication_requests_proto) == 3


def test_medication_request_search() -> None:
    lpr_dict = LPR(get_example_bundle())
    lpr_proto = LPR(get_example_bundle_proto())

    assert len(lpr_dict.medication_requests.find_by_text_match("Penicillin")) == 2
    assert len(lpr_proto.medication_requests.find_by_text_match("Penicillin")) == 2


def test_procedure_sort() -> None:
    lpr_dict = LPR(get_example_bundle())
    lpr_proto = LPR(get_example_bundle_proto())

    sorted_dict = lpr_dict.medication_requests.sort_by_date()
    sorted_proto = lpr_proto.medication_requests.sort_by_date()
    sorted_dict_reverse = lpr_dict.medication_requests.sort_by_date(reverse=True)
    sorted_proto_reverse = lpr_proto.medication_requests.sort_by_date(reverse=True)

    dates = sorted([mr.authored_on for mr in sorted_dict if mr.authored_on])
    dates_reverse = sorted(dates, reverse=True)

    for i in range(len(dates)):
        assert sorted_dict.get(i).authored_on == dates[i]
        assert sorted_proto.get(i).authored_on == dates[i]
        assert sorted_dict_reverse.get(i).authored_on == dates_reverse[i]
        assert sorted_proto_reverse.get(i).authored_on == dates_reverse[i]


def test_date() -> None:
    lpr_dict = LPR(get_example_bundle())
    lpr_proto = LPR(get_example_bundle_proto())

    # This matches synthea. Just an extra sanity test
    dt = "2009-12-22T20:35:35-07:00"

    assert lpr_dict.medication_requests.get(0).authored_on == parse(dt)
    assert lpr_proto.medication_requests.get(0).authored_on == parse(dt)


def test_status() -> None:
    lpr_dict = LPR(get_example_bundle())
    lpr_proto = LPR(get_example_bundle_proto())

    assert lpr_dict.medication_requests.get(0).status == "active"
    assert lpr_proto.medication_requests.get(0).status == "active"

    assert lpr_dict.medication_requests.get(2).status == "stopped"
    assert lpr_proto.medication_requests.get(2).status == "stopped"


def test_requester() -> None:
    lpr_dict = LPR(get_example_bundle())
    lpr_proto = LPR(get_example_bundle_proto())

    lpr_requestor_dict = lpr_dict.medication_requests.get(0).requester_practitioner
    lpr_requestor_proto = lpr_proto.medication_requests.get(0).requester_practitioner

    assert lpr_requestor_dict
    assert lpr_requestor_dict == lpr_dict.practitioners.find_by_id(
        lpr_requestor_dict.id
    )

    assert lpr_requestor_proto
    assert lpr_requestor_proto == lpr_proto.practitioners.find_by_id(
        lpr_requestor_proto.id
    )

    requests = lpr_dict.medication_requests.filter(
        lambda mr: mr.requester_practitioner is not None
        and mr.requester_practitioner.id == "ed3630e0-cdaa-3d90-b52b-2b1a15247493"
    )
    assert len(requests) == 6
