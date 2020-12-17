from typing import Any, Tuple

from fhir_helpers.resources.lpr import LPR
from fhir_helpers.rules_engine.nodes import NodeDict
from fhir_helpers.rules_engine.rules_engine import RulesEngine

from .helpers import get_example_bundle


def test_rules_engine_tree(monkeypatch: Any) -> None:
    lpr = LPR(get_example_bundle())

    def mock_eval(self: Any, node: NodeDict) -> Tuple[bool, NodeDict]:
        return node["value"], {"evaluation": node["value"], "node": node}

    monkeypatch.setattr(RulesEngine, "eval_node", mock_eval)

    query = {
        "nodeType": "and",
        "children": [
            {"value": True},
            {"value": True},
            {"nodeType": "not", "child": {"value": False}},
            {
                "nodeType": "or",
                "children": [
                    {"value": False},
                    {"value": False},
                    {"value": True},
                ],
            },
        ],
    }

    is_valid, result = RulesEngine(lpr).validate(query)
    assert is_valid

    query = {
        "nodeType": "and",
        "children": [
            {"value": True},
            {"value": True},
            {"nodeType": "not", "child": {"value": False}},
            {
                "nodeType": "or",
                "children": [
                    {"value": False},
                    {"value": False},
                    {"value": False},
                ],
            },
        ],
    }

    is_valid, result = RulesEngine(lpr).validate(query)
    assert not is_valid

    query = {
        "nodeType": "and",
        "children": [{"value": True}, {"nodeType": "not", "child": {"value": True}}],
    }

    is_valid, result = RulesEngine(lpr).validate(query)
    assert not is_valid


def test_rules_engine() -> None:
    lpr = LPR(get_example_bundle())

    query = {
        "nodeType": "and",
        "children": [
            {
                "nodeType": "resource",
                "resource": "Condition",
                "coding": {"code": "195662009", "system": "CHECK ME"},
                "withinLastDays": 10000,
            },
            {
                "nodeType": "resource",
                "resource": "Medication",
                "coding": {"code": "834061", "system": "CHECK ME"},
            },
        ],
    }

    is_valid, result = RulesEngine(lpr).validate(query)
    assert is_valid

    query = {
        "nodeType": "and",
        "children": [
            {
                "nodeType": "resource",
                "resource": "Condition",
                "coding": {"code": "195662009", "system": "CHECK ME"},
                "withinLastDays": 1,
            },
            {
                "nodeType": "resource",
                "resource": "Medication",
                "coding": {"code": "834061", "system": "CHECK ME"},
                "withinLastDays": 1,
            },
        ],
    }

    is_valid, result = RulesEngine(lpr).validate(query)
    assert not is_valid
