# Architectural Block Schema — Before State

This diagram shows the actual (before-state) architecture of the `broken-python` repository as extracted by Graphify. Both systems are procedural, isolated from each other, and each has distinct structural problems.

```mermaid
graph TD
    subgraph User_Input
        UI1[/"sides = int(input(...))"/]
        UI2[/"answer = input(...)"/]
    end

    subgraph Polygons_System["Polygons System (polygons.py)"]
        direction TB
        PC[Polygon class\n⚠️ inherits from 'Object' — NameError\n⚠️ instantiated with 'new' — SyntaxError]
        GF1["calc_polygon_details(sides)\n⚠️ God Function — lives outside class\n⚠️ Hardcoded only for 3 & 4 sides\n⚠️ Uses 'new Polygon(...)' — SyntaxError"]
        GF2["draw_polygon(polygon_details)\n⚠️ God Function — lives outside class\n⚠️ Hardcoded range(0,6) + 60° — always draws hexagon"]
        PRINT[Print polygon details]
    end

    subgraph MathQuiz_System["Math Quiz System (mathsquiz.py + step files)"]
        direction TB
        STEP1[mathsquiz-step1.py\nLegacy clutter]
        STEP2[mathsquiz-step2.py\nLegacy clutter]
        STEP3[mathsquiz-step3.py\nLegacy clutter]
        MAIN[mathsquiz.py\n⚠️ print without parens — Python 2 syntax\n⚠️ if answer = N — assignment not comparison\n⚠️ else if — should be elif\n⚠️ score never incremented\n⚠️ Only 6 questions, claims 10\n⚠️ All labels say 'Question 1'\n⚠️ Multiple wrong answers]
    end

    subgraph Zero_Edge_Isolation["Zero-Edge Isolation (Enforced by Orchestrator)"]
        BARRIER[ ]
        style BARRIER fill:none,stroke:none
    end

    UI1 --> GF1
    GF1 --> PC
    GF1 --> PRINT
    PRINT --> GF2
    UI2 --> MAIN
    STEP1 -.->|duplicated logic| MAIN
    STEP2 -.->|duplicated logic| MAIN
    STEP3 -.->|duplicated logic| MAIN

    Polygons_System -.-|"NO EDGES — Zero-Edge Protocol"| MathQuiz_System
```

## Key Observations

- **God Nodes:** `calc_polygon_details()` and `draw_polygon()` live outside the `Polygon` class, violating encapsulation entirely.
- **No shared state:** The two systems (`polygons/` and `mathsquiz/`) are fully independent — no shared imports, no shared utilities.
- **Fragmented Math Quiz:** The step files (`step1`–`step3`) duplicate logic from `mathsquiz.py` and pollute the namespace without adding value.
- **Entry points:** Both systems use top-level scripting (no `if __name__ == "__main__"` guard), making them untestable as-is.
