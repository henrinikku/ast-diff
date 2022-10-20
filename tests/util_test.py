from astdiff.ast import Node, NodeMetadata
from astdiff.util import HeightIndexedPriorityQueue, longest_common_subsequence


def test_longest_common_subsequence_empty_source():
    assert list(longest_common_subsequence("", "12345")) == []


def test_longest_common_subsequence_empty_input():
    assert list(longest_common_subsequence("", "")) == []


def test_longest_common_subsequence_short_equal_strings():
    source = target = "12345"
    assert list(longest_common_subsequence(source, target)) == list(zip(source, target))


def test_longest_common_subsequence_one_common_character():
    source = "12345"
    target = "4"
    assert list(longest_common_subsequence(source, target)) == [("4", "4")]


def test_longest_common_subsequence_no_common_characters():
    source = "12345"
    target = "67890"
    assert list(longest_common_subsequence(source, target)) == []


def test_longest_common_subsequence_reversed_input():
    source = "12345"
    target = "54321"
    assert list(longest_common_subsequence(source, target)) == [("5", "5")]
    assert list(longest_common_subsequence(target, source)) == [("1", "1")]


def test_longest_common_subsequence_non_continuous_match():
    source = "1_2_3_4_5"
    target = "235"
    result = list(longest_common_subsequence(source, target))
    assert result == list(zip(target, target))


def test_longest_common_subsequence_continuous_match_at_start():
    source = "saippuakauppias"
    target = "saippua"
    assert list(longest_common_subsequence(source, target)) == list(zip(target, target))


def test_longest_common_subsequence_continuous_match_at_end():
    source = "saippuakauppias"
    target = "kauppias"
    assert list(longest_common_subsequence(source, target)) == list(zip(target, target))


def test_longest_common_subsequence_wikipedia_example():
    source = "ABCD"
    target = "ACBAD"
    result = list(longest_common_subsequence(source, target))
    assert all(s == t for s, t in result)
    assert [s for s, t in result] == ["A", "C", "D"]


def test_height_indexed_priority_queue():
    tree1 = Node(
        "foo",
        "foo",
        children=(
            Node("foo", "foo", metadata=NodeMetadata(hashcode=0, height=4, size=0)),
            Node("foo", "foo", metadata=NodeMetadata(hashcode=0, height=4, size=0)),
            Node("foo", "foo", metadata=NodeMetadata(hashcode=0, height=3, size=0)),
        ),
        metadata=NodeMetadata(hashcode=0, height=5, size=0),
    )
    tree2 = Node("bar", "bar", metadata=NodeMetadata(hashcode=0, height=1, size=0))

    queue = HeightIndexedPriorityQueue()
    queue.push(tree1)
    queue.push(tree2)
    assert queue.peek_max() == 5
    assert list(queue.pop()) == [tree1]
    assert queue.peek_max() == 1

    queue.open(tree1)
    assert len(queue) == 4
    assert queue.peek_max() == 4
    assert list(queue.pop()) == [tree1.children[0], tree1.children[1]]
    assert list(queue.pop()) == [tree1.children[2]]
    assert queue.peek_max() == 1
    assert list(queue.pop()) == [tree2]
    assert len(queue) == 0
    assert queue.peek_max() == 0
