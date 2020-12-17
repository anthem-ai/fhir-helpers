from fhir_helpers.resources.lpr import LPR
from fhir_helpers.utils import ensure_non_null_date

from .helpers import get_example_bundle, get_example_bundle_proto


def test_practicioner_find() -> None:
    lpr_dict = LPR(get_example_bundle())
    lpr_proto = LPR(get_example_bundle_proto())

    assert len(lpr_dict.practitioners) == 2
    assert len(lpr_proto.practitioners) == 2

    assert not lpr_dict.practitioners.find_by_id("random_111")

    practitioner_dict = lpr_dict.practitioners.find_by_id(
        "bf3d8e3e-c8cc-3b52-ba5e-3640fdb31f7d"
    )

    practitioner_proto = lpr_proto.practitioners.find_by_id(
        "bf3d8e3e-c8cc-3b52-ba5e-3640fdb31f7d"
    )

    assert practitioner_dict
    assert practitioner_dict.name[0].display_name == "Tyrell880 Hyatt152"
    assert practitioner_dict.gender == "male"
    assert practitioner_dict._sort_date == ensure_non_null_date(None)

    assert practitioner_proto
    assert "Tyrell880 Hyatt152" in practitioner_proto.name[0].display_name
    assert practitioner_proto.gender == "male"
    assert practitioner_proto._sort_date == ensure_non_null_date(None)


def test_practitioner_search() -> None:
    lpr_dict = LPR(get_example_bundle())
    lpr_proto = LPR(get_example_bundle_proto())

    assert len(lpr_dict.practitioners.find_by_text_match("Bernard308")) == 1
    assert len(lpr_proto.practitioners.find_by_text_match("Bernard308")) == 1
