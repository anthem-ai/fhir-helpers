from datetime import datetime

from freezegun import freeze_time

from fhir_helpers.resources.lpr import LPR

from .helpers import get_example_allergy_intolerance_bundle as get_example_bundle
from .helpers import (
    get_example_allergy_intolerance_bundle_proto as get_example_bundle_proto,
)


@freeze_time("2021-03-07")
def test_allergy_intolerance_find() -> None:
    lpr_dict = LPR(get_example_bundle())
    lpr_proto = LPR(get_example_bundle_proto())

    assert len(lpr_dict.allergy_intolerances) == 7
    assert len(lpr_proto.allergy_intolerances) == 7

    allergy_intolerances_dict = lpr_dict.allergy_intolerances.find_by_coding(
        "714035009"
    )
    allergy_intolerances_proto = lpr_proto.allergy_intolerances.find_by_coding(
        "714035009"
    )
    assert len(allergy_intolerances_dict) == 1
    assert len(allergy_intolerances_proto) == 1

    back_in_2010 = datetime(year=2010, month=3, day=6)
    allergy_intolerances_dict = lpr_dict.allergy_intolerances.find_after_date(
        back_in_2010
    )
    allergy_intolerances_proto = lpr_proto.allergy_intolerances.find_after_date(
        back_in_2010
    )
    assert len(allergy_intolerances_dict) == 0
    assert len(allergy_intolerances_proto) == 0

    # None of the AllergyIntolerances in this LPR had onsetDateTime, so it was manually
    # added to one of them.
    back_in_2000 = datetime(year=2000, month=3, day=6)
    allergy_intolerances_dict = lpr_dict.allergy_intolerances.find_after_date(
        back_in_2000
    )
    allergy_intolerances_proto = lpr_proto.allergy_intolerances.find_after_date(
        back_in_2000
    )
    assert len(allergy_intolerances_dict) == 1
    assert len(allergy_intolerances_proto) == 1


def test_allergy_intolerance_search() -> None:
    lpr_dict = LPR(get_example_bundle())
    lpr_proto = LPR(get_example_bundle_proto())

    assert len(lpr_dict.allergy_intolerances.find_by_text_match("soya")) == 1
    assert len(lpr_proto.allergy_intolerances.find_by_text_match("soya")) == 1
