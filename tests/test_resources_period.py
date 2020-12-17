import json
from datetime import datetime

from dateutil import tz
from fhir_types import FHIR_Period
from google.fhir.r4.json_format import json_fhir_string_to_proto
from proto.google.fhir.proto.r4.core import datatypes_pb2

from fhir_helpers.resources.period import PeriodDict, PeriodProto


def test_period_end() -> None:

    test_concept: FHIR_Period = {
        "start": "2014-08-20T21:35:35-06:00",
        "end": "2014-08-20T21:50:35-06:00",
    }

    period_dict = PeriodDict(test_concept)
    period_proto = PeriodProto(
        json_fhir_string_to_proto(json.dumps(test_concept), datatypes_pb2.Period)
    )

    assert period_dict.start == datetime(
        year=2014,
        month=8,
        day=20,
        hour=21,
        minute=35,
        second=35,
        tzinfo=tz.tzoffset(None, -21600),
    )
    assert period_dict.end == datetime(
        year=2014,
        month=8,
        day=20,
        hour=21,
        minute=50,
        second=35,
        tzinfo=tz.tzoffset(None, -21600),
    )

    assert period_proto.start == datetime(
        year=2014,
        month=8,
        day=20,
        hour=21,
        minute=35,
        second=35,
        tzinfo=tz.tzoffset(None, -21600),
    )
    assert period_proto.end == datetime(
        year=2014,
        month=8,
        day=20,
        hour=21,
        minute=50,
        second=35,
        tzinfo=tz.tzoffset(None, -21600),
    )
