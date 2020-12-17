import datetime
import json

from dateutil import tz
from freezegun import freeze_time
from google.fhir.r4.json_format import json_fhir_string_to_proto
from proto.google.fhir.proto.r4.core.resources.bundle_and_contained_resource_pb2 import (  # noqa: E501
    Bundle,
)

from fhir_helpers.resources.lpr import LPR

from .helpers import (
    get_example_bundle,
    get_example_bundle_by_filename,
    get_example_bundle_deceased_boolean,
    get_example_bundle_deceased_boolean_proto,
    get_example_bundle_not_dead,
    get_example_bundle_not_dead_proto,
    get_example_bundle_proto,
)


@freeze_time("2021-03-07")
def test_patient() -> None:
    lpr_dict = LPR(get_example_bundle())
    lpr_proto = LPR(get_example_bundle_proto())

    assert lpr_dict.patient.gender == "female"
    assert lpr_proto.patient.gender == "female"

    assert lpr_dict.patient.birthdate == datetime.date(
        year=2006,
        month=12,
        day=2,
    )
    assert lpr_proto.patient.birthdate == datetime.date(
        year=2006,
        month=12,
        day=2,
    )

    assert lpr_dict.patient.age == 14
    assert lpr_proto.patient.age == 14

    assert lpr_dict.patient.id == "85e52038-4d69-50e9-9e46-e379b8d830af"
    assert lpr_proto.patient.id == "85e52038-4d69-50e9-9e46-e379b8d830af"


def test_patient_deceased() -> None:
    # Dead patient.
    lpr_dict = LPR(get_example_bundle())
    lpr_proto = LPR(get_example_bundle_proto())

    assert lpr_dict.patient.deceased_boolean is True
    assert lpr_proto.patient.deceased_boolean is None

    assert lpr_dict.patient.deceased_datetime == datetime.datetime(
        year=2020,
        month=12,
        day=3,
        hour=20,
        minute=35,
        second=35,
        tzinfo=tz.tzoffset(None, -25200),
    )

    assert lpr_proto.patient.deceased_datetime == datetime.datetime(
        year=2020,
        month=12,
        day=3,
        hour=20,
        minute=35,
        second=35,
        tzinfo=tz.tzoffset(None, -25200),
    )

    assert lpr_dict.patient.is_deceased is True
    assert lpr_proto.patient.is_deceased is True

    # Not a dead patient.
    lpr_dict = LPR(get_example_bundle_not_dead())
    lpr_proto = LPR(get_example_bundle_not_dead_proto())

    assert lpr_dict.patient.deceased_boolean is None
    assert lpr_proto.patient.deceased_boolean is None

    assert lpr_dict.patient.deceased_datetime is None
    assert lpr_proto.patient.deceased_datetime is None

    assert lpr_dict.patient.is_deceased is False
    assert lpr_proto.patient.is_deceased is False

    # Deceased Boolean only patient.
    lpr_dict = LPR(get_example_bundle_deceased_boolean())
    lpr_proto = LPR(get_example_bundle_deceased_boolean_proto())

    assert lpr_dict.patient.deceased_boolean is True
    assert lpr_proto.patient.deceased_boolean is True

    assert lpr_dict.patient.deceased_datetime is None
    assert lpr_proto.patient.deceased_datetime is None

    assert lpr_dict.patient.is_deceased is True
    assert lpr_proto.patient.is_deceased is True


def test_name() -> None:
    lpr_dict = LPR(get_example_bundle())
    lpr_proto = LPR(get_example_bundle_proto())

    assert lpr_dict.patient.display_name == "Tawny381 Rempel203 (official)"
    assert lpr_proto.patient.display_name == "Tawny381 Rempel203 (official)"


def test_patient_missing_data() -> None:
    bundle_dict = get_example_bundle_by_filename("synthea_patient.json")

    del bundle_dict["entry"][0]["resource"]["birthDate"]
    del bundle_dict["entry"][0]["resource"]["name"]
    del bundle_dict["entry"][0]["resource"]["id"]

    lpr_dict = LPR(bundle_dict)
    lpr_proto = LPR(json_fhir_string_to_proto(json.dumps(bundle_dict), Bundle))

    assert not lpr_dict.patient.birthdate
    assert not lpr_proto.patient.birthdate

    assert not lpr_dict.patient.age
    assert not lpr_proto.patient.age

    assert len(lpr_dict.patient.name) == 0
    assert len(lpr_proto.patient.name) == 0

    assert not lpr_dict.patient.display_name
    assert not lpr_proto.patient.display_name

    assert lpr_dict.patient.id == ""
    assert lpr_proto.patient.id == ""
