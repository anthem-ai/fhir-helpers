from fhir_helpers.resources.lpr import LPR

from .helpers import get_example_bundle, get_example_bundle_proto


def test_lpr_init() -> None:
    lpr_dict = LPR(get_example_bundle())
    lpr_proto = LPR(get_example_bundle_proto())

    assert lpr_dict.patient
    assert len(lpr_dict.observations) == 137
    assert len(lpr_dict.medication_requests) == 6
    assert len(lpr_dict.procedures) == 41
    assert len(lpr_dict.conditions) == 12

    assert lpr_proto.patient
    assert len(lpr_proto.observations) == 137
    assert len(lpr_proto.medication_requests) == 6
    assert len(lpr_proto.procedures) == 41
    assert len(lpr_proto.conditions) == 12
