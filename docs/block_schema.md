# Architectural Block Schema — Before & After

## Before State (Broken)

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

### Key Observations

- **God Nodes:** `calc_polygon_details()` and `draw_polygon()` live outside the `Polygon` class, violating encapsulation entirely.
- **No shared state:** The two systems (`polygons/` and `mathsquiz/`) are fully independent — no shared imports, no shared utilities.
- **Fragmented Math Quiz:** The step files (`step1`–`step3`) duplicate logic from `mathsquiz.py` and pollute the namespace without adding value.
- **Entry points:** Both systems use top-level scripting (no `if __name__ == "__main__"` guard), making them untestable as-is.

## After State (Refactored)

This diagram shows the architecture after remediation, as captured in the after-state graph (`docs/after_state/`). The God Functions are gone, behaviour is encapsulated behind a real abstraction (`Shape` → `Polygon`), and the Math Quiz logic is consolidated into a single canonical class. The Zero-Edge isolation between the two communities is preserved — the fix never coupled them.

```mermaid
graph TD
    subgraph User_Input
        UI1[/"sides = int(input(...))"/]
        UI2[/"answer = input(...)"/]
    end

    subgraph Polygons_System["Polygons System (polygons.py)"]
        direction TB
        SHAPE["Shape(ABC)\n✅ real abstract base class\n✅ @abstractmethod draw()\n✅ @abstractmethod calculate_perimeter()"]
        POLY["Polygon(Shape)\n✅ idiomatic instantiation: Polygon(sides)\n✅ calculate_internal_angle() — formula (n-2)*180/n\n✅ calculate_perimeter()\n✅ draw() — range(self.sides), turns 360/self.sides"]
        PMAIN["if __name__ == '__main__'\n✅ guarded, testable entry point"]
    end

    subgraph MathQuiz_System["Math Quiz System (mathsquiz.py)"]
        direction TB
        MQ["MathQuiz\n✅ single canonical class\n✅ check_answer() — '==' comparison\n✅ ask_question(number, question)\n✅ run() — 10 questions, score increments\n✅ display_result()"]
        MMAIN["if __name__ == '__main__'\n✅ guarded, testable entry point"]
        LEGACY["mathsquiz-step1..3.py\n(retained as documented before-state\n& naive-baseline noise — superseded)"]
    end

    subgraph Zero_Edge_Isolation["Zero-Edge Isolation (Preserved)"]
        BARRIER[ ]
        style BARRIER fill:none,stroke:none
    end

    UI1 --> POLY
    SHAPE -->|"base class (inherits)"| POLY
    POLY --> PMAIN
    UI2 --> MQ
    MQ --> MMAIN
    LEGACY -.->|"superseded by"| MQ

    Polygons_System -.-|"NO EDGES — Zero-Edge Protocol"| MathQuiz_System
```

### Key Improvements

- **God Nodes eliminated:** `calc_polygon_details()` and `draw_polygon()` are gone; their behaviour now lives as methods on `Polygon`, restoring encapsulation.
- **Real abstraction introduced:** a new `Shape(ABC)` base declares `draw()` / `calculate_perimeter()`; `Polygon(Shape)` is the first concrete subclass — the new bridge that did not exist before.
- **Math Quiz consolidated:** all quiz logic collapses into one `MathQuiz` class. The `step1`–`step3` files are intentionally **retained** (not deleted) as the documented before-state and as the naive baseline's "noise" for the token-efficiency proof.
- **Entry points guarded:** both modules now run only under `if __name__ == "__main__"`, making them importable and testable.
- **Isolation preserved:** the two communities still share zero edges — the refactor improved each system internally without coupling them.
- **Graph delta:** these changes correspond to the **27 → 35 node** growth between [`before_state`](before_state/graph.html) and [`after_state`](after_state/graph.html) (`Polygon` 4 → 8 edges, new `Shape` hub at 6 edges). See [`knowledge_delta.md`](../obsidian/knowledge_delta.md).
