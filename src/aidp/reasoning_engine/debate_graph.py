import uuid
from dataclasses import dataclass, field

from aidp.reasoning.subjective_logic import Opinion, consensus_fusion


@dataclass
class DebateNode:
    author: str
    content: str
    opinion: Opinion
    node_type: str = "claim"  # claim, critique, rebuttal
    id: str = field(default_factory=lambda: f"node_{uuid.uuid4()}")
    children: list["DebateNode"] = field(default_factory=list)
    depth: int = 0


class DebateGraph:
    """
    Directed Acyclic Graph (DAG) for recursive peer review.
    """

    def __init__(self, root_claim: str, root_author: str, initial_opinion: Opinion) -> None:
        self.root = DebateNode(author=root_author, content=root_claim, opinion=initial_opinion)
        self.max_depth = 3

    def add_critique(
        self, parent_id: str, author: str, content: str, opinion: Opinion
    ) -> DebateNode | None:
        parent = self._find_node(self.root, parent_id)
        if not parent or parent.depth >= self.max_depth:
            return None
        node = DebateNode(
            author=author,
            content=content,
            opinion=opinion,
            node_type="critique",
            depth=parent.depth + 1,
        )
        parent.children.append(node)
        return node

    def add_rebuttal(
        self, parent_id: str, author: str, content: str, opinion: Opinion
    ) -> DebateNode | None:
        parent = self._find_node(self.root, parent_id)
        if not parent or parent.node_type != "critique" or parent.depth >= self.max_depth:
            return None
        node = DebateNode(
            author=author,
            content=content,
            opinion=opinion,
            node_type="rebuttal",
            depth=parent.depth + 1,
        )
        parent.children.append(node)
        return node

    def _find_node(self, current: DebateNode, target_id: str) -> DebateNode | None:
        if current.id == target_id:
            return current
        for child in current.children:
            res = self._find_node(child, target_id)
            if res:
                return res
        return None

    def resolve(self) -> Opinion:
        return self._resolve_node(self.root)

    def _resolve_node(self, node: DebateNode) -> Opinion:
        if not node.children:
            return node.opinion
        fused = node.opinion
        for child in node.children:
            fused = consensus_fusion(fused, self._resolve_node(child))
        return fused
