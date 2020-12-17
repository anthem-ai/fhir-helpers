from datetime import datetime

from freezegun import freeze_time

from fhir_helpers.resources.lpr import LPR

from .helpers import get_example_bundle, get_example_bundle_proto


@freeze_time("2021-03-07")
def test_immunization_find() -> None:
    lpr_dict = LPR(get_example_bundle())
    lpr_proto = LPR(get_example_bundle_proto())

    assert len(lpr_dict.immunizations) == 18
    assert len(lpr_proto.immunizations) == 18

    immunizations_dict = lpr_dict.immunizations.find_by_coding("140")
    immunizations_proto = lpr_proto.immunizations.find_by_coding("140")
    assert len(immunizations_dict) == 9
    assert len(immunizations_proto) == 9

    three_years_ago = datetime(year=2018, month=3, day=6)
    immunizations_dict = lpr_dict.immunizations.find_after_date(three_years_ago)
    immunizations_proto = lpr_proto.immunizations.find_after_date(three_years_ago)
    assert len(immunizations_dict) == 4
    assert len(immunizations_proto) == 4


def test_immunization_search() -> None:
    lpr_dict = LPR(get_example_bundle())
    lpr_proto = LPR(get_example_bundle_proto())

    assert len(lpr_dict.immunizations.find_by_text_match("Influenza")) == 9
    assert len(lpr_proto.immunizations.find_by_text_match("Influenza")) == 9
