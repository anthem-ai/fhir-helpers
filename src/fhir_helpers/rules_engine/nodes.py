from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple, Type

from fhir_helpers.resources.lpr import LPR
from fhir_helpers.utils import calc_time_ago

NodeDict = Dict[str, Any]


class Node(ABC):
    required_keys: List[str] = []
    optional_keys: List[str] = []

    def __init__(self, node: NodeDict) -> None:
        self.node = node
        self._pre_validate()

    def _pre_validate(self) -> None:
        node_keys = set(self.node.keys())
        required_keys = set(["nodeType", "resource"] + self.required_keys)
        allowed_keys = required_keys.union(set(self.optional_keys))

        if not required_keys.issubset(node_keys):
            raise Exception(
                f"Expecting required keys {required_keys} but got keys {node_keys}"
            )

        if not node_keys.issubset(allowed_keys):
            raise Exception(f"Expecting keys {allowed_keys} but got keys {node_keys}")

    @abstractmethod
    def validate(self, lpr: LPR) -> Tuple[bool, NodeDict]:
        pass  # pragma: no cover


class MedicationCodeNode(Node):
    required_keys = ["coding"]
    optional_keys = ["policy", "withinLastDays", "relatedCodings"]

    def validate(self, lpr: LPR) -> Tuple[bool, NodeDict]:
        request_lambdas = [
            lambda medication_requests: medication_requests.find_by_coding(
                self.node["coding"]["code"]
            )
        ]

        medication_requests = lpr.medication_requests.or_(*request_lambdas)

        if isinstance(self.node.get("withinLastDays", None), int):
            medication_requests = medication_requests.find_after_date(
                calc_time_ago(days=self.node["withinLastDays"])
            )

        if medication_requests:
            return True, {"evaluation": True, "node": self.node}
        return False, {"evaluation": False, "node": self.node}


class ConditionCodeNode(Node):
    required_keys = ["coding"]
    optional_keys = ["policy", "withinLastDays", "relatedCodings"]

    def validate(self, lpr: LPR) -> Tuple[bool, NodeDict]:
        lambdas = [
            lambda conditions: conditions.find_by_coding(self.node["coding"]["code"])
        ]

        conditions = lpr.conditions.or_(*lambdas)

        if isinstance(self.node.get("withinLastDays", None), int):
            conditions = conditions.find_after_date(
                calc_time_ago(days=self.node["withinLastDays"])
            )

        if conditions:
            return True, {"evaluation": True, "node": self.node}
        return False, {"evaluation": False, "node": self.node}


NodeMapper: Dict[str, Type[Node]] = {
    "Condition": ConditionCodeNode,
    # "MedicationDispense": MedicationCodeNode,
    "Medication": MedicationCodeNode,
}
