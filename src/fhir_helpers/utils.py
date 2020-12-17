import operator
from datetime import date, datetime
from typing import Any, Literal, Optional

from dateutil import tz
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from google.protobuf import message
from proto.google.fhir.proto.r4.core import datatypes_pb2

ComparatorType = Literal["=", ">", ">=", "<", "<="]

ComparatorFunc = {
    "=": operator.eq,
    ">": operator.gt,
    ">=": operator.ge,
    "<": operator.lt,
    "<=": operator.le,
}


def tz_conv(s: str) -> int:
    try:
        base = 1
        if s[0] == "-":
            base = -1
            s = s[1:]
        parts = [int(x) for x in s.split(":")]
        return base * (parts[0] * 3600 + parts[1] * 60)
    except Exception:
        return 0


# https://stackoverflow.com/questions/5802108/how-to-check-if-a-datetime-object-is-localized-with-pytz
def _is_tz_aware(dt: datetime) -> bool:
    return dt.tzinfo is not None and dt.tzinfo.utcoffset(dt) is not None


def _ensure_tz_aware(dt: datetime) -> datetime:
    if not _is_tz_aware(dt):
        return dt.replace(tzinfo=tz.tzutc())
    return dt


def get_years_since_datetime(resource_date: datetime) -> int:
    return relativedelta(
        datetime.now(tz=tz.tzutc()), _ensure_tz_aware(resource_date)
    ).years


def get_years_since_date(resource_date: date) -> int:
    return relativedelta(date.today(), resource_date).years


def parse_iso_datetime(str_datetime: str) -> Optional[datetime]:
    return _ensure_tz_aware(parse(str_datetime)) if str_datetime else None


def parse_iso_date(str_datetime: str) -> Optional[date]:
    return parse(str_datetime).date() if str_datetime else None


def convert_proto_date_time(
    proto_datetime: datatypes_pb2.DateTime,
) -> Optional[datetime]:
    if not proto_datetime.ByteSize():
        return None

    return datetime.fromtimestamp(
        proto_datetime.value_us / 1_000_000,
        tz=tz.tzoffset(None, tz_conv(proto_datetime.timezone)),
    )


def convert_proto_date(
    proto_date: datatypes_pb2.Date,
) -> Optional[date]:
    if not proto_date.ByteSize():
        return None

    return datetime.fromtimestamp(
        proto_date.value_us / 1_000_000,
    ).date()


def check_after_date(
    after_date: datetime,
    resource_date: Optional[datetime] = None,
) -> bool:
    return (
        _ensure_tz_aware(after_date) < _ensure_tz_aware(resource_date)
        if resource_date
        else False
    )


def check_before_date(
    before_date: datetime,
    resource_date: Optional[datetime] = None,
) -> bool:
    return (
        _ensure_tz_aware(before_date) > _ensure_tz_aware(resource_date)
        if resource_date
        else False
    )


def ensure_non_null_date(dt: Optional[datetime]) -> datetime:
    if not dt:
        return datetime(1900, 1, 1, tzinfo=tz.tzutc())
    return dt


# Rough calculation, could be improved, but reasonably close
def calc_time_ago(years: int = 0, months: int = 0, days: int = 0) -> datetime:
    return datetime.now(tz=tz.tzutc()) - relativedelta(
        years=years, months=months, days=days
    )


def search(val: Any, search_str: str) -> bool:
    if type(val) is dict:
        for k, v in val.items():
            if search(v, search_str):
                return True

    if type(val) is list:
        for v in val:
            if search(v, search_str):
                return True

    if type(val) is str:
        if search_str.lower() in val.lower():
            return True

    return False


# https://stackoverflow.com/questions/29148391/looping-over-protocol-buffers-attributes-in-python
def search_proto(proto: message.Message, search_str: str) -> bool:
    for descriptor, value in proto.ListFields():
        if descriptor.type == descriptor.TYPE_MESSAGE:
            # Is List
            if descriptor.label == descriptor.LABEL_REPEATED:
                for val in value:
                    if search_proto(val, search_str):
                        return True
            # Is Object
            elif search_proto(value, search_str):
                return True

        elif descriptor.type == descriptor.TYPE_STRING and type(value) is str:
            if search_str.lower() in value.lower():
                return True

    return False
