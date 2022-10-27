from copy import deepcopy
from dataclasses import dataclass, field
from functools import total_ordering
from typing import Dict, Iterable

from more_itertools import first

from astdiff.ast.node import Node
from astdiff.ast.traversal import pre_order_walk
from astdiff.editscript import EditScript

NodeId = int


@total_ordering
@dataclass(frozen=True)
class MatchingPair:
    """
    Represents a pair of matched nodes.
    """

    source: NodeId
    target: NodeId

    def __lt__(self, other: "MatchingPair"):
        return (self.source, self.target) < (other.source, other.target)


@dataclass(frozen=True)
class MatchingSet:
    """
    Represents a set of matches between nodes.
    """

    source_target_map: Dict[NodeId, NodeId] = field(default_factory=dict)
    target_source_map: Dict[NodeId, NodeId] = field(default_factory=dict)

    def add(self, pair: MatchingPair):
        """
        Adds given match to self.
        """
        assert not self.matched(pair)

        self.source_target_map[pair.source] = pair.target
        self.target_source_map[pair.target] = pair.source

    def update(self, pairs: Iterable[MatchingPair]):
        """
        Adds given matches to self.
        """
        for pair in pairs:
            self.add(pair)

    def matched(self, pair: MatchingPair):
        """
        Tells whether at least one node in the given match is already matched.
        """
        return (
            pair.source in self.source_target_map
            or pair.target in self.target_source_map
        )

    def __len__(self):
        assert len(self.source_target_map) == len(self.target_source_map)
        return len(self.source_target_map)

    @property
    def pairs(self):
        """
        Yields all matching pairs in self.
        """
        return (MatchingPair(s, t) for s, t in self.source_target_map.items())


@dataclass(init=False)
class DiffContext:
    """
    Helper class for holding data that need to be passed along
    between different stages of the algorithm.
    """

    # In data structures that require hashing, nodes are stored and acccessed
    # by their ids in order to distinguish nodes with equal values from each other.
    source_nodes: Dict[NodeId, Node]
    target_nodes: Dict[NodeId, Node]

    matching_set: MatchingSet
    edit_script: EditScript

    def __init__(self, source_tree: Node, target_tree: Node):
        self.source_nodes = {id(x): x for x in pre_order_walk(deepcopy(source_tree))}
        self.target_nodes = {id(x): x for x in pre_order_walk(deepcopy(target_tree))}
        self.matching_set = MatchingSet()
        self.edit_script = EditScript()

    def add_source(self, node: Node):
        """
        Adds a new source node to self.
        """
        assert id(node) not in self.source_nodes
        self.source_nodes[id(node)] = node
        for child in node.children:
            self.add_source(child)

    def remove_source(self, node: Node):
        """
        Removes a source node from self.
        """
        assert id(node) in self.source_nodes
        self.source_nodes.pop(id(node))
        for child in node.children:
            self.remove_source(child)

    def partner(self, node: Node):
        """
        Returns the partner of given node, i.e., a source node for target node
        and vice versa.
        """
        target_id = self.matching_set.source_target_map.get(id(node))
        if target_id is not None:
            return self.target_nodes[target_id]

        source_id = self.matching_set.target_source_map.get(id(node))
        if source_id is not None:
            return self.source_nodes[source_id]

        return None

    def unmatched(self, node: Node):
        """
        Tells whether given node is not matched.
        """
        return self.partner(node) is None

    @property
    def source_root(self):
        return first(self.source_nodes.values())

    @property
    def target_root(self):
        return first(self.target_nodes.values())

    @property
    def matched_nodes(self):
        return (
            (self.source_nodes[x.source], self.target_nodes[x.target])
            for x in self.matching_set.pairs
        )
