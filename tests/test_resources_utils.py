import json
from datetime import date, datetime

from dateutil import tz
from freezegun import freeze_time
from google.fhir.r4.json_format import json_fhir_string_to_proto
from proto.google.fhir.proto.r4.core.resources import observation_pb2

from fhir_helpers.utils import (
    calc_time_ago,
    ensure_non_null_date,
    get_years_since_date,
    get_years_since_datetime,
    parse_iso_datetime,
    search_proto,
    tz_conv,
)


def test_tz_conv() -> None:
    assert tz_conv("Z") == 0
    assert tz_conv("00:00") == 0
    assert tz_conv("-06:00") == -21600
    assert tz_conv("06:00") == 21600
    assert tz_conv("-06:30") == -23400
    assert tz_conv("06:30") == 23400
    assert tz_conv("-11:00") == -39600
    assert tz_conv("11:00") == 39600


def test_parse_iso_datetime() -> None:
    assert isinstance(parse_iso_datetime("2012-11-17T20:35:35-07:00"), datetime)
    assert isinstance(parse_iso_datetime("2018-09-27T23:37:44Z"), datetime)


def test_get_years_since_date() -> None:
    with freeze_time("2021-03-07"):
        assert get_years_since_date(date(2019, 2, 2)) == 2
        assert get_years_since_date(date(2019, 2, 2)) == 2


def test_get_years_since_datetime() -> None:
    with freeze_time("2021-03-07"):
        assert get_years_since_datetime(datetime(2019, 2, 2, tzinfo=tz.tzutc())) == 2
        assert get_years_since_datetime(datetime(2019, 2, 2, tzinfo=tz.tzutc())) == 2


def test_calc_time_ago() -> None:
    with freeze_time("2021-03-07"):
        assert calc_time_ago(1) == datetime(2020, 3, 7, tzinfo=tz.tzutc())
        assert calc_time_ago(1, 1) == datetime(2020, 2, 7, tzinfo=tz.tzutc())
        assert calc_time_ago(1, 1, 1) == datetime(2020, 2, 6, tzinfo=tz.tzutc())


def test_ensure_non_null_date() -> None:
    dt = datetime(2020, 3, 7, tzinfo=tz.tzutc())
    assert ensure_non_null_date(dt) == dt
    assert ensure_non_null_date(None) == datetime(1900, 1, 1, tzinfo=tz.tzutc())


def test_search_proto() -> None:
    observation_test = {
        "resourceType": "Observation",
        "id": "c28fdbc3-339a-2774-05d3-2de62eb805b3",
        "status": "final",
        "code": {
            "coding": [
                {
                    "system": "http://loinc.org",
                    "code": "8302-2",
                    "display": "Body Height",
                }
            ],
            "text": "Body Height",
        },
        "subject": {"reference": "urn:uuid:85e52038-4d69-50e9-9e46-e379b8d830af"},
        "effectiveDateTime": "2011-11-12T20:35:35-07:00",
        "valueQuantity": {
            "value": 104.8,
            "unit": "cm",
            "system": "http://unitsofmeasure.org",
            "code": "cm",
        },
    }
    observation_proto = json_fhir_string_to_proto(
        json.dumps(observation_test), observation_pb2.Observation
    )
    assert search_proto(observation_proto, "8302")
    assert not search_proto(observation_proto, "1234WWW")
