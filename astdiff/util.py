import heapq
import operator
from collections import defaultdict
from functools import reduce
from itertools import product
from typing import Callable, DefaultDict, Iterable, List, Sequence, Tuple, TypeVar

from more_itertools import peekable

from astdiff.ast import Node

T = TypeVar("T")
K = TypeVar("K")


def group_by(items: Iterable[T], key_fn: Callable[[T], K]):
    initial: DefaultDict[K, T] = defaultdict(list)
    return reduce(
        lambda res, item: res[key_fn(item)].append(item) or res,
        items,
        initial,
    )


def longest_common_subsequence(
    source: Sequence[T],
    target: Sequence[T],
    equals_fn: Callable[[T, T], bool] = operator.eq,
):
    # Calculate length
    cache = defaultdict(lambda: defaultdict(int))

    for s, t in product(
        reversed(range(len(source))),
        reversed(range(len(target))),
    ):
        if equals_fn(source[s], target[t]):
            cache[s][t] = cache[s + 1][t + 1] + 1

        elif cache[s + 1][t] >= cache[s][t + 1]:
            cache[s][t] = cache[s + 1][t]

        else:
            cache[s][t] = cache[s][t + 1]

    # Collect the result
    s = peekable(range(len(source)))
    t = peekable(range(len(target)))

    while s and t:
        if equals_fn(source[s.peek()], target[t.peek()]):
            yield source[s.peek()], target[t.peek()]
            next(s)
            next(t)

        elif cache[s.peek() + 1][t.peek()] >= cache[s.peek()][t.peek() + 1]:
            next(s)

        else:
            next(t)


class HeightIndexedPriorityQueue:
    """
    Priority queue that keeps nodes in descending order based on height.
    """

    def __init__(self):
        self.heap: List[Tuple[int, Node]] = []

    def __len__(self):
        return len(self.heap)

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
