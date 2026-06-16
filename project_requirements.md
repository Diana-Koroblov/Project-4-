Guidelines for Writing Professional Software at the Highest Level of Excellence.
Dr. Yoram Segal.
All Rights Reserved - Dr. Yoram Segal.
Date: 2026-03-26.
Version: 3.00.

1 Introduction - The Professional Programmer in the AI Era.
1.1 What is a professional programmer?
A professional programmer (Professional Software Engineer) is not only someone who knows how to write code, but someone who understands the full software lifecycle, knows how to plan, document, test, and maintain complex systems. A professional programmer meets high standards of code quality, adheres to proven best practices, and is capable of working in a team while maintaining consistency, clear communication, and responsibility.
The main characteristics of a professional programmer include:
* Systemic thinking - the ability to see the big picture and understand how each component fits into the entire system.
* Planning before execution - writing requirements, architecture, and planning documents before the first line of code.
* Uncompromising quality - strict adherence to writing clean, documented, test-covered, and secure code.
* Continuous learning - updating knowledge with new technologies, tools, and methodologies.
* Effective communication - the ability to describe technical solutions to diverse audiences.

1.2 Teamwork in software development.
Professional software development is almost always done in a team. Effective teamwork is based on several key principles:
* Roles and responsibilities - a typical development team includes a Software Architect responsible for system design, Developers who implement the code, a QA Engineer who verifies product quality, a Product Manager who defines requirements, and sometimes a DevOps developer responsible for infrastructure and deployment processes.
* Work processes - professional teams work with methodologies such as Scrum, SAFE, or Kanban, which include daily standups, sprint reviews, retrospectives, and mutual code reviews via Pull Requests.
* Shared standards - the team defines and adheres to coding standards, uniform project structures, and automated CI/CD testing and deployment processes.

1.3 Software project lifecycle.
Every professional software project goes through a defined Software Development Life Cycle (SDLC):
1. Requirements definition - writing a detailed Product Requirements Document (PRD).
2. Planning and architecture - system design, writing planning documents (PLAN), and setting milestones (TODO).
3. Development - writing code according to the plan, using a Test-Driven Development (TDD) approach.
4. Testing - unit, integration, and system tests.
5. Deployment - distributing the software to the production environment.
6. Maintenance and improvement - fixing bugs, adding features, and upgrading.

1.4 The Revolution: AI and Prompt-Driven Coding.
In the current era, Artificial Intelligence (AI) and AI agents are fundamentally changing how software is developed. Prompt-driven coding (Vibe Coding)—where a programmer instructs AI agents to create, test, and improve code—allows a single programmer to function as a Senior Software Architect orchestrating multiple AI agents simultaneously.
* Doubling production capacity: A programmer working with AI agents and using prompt-driven coding can produce 16 times more high-quality lines of code in a given timeframe compared to manual writing without AI. This means any programmer, regardless of seniority or prior experience, can become a high-level professional programmer provided they follow the rules and processes defined in this document.
* The first and most important rule: To harness the full potential of AI agents, you must define clear and detailed requirements. Without requirements, planning, and architecture documents, AI agents will generate code that might work but won't meet professional standards. Therefore, the first rule of professional coding with AI is to define and demand full documentation before any line of code.
* This document defines all the requirements, standards, and processes that must be met to create professional software at the highest level. Follow these guidelines, and you can leverage the full power of AI agents and become a software architect who orchestrates a team of agents, producing professional-level results that were previously impossible.

2 Mandatory Project Structure and Documentation Documents.
Every professional software project must include a minimal folder structure and documentation documents. Without these documents, the project will not be considered as meeting the minimum requirements.

2.1 README.md File in the Project Root.
Every project must include a README.md file in the root directory. This file serves as a complete user manual and includes:
* Installation Instructions - System requirements, step-by-step installation, environment variable setup, and common troubleshooting.
* Usage Instructions - Execution in different modes, flags and options, typical CLI/GUI workflows.
* Examples and Demonstrations - Code examples, screenshots, common use cases.
* Configuration Guide - Explanation of configuration files, parameters, and their effects.
* Contribution Guidelines - Code and style standards.
* License & Credits - Usage license and attribution for third-party libraries.

2.2 /docs Folder - Mandatory Documentation Documents.
Every project must include a /docs folder in the project root, containing at least the following documents:
1. Product Requirements Document (docs/PRD.md).
The PRD is the central document defining the project's purpose and its requirements. The document includes:
* Project overview and context, user problem description, market analysis, and target audience identification.
* Measurable goals, KPIs, and acceptance criteria.
* Functional and non-functional requirements, user stories, and use cases.
* Assumptions, dependencies, constraints, and out-of-scope items.
* Timeline and milestones with expected deliverables.

2. Planning Document (docs/PLAN.md).
The planning document describes the architecture and technical design of the project, and includes:
* C4 Model (Context, Container, Component, Code) diagrams.
* UML diagrams for complex processes and deployment diagrams.
* API and interface documentation, data schemas, and contracts.
* Architectural Decision Records (ADRs) with rationale and alternatives trade-offs.

3. Tasks Document (docs/TODO.md).
The tasks document details all the tasks required to implement the project:
* Detailed task list with priorities and status (Not Started / In Progress / Completed).
* Division into phases with milestones.
* Assignment of responsibility for each task.
* Definition of done for each task.

2.3 Dedicated PRD Documents for Algorithms and Mechanisms.
Important requirement: For every specific algorithm, core mechanism, or complex technical component in the project, you must create a dedicated and separate PRD document. For example:
* Machine learning algorithm - docs/PRD_ml_algorithm.md.
* User authentication mechanism - docs/PRD_authentication.md.
* Search engine - docs/PRD_search_engine.md.
* Caching system - docs/PRD_caching.md.
Each dedicated PRD document includes:
* A detailed description of the algorithm or mechanism, including theoretical background.
* Specific requirements, expected input/output, and performance metrics.
* Constraints and limitations, alternatives considered, and an explanation of the choice.
* Success criteria and specific test scenarios.

2.4 Recommended Project Structure.
(Omitted raw directory tree code structure, follow standard Python modular organization as detailed in the source).

2.5 Mandatory Workflow.
The mandatory workflow is:
1. Product Requirements Document (docs/PRD.md) and its approval before proceeding.
2. Architectural Planning (docs/PLAN.md).
3. Task List (docs/TODO.md).
4. Creation of dedicated PRD documents for every core algorithm/mechanism.
5. Approval of all documents before starting development.
6. Starting development - updating TODO.md with progress.
7. Saving results, creating visualizations, and updating README.md.

3 Code Documentation and Project Structure.
3.1 Modular Project Structure.
Proper organization of the project structure is key to efficient maintenance and future code development. Organizational principles include logical division of the project into folders by role, such as source code, tests, documentation, data, results, configuration, and resources. The organization can be feature-based or a layered architecture, while maintaining clear separation between code, data, results, and documentation.

3.2 File Size Rule - Maximum 150 Lines.
Every code file must not exceed 150 lines of code (blank lines and comment lines are not counted). When a file exceeds the limit, it must be split into multiple files—never compress code to fit the limit.
Splitting strategies:
* Extracting helper functions - independent functions to a separate file.
* 50/50 split - when a class has multiple responsibilities (mixin) or when there are two logical halves (read/write).
* Extracting constants - constants to a constants.py file.
* Extracting models - model definitions to a separate file.

3.3 Code Quality and Comments.
Code quality is measured not only by its functionality but also by its ease of reading and maintenance. Code Comments Standards require that comments explain the "why" and not just the "what". Every function, class, and module should include detailed Docstrings. Comments should explain complex design decisions, document assumptions and preconditions, and be updated alongside code changes.
Principles of writing high-quality code include using descriptive and accurate variable and function names, writing short and focused functions that adhere to the Single Responsibility Principle, avoiding duplicate code according to the DRY (Don't Repeat Yourself) principle, and maintaining code style consistency throughout the project.

4 SDK Architecture and Object-Oriented Design.
4.1 SDK-Based Architecture.
Every function containing business logic must be accessible through an SDK layer. The SDK is the sole entry point for all consumers: GUI menus, CLI, third-party integrations, and future services.
Architectural requirements:
* Every business function is exposed via an SDK class.
* No business logic in CLI, GUI, or controller layers—these layers delegate to the SDK.
* External consumers can import the SDK and execute all operations without accessing internal modules.

4.2 Object-Oriented Design (OOP) - No Code Duplication.
Code must be designed using an OOP approach. Code must not be duplicated. When the same logic appears in two or more files, it must be extracted to a shared module, a base class, or a mixin.
* Same function body in two or more files - extract to a shared module.
* Same try/except in three or more files - create a wrapper function.
* Identical method in three or more classes - create a base class or mixin.
* Copied logic with slight variations - use the Template Method pattern.
Mixin rules:
* A mixin provides only a single concern.
* Mixins do not override each other's methods.
* Mixins must be independently testable.

5 API Gatekeeper and Rate Limiting.
5.1 Central API Gatekeeper.
All external API calls must pass through a central gatekeeper. The gatekeeper handles rate limiting, queues, retries, and monitoring.
Gatekeeper requirements:
* No direct API calls that bypass the gatekeeper.
* Rate limits are enforced before every call.
* Overflow is pushed to a queue, not rejected.
* All API calls are logged for monitoring.

5.2 Rate Limit Configuration.
All rate limits must be read from a configuration file, never hardcoded in the code.

5.3 Queue Management for Overflow.
When rate limits reach their threshold, the gatekeeper must move requests to a queue instead of rejecting or crashing:
* FIFO queue for pending requests.
* Maximum queue depth defined in configuration.
* Backpressure alert when the queue is full.
* Drain mechanism that processes requests when rate windows reset.

6 Test-Driven Development and Quality Assurance.
6.1 RED, GREEN, REFACTOR TDD Process.
All development must follow Test-Driven Development:
* Every module must include a corresponding test file.
* Every public function/method must include at least one test.
* Tests cover both the happy path and error cases.
* Tests are written before or alongside implementation, not as an afterthought.
Test Rules:
1. Every new module must have a corresponding test file.
2. Every public function must have at least one test.
3. Both happy path and error case tests.
4. Use of fixtures in conftest for shared test data.
5. Mock for external dependencies (database, files, API).
6. Test files also comply with the 150-line rule.
7. No tests that depend on external services.

6.2 Minimum 85% Test Coverage.
Global test coverage must be 85% or higher. The test suite must fail if coverage drops below this threshold. Required coverage types include Statement coverage, Branch coverage, and Path coverage for critical paths.

6.3 Handling Edge Cases and Failures.
Identifying and documenting Edge Cases is a vital part of quality software development. Boundary conditions must be identified, each case documented with a detailed description, and screenshots of failures included when relevant. Error handling mechanisms must include defensive programming, clear error messages, detailed logging, and graceful degradation.

6.4 Expected Test Results.
Expected run results must be documented for each test, automated testing reports generated with pass/fail rates, and logs of successful and failed runs saved.

7 Code Review, Configuration Management, and Information Security.
7.1 Linter Compliance - Zero Ruff Violations.
Zero Ruff violations are permitted. All code must pass `ruff check` without errors.
Active rule categories include PEP 8 errors, Pyflakes, PEP 8 warnings, isort, pep-naming, pyupgrade, flake8-bugbear, flake8-comprehensions, and flake8-simplify.

7.2 Prohibition of Hardcoded Values.
All configurable values must come from configuration files, not from source code.
Table 1: Hardcoded Values vs. Configuration.
* API URLs: Incorrect - "https://api.example.com", Correct - cfg.get("api_url").
* Rate Limits: Incorrect - rate_limit = 10, Correct - cfg.get("rate_limit", 10).
* Timeouts: Incorrect - timeout = 60, Correct - cfg.get("timeout", 60).
* Secrets: Incorrect - api_key = "abc123", Correct - os.environ.get("API_KEY").
Values allowed in code: physical/mathematical constants, default parameter values, project constants in constants.py.

7.3 Configuration Architecture.
All configuration must follow a clear hierarchy with versioned configuration files.
* setup.json - Main app config (versioned).
* rate_limits.json - API rate limits (versioned).
* logging_config.json - Logging configuration.
* .env - Secrets (git-ignored).
* .env-example - Secret placeholders (committed).
* pyproject.toml - Build, lint, test settings.
* src/<package>/constants.py - Immutable project constants.

7.4 Information Security and Secrets Management.
There is no secret data in the project. When pushing to GitHub, an .env-example with dummy values must be created.
* It is forbidden to store API keys, passwords, or tokens in the source code.
* Use strictly environment variables: os.environ.get("API_KEY").
* .gitignore must include .env, *.key, *.pem, credentials.json.
* .env-example must exist with dummy values.
* In production environments, use a secrets management tool.
* Periodic key rotation, usage monitoring, and limiting permissions to the bare minimum.

8 Version Control and uv Package Manager.
8.1 Global Version Control.
Both code and configuration files must include explicit version tracking. The version starts at 1.00 and increments with significant changes.
The application should validate configuration version compatibility upon startup.

8.2 Git Best Practices.
Best practices include maintaining a clear commit history with meaningful messages, using separate branches for new feature development, conducting code reviews via Pull Requests, and using tagging to mark major versions.

8.3 Prompt Book.
Documenting the AI development process (Prompt Engineering Log) includes a list of all significant prompts used to build the project, a description of context and purpose, examples of generated outputs, iterative improvements, and best practices derived from the experience.

8.4 Mandatory uv Package Manager.
All projects must use `uv` as the package manager and task runner. It is forbidden to use `pip install`, `python -m`, or `virtualenv` directly.
Requirements:
* pyproject.toml is the single source of truth for dependencies (no requirements.txt).
* uv.lock exists and is under version control.
* No direct calls to pip or python in code, scripts, CI/CD, or documentation.
* All tools are run via `uv run`.

9 Research and Results Analysis.
9.1 Parameter Research.
Parameter Sensitivity Analysis is a systematic process of testing the impact of different parameters on system performance. The process includes conducting systematic experiments with controlled parameter changes, accurately documenting each parameter's effect, and using advanced analysis methods such as partial derivatives, variance-based analysis, or One-At-a-Time (OAT) approaches.

9.2 Results Analysis Notebook.
A Results Analysis Notebook is a central tool for presenting research. Depth of analysis is achieved using Jupyter Notebook or similar tools, performing methodical analysis of experimental results, comparing algorithms, configurations, or different approaches, and including mathematical proofs or theoretical analyses. LaTeX must be used for writing professional equations and formulas, and references to academic literature must be included.

9.3 Visual Presentation of Results.
High-quality data visualization is essential for conveying the research message. Types of visualizations include Bar charts for comparisons, Line charts for trends, Scatter plots for correlations, Heatmaps for parameter sensitivity, Box plots for distributions, and Waterfall charts for change analysis. Graph quality is measured by label clarity, use of consistent and accessible colors, detailed captions and a clear legend, and high resolution.

10 User Interface and User Experience.
10.1 Quality Criteria.
Usability criteria include: Learnability, Efficiency, Memorability, Error Prevention, and Satisfaction. Nielsen's 10 Heuristics: Visibility of system status, match between system and the real world, user control and freedom, consistency and standards, error prevention, recognition rather than recall, flexibility and efficiency of use, aesthetic and minimalist design, help users recognize, diagnose, and recover from errors, and help and documentation.

10.2 Interface Documentation.
Comprehensive documentation of the interface includes screenshots of every screen and state, a description of a typical user workflow, explanations of interactions and feedback, and accessibility considerations.

11 Costs and Pricing.
11.1 Cost Analysis.
A Cost Breakdown of API Tokens usage includes accurate counting of Input and Output Tokens, calculating the cost per million tokens, and estimating the total cost by model and service.
Optimization strategies include reducing token usage, batch processing, and selecting models based on cost-benefit ratios.

11.2 Budget Management.
Effective budget management includes cost forecasting for scale, real-time usage monitoring, and setting up budget overrun alerts.

12 Extensibility and Maintainability.
12.1 Extension Points.
A Plugins Architecture allows adding new functionality without modifying core code: clear interfaces for extension, lifecycle hooks (such as beforeCreate, afterUpdate), middleware mechanisms, and an API-first design.

12.2 Maintainability.
Maintainable code is characterized by modularity and separation of concerns, component reusability, analyzability, and testability.

13 International Quality Standards.
13.1 Product Quality Characteristics.
ISO/IEC 25010 defines a comprehensive software quality model covering eight main quality characteristics: Functional Suitability, Performance Efficiency, Compatibility, Usability, Reliability, Security, Maintainability, and Portability.

14 Organizing the Project as a Package.
14.1 Package Definition File.
Every package must include a pyproject.toml (preferred over setup.py) detailing name, version, description, author, license, and dependencies.

14.2 __init__.py Files.
__init__.py files must exist in the main directory and every subdirectory. It's recommended to use them to export public interfaces via __all__ and to define __version__.

14.3 Relative Paths.
All imports must use relative paths or package names, never absolute paths. Reading/writing files is also done relative to the package path.

14.4 Checklist: Package Organization.
1. Package definition file: Does pyproject.toml exist? Does it contain name, version, and dependencies? Are dependencies listed with versions?
2. __init__.py file: Does it exist in the main directory? Does it export public interfaces? Is __version__ defined?
3. Directory structure: Is source code in a dedicated folder? Are tests in /tests? Is documentation in /docs?
4. Relative paths: Are all imports relative? Are absolute paths avoided?

15 Parallel Processing and Performance.
15.1 Difference between Multiprocessing and Multithreading.
Multiprocessing is suitable for CPU-bound tasks (math calculations, image processing, model training). Each process runs in separate memory and utilizes a different CPU core.
Multithreading is suitable for I/O-bound tasks (network calls, database access, file I/O). Threads allow other operations during wait times.

15.2 Thread Safety.
Thread safety is critical: protecting shared variables using locks, queue.Queue for passing data, avoiding deadlocks, and using context managers.

15.3 Checklist: Parallel Processing.
1. Identify operations: identify I/O-bound/CPU-bound tasks, select the correct tool, evaluate benefit.
2. Implementation: dynamic number of processes/threads, safe data sharing, correct synchronization.
3. Resource management: proper shutdown, exception handling, preventing memory leaks.
4. Safety: protecting shared variables, preventing race conditions and deadlocks.

16 Modular Design and Building Blocks.
16.1 Building Block Structure.
Every building block is defined by:
* Input Data - data types, valid range, external dependencies, comprehensive validation.
* Output Data - data types, format, edge case behavior.
* Setup Data - parameters with defaults, configuration, initialization.

16.2 Design Principles.
* Single Responsibility - each building block is responsible for one task.
* Separation of Concerns - each block deals with one aspect.
* Reusability - building blocks are independent and not tied to specific code.
* Testability - every block can be tested using dependency injection.

17 Final Checklist.
Before submitting the project, a comprehensive checklist must be reviewed.
17.1 Mandatory Structure and Documentation.
* Comprehensive README.md in the project root serving as a user manual.
* docs/PRD.md, PLAN.md, TODO.md.
* Dedicated PRD documents for every core algorithm/mechanism.
* Architecture documentation with clear diagrams.
* Documented prompt book.
17.2 Architecture and Code.
* SDK architecture - all business logic through the SDK layer.
* OOP design - no code duplication, use of inheritance and mixins.
* API Gatekeeper - all external calls via Gatekeeper.
* Rate limits from configuration, queue management for overflow.
* Files up to 150 lines of code, comments, and docstrings.
* Code style consistency, descriptive names.
17.3 Testing and Quality.
* TDD - tests written before/alongside code.
* Test coverage 85% and above.
* Zero Ruff violations.
* Edge case documentation and error handling.
* Automated test reports.
17.4 Configuration and Security.
* Configuration files separate from code with versions.
* .env-example with dummy values.
* No API keys or secrets in code.
* Updated .gitignore.
* Use of uv as the sole package manager.
* pyproject.toml and uv.lock exist.
17.5 Research and Visualization.
* Systematic experiments with parameter changes.
* Documented sensitivity analysis, analysis notebook with graphs.
* High-quality graphs, screenshots, architecture diagrams.
* Token cost analysis and optimization strategies.
17.6 Extensibility and Standards.
* Documented extension points.
* Organization as a professional Python package.
* Parallel processing with thread safety.
* Building block-based design.
* Compliance with ISO/IEC 25010 standard.
* Tidy Git history, license, attribution, deployment instructions.

18 Additional Sources and Standards.
For preparing a project at a level of excellence, it is recommended to refer to international standards and sources: MIT's Software Quality Assurance Plan, ISO/IEC 25010 Software Quality Model, Google's Engineering Practices, Microsoft's API Guidelines, and Nielsen's Usability Heuristics.

19 Important Note.
This document presents a particularly high level of excellence. Not every clause is fully mandatory, but the more criteria are met, the higher the quality evaluation will be. Focus on depth, professionalism, and demonstrating high-level development capabilities.
It is recommended to use LLM tools and AI agents to assist in completing the project. It is clarified that as part of the evaluation, AI agents may be used to conduct the review.

20 Appendix: Detailed Guidelines for Professional Software Submission.
This appendix consolidates all the detailed guidelines for submitting a professional software project. The guidelines are organized systematically and cover all required aspects.
20.1 Project and Planning Documents - PRD components, Architecture document components.
20.2 Code Documentation and Project Structure - README components, Modular project structure, Code quality.
20.3 Configuration Management and Information Security - Configuration files, Information security.
20.4 Testing and Software Quality - Unit tests, Edge case handling.
20.5 Research and Analysis - Parameter research, Visualization.
20.6 User Interface - Usability criteria, Interface documentation.
20.7 Version and Cost Management - Version control, Cost analysis.
20.8 Extensibility and Standards - Plugin architecture, Compliance with standards.
20.9 Final Checklist - Summary of all points above.