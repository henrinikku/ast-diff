from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, Set

from astdiff.ast.node import Node
from astdiff.context import DiffContext, NodeId


@dataclass
class Mapping:
    """
    Represents possible mappings between isomorphic nodes.
    """

    source_ids: Set[NodeId] = field(default_factory=set)
    target_ids: Set[NodeId] = field(default_factory=set)

    def max_size(self, context: DiffContext):
        """
        Returns the size of the largest source node.
        """
        return max(
            context.source_nodes[source_id].metadata.size
            for source_id in self.source_ids
        )

    @property
    def duplicate(self):
        """
        Tells whether self represents a non-unique, non-empty mapping.
        """
        return (
            self.source_ids
            and self.target_ids
            and (len(self.source_ids) > 1 or len(self.target_ids) > 1)
        )

    @property
    def unique(self):
        """
        Tells whether self represents an unique mapping.
        """
        return len(self.source_ids) == len(self.target_ids) == 1

    @property
    def unmatched(self):
        """
        Tells whether self is empty.
        """
        return not all((self.source_ids, self.target_ids))


class MappingStore:
    """
    Helper class for grouping matching (i.e. isomorphic) nodes.
    """

    def __init__(self):
        self.mappings: Dict[int, Mapping] = defaultdict(Mapping)

    def add_source(self, node: Node):
        """
        Adds a source node to the set of mappings.
        """
        self.mappings[node.metadata.hashcode].source_ids.add(id(node))

    def add_target(self, node: Node):
        """
        Adds a target node to the set of mappings.
        """
        self.mappings[node.metadata.hashcode].target_ids.add(id(node))

    def candidate_mappings(self):
        """
        Yields mappings with more than one possible mapping.
        """
        return (x for x in self.mappings.values() if x.duplicate)

    def unique_mappings(self):
        """
        Yields mappings with exactly one possible mapping.
        """
        return (x for x in self.mappings.values() if x.unique)

    def unmatched_mappings(self):
        """
        Yields mappings with nodes only on one side.
        """
        return (x for x in self.mappings.values() if x.unmatched)
