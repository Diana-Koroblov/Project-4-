# OOP Schema — Before State

This diagram represents the actual object-oriented (or lack thereof) structure of the `broken-python` codebase **before remediation**, as reverse-engineered from the source files.

## Polygons System — Before State

```mermaid
classDiagram
    class Object {
        <<Built-in — WRONG BASE>>
        ⚠️ Should be lowercase 'object'
    }

    class Polygon {
        +sides: int
        +internal_angles_sum: int
        +internal_angle: int
        +__init__(sides, internal_angles_sum, internal_angle)
        ⚠️ Inherits from 'Object' — NameError at runtime
        ⚠️ Instantiated with 'new' keyword — SyntaxError
        ⚠️ No draw() method
        ⚠️ No calculate_perimeter() method
    }

    class calc_polygon_details {
        <<God Function — module-level>>
        +sides: int
        ⚠️ Hardcoded for sides == 3 and sides == 4 only
        ⚠️ Returns dict, ignores Polygon class
        ⚠️ Uses 'new Polygon(...)' — SyntaxError
    }

    class draw_polygon {
        <<God Function — module-level>>
        +polygon_details: dict
        ⚠️ Hardcoded range(0,6) — always draws hexagon
        ⚠️ Hardcoded 60° turn — ignores polygon_details
        ⚠️ No connection to Polygon class
    }

    Object <|-- Polygon : "broken inheritance"
    calc_polygon_details ..> Polygon : "attempts 'new Polygon' (SyntaxError)"
    calc_polygon_details ..> draw_polygon : "caller passes return dict"
```

## Math Quiz System — Before State

```mermaid
classDiagram
    class mathsquiz {
        <<Procedural Script — no classes>>
        score: int (never incremented)
        ⚠️ Python 2 print syntax at top
        ⚠️ '=' used for comparison (should be '==')
        ⚠️ 'else if' instead of 'elif'
        ⚠️ Only 6 questions, claims 10
        ⚠️ All prompts labeled 'Question 1'
        ⚠️ Multiple wrong expected answers
    }

    class mathsquiz_step1 {
        <<Legacy Duplicate — module-level>>
        ⚠️ Duplicated subset of mathsquiz logic
    }

    class mathsquiz_step2 {
        <<Legacy Duplicate — module-level>>
        ⚠️ Duplicated subset of mathsquiz logic
    }

    class mathsquiz_step3 {
        <<Legacy Duplicate — module-level>>
        ⚠️ Duplicated subset of mathsquiz logic
    }

    mathsquiz_step1 --|> mathsquiz : "duplicated logic"
    mathsquiz_step2 --|> mathsquiz : "duplicated logic"
    mathsquiz_step3 --|> mathsquiz : "duplicated logic"
```

## Target Architecture — After Remediation

```mermaid
classDiagram
    class Shape {
        <<Abstract Base Class>>
        +name: str
        +draw()* 
        +calculate_perimeter()*
    }

    class Polygon {
        +sides: int
        +length: float
        +draw()
        +calculate_perimeter()
        +calculate_internal_angle()
    }

    class MainApp {
        +run_simulation()
    }

    class MathQuiz {
        +questions: list
        +score: int
        +run()
        +ask_question(q)
        +display_result()
    }

    Shape <|-- Polygon : Inheritance
    MainApp --> Polygon : Composition
```
