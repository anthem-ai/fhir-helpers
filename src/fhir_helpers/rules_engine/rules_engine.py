from typing import Tuple

from fhir_helpers.resources.lpr import LPR

from .nodes import NodeDict, NodeMapper


class RulesEngine:
    def __init__(self, lpr: LPR):
        self.lpr = lpr

    def validate(self, query: NodeDict) -> Tuple[bool, NodeDict]:
        return self.recurse_boolean_node(query)

    def recurse_node(self, node: NodeDict) -> Tuple[bool, NodeDict]:
        if node.get("nodeType", "") in {"and", "or", "not"}:
            return self.recurse_boolean_node(node)

        return self.eval_node(node)

    def recurse_boolean_node(self, node: NodeDict) -> Tuple[bool, NodeDict]:
        if node["nodeType"] == "and":
            vals, result_nodes = [], []
            for n in node["children"]:
                val, result_node = self.recurse_node(n)
                vals.append(val)
                result_nodes.append(result_node)

            copied = node.copy()
            copied["children"] = result_nodes
            return all(vals), copied

        if node["nodeType"] == "or":
            vals, result_nodes = [], []
            for n in node["children"]:
                val, result_node = self.recurse_node(n)
                vals.append(val)
                result_nodes.append(result_node)

            copied = node.copy()
            copied["children"] = result_nodes
            return any(vals), copied

        if node["nodeType"] == "not":
            val, result_node = self.recurse_node(node["child"])
            copied = node.copy()
            copied["child"] = result_node
            return not val, copied

        raise Exception(
            "Boolean Nodes must have nodeType: and, or, not"
        )  # pragma: no cover

    def eval_node(self, node: NodeDict) -> Tuple[bool, NodeDict]:
        if "resource" not in node:
            raise Exception("resource key is required")  # pragma: no cover

        try:
            node_class = NodeMapper[node["resource"]]
        except KeyError:  # pragma: no cover
            raise Exception(
                f"node for resource '{node['resource']}' does not exist"
            )  # pragma: no cover
        return node_class(node).validate(self.lpr)
