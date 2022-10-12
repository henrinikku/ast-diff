from dataclasses import dataclass, field, replace
from functools import total_ordering
from typing import Dict, Iterable

from more_itertools import first

from astdiff.ast import Node
from astdiff.edit_script import EditScript

NodeId = int


@total_ordering
@dataclass(frozen=True)
class MatchingPair:
    source: NodeId
    target: NodeId

    def __lt__(self, other: "MatchingPair"):
        return (self.source, self.target) < (other.source, other.target)


@dataclass(frozen=True)
class MatchingSet:
    source_target_map: Dict[NodeId, NodeId] = field(default_factory=dict)
    target_source_map: Dict[NodeId, NodeId] = field(default_factory=dict)

    def add(self, pair: MatchingPair):
        assert not self.matched(pair)

        self.source_target_map[pair.source] = pair.target
        self.target_source_map[pair.target] = pair.source

    def update(self, pairs: Iterable[MatchingPair]):
        for pair in pairs:
            self.add(pair)

    def matched(self, pair: MatchingPair):
        return (
            pair.source in self.source_target_map
            or pair.target in self.target_source_map
        )

    def __len__(self):
        assert len(self.source_target_map) == len(self.target_source_map)
        return len(self.source_target_map)

    @property
    def pairs(self):
        return (MatchingPair(s, t) for s, t in self.source_target_map.items())


@dataclass
class DiffContext:
    """
    Helper class for holding data that need to be passed along
    between different stages of the algorithm.
    """

    # In data structures that require hashing, nodes are stored and acccessed
    # by their ids in order to avoid recursive hash computations.
    source_nodes: Dict[NodeId, Node]
    target_nodes: Dict[NodeId, Node]

    matching_set: MatchingSet = field(default_factory=MatchingSet)
    edit_script: EditScript = field(default_factory=tuple)

    def copy(self, **changes):
        return replace(self, **changes)

    # TODO: Finish and use before edit script generation
    # def deepcopy(self):
    #     old_source_root = first(self.source_nodes.values())
    #     old_target_root = first(self.target_nodes.values())

    #     new_source_root = copy.deepcopy(old_source_root)
    #     new_target_root = copy.deepcopy(old_target_root)

    #     old_new_id_map = {
    #         id(old_node): id(new_node)
    #         for old_node, new_node in chain(
    #             zip(pre_order_walk(old_source_root), pre_order_walk(new_source_root)),
    #             zip(pre_order_walk(old_target_root), pre_order_walk(new_target_root)),
    #         )
    #     }

    #     new_source_target_map = {
    #         old_new_id_map[k]: old_new_id_map[v]
    #         for k, v in self.matching_set.source_target_map.items()
    #     }
    #     new_target_source_map = {
    #         old_new_id_map[k]: old_new_id_map[v]
    #         for k, v in self.matching_set.target_source_map.items()
    #     }

    #     new_source_nodes = {id(x) for x in pre_order_walk(new_source_root)}
    #     new_target_nodes = {id(x) for x in pre_order_walk(new_target_root)}

    #     return DiffContext(
    #         source_nodes=new_source_nodes,
    #         target_nodes=new_target_nodes,
    #         matching_set=MatchingSet(new_source_target_map, new_target_source_map),
    #         edit_script=copy.copy(self.edit_script),
    #     )

    def partner(self, node: Node):
        target_id = self.matching_set.source_target_map.get(id(node))
        if target_id is not None:
            return self.target_nodes[target_id]

        source_id = self.matching_set.target_source_map.get(id(node))
        if source_id is not None:
            return self.source_nodes[source_id]

        return None

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
