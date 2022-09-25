import heapq
from typing import List, Tuple

from astdiff.ast import Node


class HeightIndexedPriorityQueue:
    """
    Priority queue that keeps nodes in descending order based on height.
    """

    def __init__(self):
        self.heap: List[Tuple[int, Node]] = []

    def open(self, node: Node):
        """
        Adds children of given node to the heap.
        """
        for child in node.children:
            self.push(child)

    def push(self, node: Node):
        """
        Adds given node to the heap.
        """
        heapq.heappush(self.heap, (-node.metadata.height, node))

    def pop(self):
        """
        Pops all nodes that share the current max height.
        """
        max_height = self.peek_max()
        while self.peek_max() == max_height:
            _, node = heapq.heappop(self.heap)
            yield node

    def peek_max(self):
        """
        Returns height of the tallest node, or 0 if the heap is empty.
        """
        height, _ = (self.heap and self.heap[0]) or (0, None)
        return -height
