from datetime import datetime

from freezegun import freeze_time

from fhir_helpers.resources.lpr import LPR

from .helpers import get_example_bundle, get_example_bundle_proto


@freeze_time("2021-03-07")
def test_encounter_find() -> None:
    lpr_dict = LPR(get_example_bundle())
    lpr_proto = LPR(get_example_bundle_proto())

    assert len(lpr_dict.encounters) == 34
    assert len(lpr_proto.encounters) == 34

    encounters_dict = lpr_dict.encounters.find_by_coding("50849002")
    encounters_proto = lpr_proto.encounters.find_by_coding("50849002")
    assert len(encounters_dict) == 2
    assert len(encounters_proto) == 2

    three_years_ago = datetime(year=2018, month=3, day=6)
    encounters_dict = lpr_dict.encounters.find_after_date(three_years_ago)
    encounters_proto = lpr_proto.encounters.find_after_date(three_years_ago)
    assert len(encounters_dict) == 21
    assert len(encounters_proto) == 21


def test_encounter_search() -> None:
    lpr_dict = LPR(get_example_bundle())
    lpr_proto = LPR(get_example_bundle_proto())

    assert (
        len(lpr_dict.encounters.find_by_text_match("COOLEY DICKINSON HOSPITAL INC,THE"))
        == 25
    )
    assert (
        len(
            lpr_proto.encounters.find_by_text_match("COOLEY DICKINSON HOSPITAL INC,THE")
        )
        == 25
    )
