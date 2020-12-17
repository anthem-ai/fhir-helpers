from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from fhir_types import FHIR_Period
from proto.google.fhir.proto.r4.core import datatypes_pb2

from ..utils import convert_proto_date_time, parse_iso_datetime


class Period(ABC):
    @property
    @abstractmethod
    def start(self) -> Optional[datetime]:
        pass  # pragma: no cover

    def end(self) -> Optional[datetime]:
        pass  # pragma: no cover


class PeriodDict(Period):
    def __init__(self, data: FHIR_Period) -> None:
        self.data = data

    @property
    def start(self) -> Optional[datetime]:
        return parse_iso_datetime(self.data.get("start", ""))

    @property
    def end(self) -> Optional[datetime]:
        return parse_iso_datetime(self.data.get("end", ""))


class PeriodProto(Period):
    def __init__(
        self,
        period: datatypes_pb2.Period,
    ) -> None:
        self.period = period

    @property
    def start(self) -> Optional[datetime]:
        return convert_proto_date_time(self.period.start)

    @property
    def end(self) -> Optional[datetime]:
        return convert_proto_date_time(self.period.end)
