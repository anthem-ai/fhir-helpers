import json
from abc import ABC, abstractmethod
from typing import List, Literal, cast

from fhir_types import FHIR_HumanName
from google.fhir.r4.json_format import print_fhir_to_json_string
from proto.google.fhir.proto.r4.core import datatypes_pb2

HumanNameUse = Literal[
    "usual", "official", "temp", "nickname", "anonymous", "old", "maiden"
]


class HumanName(ABC):
    @property
    @abstractmethod
    def text(self) -> str:
        pass  # pragma: no cover

    @property
    @abstractmethod
    def family(self) -> str:
        pass  # pragma: no cover

    @property
    @abstractmethod
    def given(self) -> List[str]:
        pass  # pragma: no cover

    @property
    @abstractmethod
    def prefix(self) -> List[str]:
        pass  # pragma: no cover

    @property
    @abstractmethod
    def suffix(self) -> List[str]:
        pass  # pragma: no cover

    @property
    @abstractmethod
    def use(self) -> HumanNameUse:
        pass  # pragma: no cover

    # https://www.programcreek.com/java-api-examples/?api=org.hl7.fhir.dstu3.model.HumanName
    @property
    def display_name(self) -> str:
        name = ""
        if self.text:
            name += f"{self.text} "
        else:
            for g in self.given:
                name += f"{g} "
            if self.family:
                name += f"{self.family} "

        if self.use != "usual":
            name += f"({self.use})"

        return name.strip()


class HumanNameDict(HumanName):
    def __init__(self, data: FHIR_HumanName) -> None:
        self.data = data

    @property
    def text(self) -> str:
        return self.data.get("text", "")

    @property
    def family(self) -> str:
        return self.data.get("family", "")

    @property
    def given(self) -> List[str]:
        return self.data.get("given", [])

    @property
    def prefix(self) -> List[str]:
        return self.data.get("prefix", [])

    @property
    def suffix(self) -> List[str]:
        return self.data.get("suffix", [])

    @property
    def use(self) -> HumanNameUse:
        return self.data.get("use", "usual")


class HumanNameProto(HumanName):
    def __init__(
        self,
        human_name: datatypes_pb2.HumanName,
    ) -> None:
        self.human_name = human_name

    @property
    def text(self) -> str:
        return self.human_name.text.value

    @property
    def family(self) -> str:
        return self.human_name.family.value

    @property
    def given(self) -> List[str]:
        return list(map(lambda v: v.value, self.human_name.given))

    @property
    def prefix(self) -> List[str]:
        return list(map(lambda v: v.value, self.human_name.prefix))

    @property
    def suffix(self) -> List[str]:
        return list(map(lambda v: v.value, self.human_name.suffix))

    @property
    def use(self) -> HumanNameUse:
        # TODO: There should be a better way
        return cast(
            HumanNameUse,
            json.loads(print_fhir_to_json_string(self.human_name.use) or "usual"),
        )
