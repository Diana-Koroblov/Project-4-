"""Unit tests for the refactored Polygons system.

These tests target the fixed src/broken-python/polygons/polygons.py
after Subagent Alpha completes its remediation.
"""

import pytest


# ---------------------------------------------------------------------------
# Tests will be filled in once the refactored Polygon class is in place.
# The structure below follows the target OOP architecture from docs/oop_schema.md
# ---------------------------------------------------------------------------


class TestPolygonInit:
    """Test Polygon class instantiation."""

    def test_triangle_sides(self):
        pytest.skip("Implement after Phase 4 refactoring")

    def test_square_sides(self):
        pytest.skip("Implement after Phase 4 refactoring")

    def test_hexagon_sides(self):
        pytest.skip("Implement after Phase 4 refactoring")


class TestPolygonPerimeter:
    """Test Polygon.calculate_perimeter()."""

    def test_triangle_perimeter(self):
        pytest.skip("Implement after Phase 4 refactoring")

    def test_square_perimeter(self):
        pytest.skip("Implement after Phase 4 refactoring")


class TestPolygonInternalAngle:
    """Test Polygon.calculate_internal_angle()."""

    def test_triangle_angle(self):
        """Internal angle of equilateral triangle = 60°."""
        pytest.skip("Implement after Phase 4 refactoring")

    def test_square_angle(self):
        """Internal angle of square = 90°."""
        pytest.skip("Implement after Phase 4 refactoring")

    def test_hexagon_angle(self):
        """Internal angle of regular hexagon = 120°."""
        pytest.skip("Implement after Phase 4 refactoring")

    def test_generic_polygon_angle(self):
        """Formula: (sides - 2) * 180 / sides."""
        pytest.skip("Implement after Phase 4 refactoring")


class TestPolygonInheritance:
    """Test that Polygon correctly inherits from Shape."""

    def test_polygon_is_shape(self):
        pytest.skip("Implement after Phase 4 refactoring")
