"""Unit tests for interaction filtering logic."""

from app.models.interaction import InteractionLog
from app.routers.interactions import _filter_by_item_id


def _make_log(id: int, learner_id: int, item_id: int) -> InteractionLog:
    return InteractionLog(id=id, learner_id=learner_id, item_id=item_id, kind="attempt")


def test_filter_returns_all_when_item_id_is_none() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, None)
    assert result == interactions


def test_filter_returns_empty_for_empty_input() -> None:
    result = _filter_by_item_id([], 1)
    assert result == []


def test_filter_returns_interaction_with_matching_ids() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, 1)
    assert len(result) == 1
    assert result[0].id == 1


def test_filter_excludes_interaction_with_different_learner_id() -> None:
    """Filter by item_id=1 should include interaction with item_id=1, learner_id=2."""
    interactions = [_make_log(1, 2, 1), _make_log(2, 1, 2)]
    result = _filter_by_item_id(interactions, 1)
    assert len(result) == 1
    assert result[0].item_id == 1
    assert result[0].learner_id == 2


def test_filter_returns_multiple_when_same_item_id() -> None:
    """Multiple interactions can share the same item_id; filter returns all of them."""
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 1), _make_log(3, 3, 2)]
    result = _filter_by_item_id(interactions, 1)
    assert len(result) == 2
    assert {r.id for r in result} == {1, 2}
    assert all(r.item_id == 1 for r in result)


def test_filter_returns_empty_when_no_match() -> None:
    """Filter by item_id that no interaction has returns empty list."""
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, 99)
    assert result == []


def test_filter_preserves_order() -> None:
    """Filtered results preserve the order of the input list."""
    interactions = [_make_log(3, 1, 1), _make_log(1, 2, 1), _make_log(2, 3, 1)]
    result = _filter_by_item_id(interactions, 1)
    assert [r.id for r in result] == [3, 1, 2]


def test_filter_item_id_zero() -> None:
    """Filter by item_id=0 returns interactions with item_id=0 (boundary value)."""
    interactions = [_make_log(1, 1, 0), _make_log(2, 2, 1)]
    result = _filter_by_item_id(interactions, 0)
    assert len(result) == 1
    assert result[0].item_id == 0
    assert result[0].id == 1


