from typing import Tuple

import pytest

from fhir_helpers.resources.lpr import LPR
from fhir_helpers.rules_engine.nodes import Node, NodeDict


class NodeTest(Node):
    required_keys = ["value"]
    optional_keys = ["other_value"]

    def validate(self, lpr: LPR) -> Tuple[bool, NodeDict]:
        return True, {"evaluation": True}


def test_abstract_node_pre_validate() -> None:

    with pytest.raises(Exception, match=r"Expecting required keys"):
        NodeTest({"one": "two"})

    with pytest.raises(Exception, match=r"Expecting required keys"):
        NodeTest({"nodeType": "resource"})

    with pytest.raises(Exception, match=r"Expecting required keys"):
        NodeTest(
            {
                "nodeType": "resource",
                "resource": "",
                "val_aaa": "1",
                "other_value": "123",
            }
        )

    with pytest.raises(Exception, match=r"Expecting keys"):
        NodeTest(
            {"nodeType": "resource", "resource": "", "value": "1", "other_aaa": "123"}
        )

    with pytest.raises(Exception, match=r"Expecting keys"):
        NodeTest(
            {
                "nodeType": "resource",
                "resource": "",
                "value": "1",
                "other_value": "123",
                "other_aaa": "123",
            }
        )

    assert NodeTest({"nodeType": "resource", "resource": "", "value": "1"})
    assert NodeTest(
        {"nodeType": "resource", "resource": "", "value": "1", "other_value": "123"}
    )
