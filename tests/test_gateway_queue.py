"""Tests for the bounded FIFO overflow queue and its backpressure alert."""

import logging

from hw4.gateway.overflow_queue import OverflowQueue


def test_enqueue_until_full_then_backpressure(caplog):
    queue = OverflowQueue(max_size=2)
    assert queue.enqueue("a") is True
    assert queue.enqueue("b") is True
    with caplog.at_level(logging.WARNING):
        admitted = queue.enqueue("c")
    assert admitted is False
    assert queue.is_full is True
    assert any("Backpressure" in r.message for r in caplog.records)


def test_fifo_peek_and_remove():
    queue = OverflowQueue(max_size=3)
    queue.enqueue("first")
    queue.enqueue("second")
    assert queue.peek() == "first"
    queue.remove("first")
    assert queue.peek() == "second"
    assert len(queue) == 1


def test_peek_empty_returns_none():
    assert OverflowQueue(max_size=1).peek() is None


def test_remove_missing_item_is_noop():
    queue = OverflowQueue(max_size=2)
    queue.enqueue("x")
    queue.remove("not-there")  # must not raise
    assert len(queue) == 1


def test_is_full_false_when_space():
    queue = OverflowQueue(max_size=2)
    queue.enqueue("x")
    assert queue.is_full is False
