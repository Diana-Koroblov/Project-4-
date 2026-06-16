"""Unit tests for the refactored Polygons system (Phase 4).

Targets the OOP after-state of src/broken-python/polygons/polygons.py:
an abstract `Shape` base class and a `Polygon(Shape)` that owns the geometry
and drawing that previously lived in module-level "God Functions".
"""

import sys
from pathlib import Path

import pytest

_POLYGONS_DIR = Path(__file__).resolve().parents[1] / "src" / "broken-python" / "polygons"
sys.path.insert(0, str(_POLYGONS_DIR))

import polygons  # noqa: E402
from polygons import Polygon, Shape  # noqa: E402


class _FakeTurtle:
    """Records the pen movements so draw() can be tested without a display."""

    def __init__(self):
        self.forwards = []
        self.turns = []

    def pen(self, **kwargs):
        pass

    def forward(self, distance):
        self.forwards.append(distance)

    def right(self, angle):
        self.turns.append(angle)


class _FakeTurtleModule:
    def __init__(self, fake_turtle):
        self._fake_turtle = fake_turtle

    def Screen(self):
        return object()

    def Turtle(self):
        return self._fake_turtle


class TestPolygonInit:
    def test_default_length(self):
        p = Polygon(4)
        assert p.sides == 4
        assert p.length == 50

    def test_custom_length(self):
        p = Polygon(3, length=12)
        assert p.sides == 3
        assert p.length == 12


class TestPolygonPerimeter:
    @pytest.mark.parametrize(
        "sides, length, expected",
        [(3, 10, 30), (4, 5, 20), (5, 2, 10), (6, 1, 6)],
    )
    def test_perimeter(self, sides, length, expected):
        assert Polygon(sides, length).calculate_perimeter() == expected


class TestPolygonInternalAngle:
    @pytest.mark.parametrize(
        "sides, expected",
        [(3, 60), (4, 90), (5, 108), (6, 120)],
    )
    def test_internal_angle(self, sides, expected):
        assert Polygon(sides).calculate_internal_angle() == expected

    @pytest.mark.parametrize(
        "sides, expected",
        [(3, 180), (4, 360), (5, 540), (6, 720)],
    )
    def test_internal_angles_sum(self, sides, expected):
        assert Polygon(sides).calculate_internal_angles_sum() == expected


class TestPolygonDraw:
    def test_draw_traces_a_pentagon(self, monkeypatch):
        fake = _FakeTurtle()
        monkeypatch.setattr(polygons, "turtle", _FakeTurtleModule(fake))
        Polygon(5, length=40).draw()
        # one forward + one turn per side, exterior angle 360/5 = 72 (a pentagon)
        assert fake.forwards == [40] * 5
        assert fake.turns == [72] * 5


class TestPolygonInheritance:
    def test_polygon_is_shape(self):
        assert issubclass(Polygon, Shape)
        assert isinstance(Polygon(4), Shape)

    def test_shape_is_abstract(self):
        with pytest.raises(TypeError):
            Shape()
