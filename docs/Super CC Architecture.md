# CC Multi-agent Architecture Plan

# Designing a Claude Code Multi‑Agent Development Workflow

## Introduction

This document outlines a design for a **Claude Code-powered AI workflow system** that turns any code repository into a high-productivity, multi-agent coding environment. The goal is to leverage **Anthropic Claude Code's native capabilities** – such as custom slash commands, subagent configuration, tool permission scoping, and event hooks – to orchestrate a team of specialized AI "agents" that assist in all stages of software development. Crucially, we will **not rebuild functionalities that Claude Code already provides** natively. Instead, we'll configure and compose those features to create a robust workflow.

By using Claude Code's features as building blocks, we ensure the solution is lean and maintainable. Subagents (custom AI personas) allow task-specific expertise without polluting the main session context. Slash commands let us encapsulate common prompts or workflows for reuse. Fine-grained tool permissions restrict what each agent can do for safety and focus. And hooks enable deterministic automation (for logging, formatting, and guardrails) that runs *alongside* Claude's AI reasoning. Using these mechanisms, we'll design a multi-agent workflow that supports test-driven development (TDD), automated planning, debugging assistance, code refactoring, and multi-pass code reviews – all while preserving context and ensuring traceability of AI actions.

## Leveraging Claude Code's Native Capabilities

To avoid over-engineering, our system leans heavily on built-in Claude Code features rather than custom code. Key capabilities we will use include:

- **Custom Subagents:** Claude Code supports defining specialized AI subagents as Markdown files (with YAML front-matter) in the project's `.claude/agents/` directory. Each subagent has its own system prompt, a descriptive trigger condition, and a restricted set of tools it's allowed to use. These subagents run in isolated context windows, preventing the main conversation from getting sidetracked while the subagent works. We will create core subagents (for planning, testing, etc.) with clear roles so Claude can delegate tasks to them appropriately.
- **Slash Commands:** We will use project-specific slash commands (Markdown files under `.claude/commands/`) to encapsulate frequent operations. Slash commands let us trigger complex multi-step prompts easily (e.g. `/context-synth` to summarize code context). They can include parameterized prompts and even embed outputs of allowed bash commands into the context. This saves time and ensures consistency in how we instruct Claude to perform recurring tasks.
- **Tool Permissions:** Claude Code allows scoping the AI's tool usage both globally and per subagent. We will take advantage of this to enforce safety (e.g. preventing certain agents from running shell commands) and to focus agents on relevant tools only. For example, a "code-reviewer" agent might be allowed to read files and run `git diff`, but not allowed to deploy or modify files itself. Using the `allowed-tools` list in command or agent definitions, or via `/permissions` settings, we can constrain each agent's capabilities.
- **Hooks:** Hooks are shell scripts or commands configured to run automatically on certain events in the Claude Code lifecycle (before/after tool use, on notifications, at the end of responses, etc.). They give deterministic control alongside the AI's actions. We will use hooks to implement **file protection**, **auto-formatting**, **audit logging**, and **notifications** without relying on the AI to remember these policies. For example, a PreToolUse hook can block unwanted file edits (enforcing a do-not-touch list), and a PostToolUse hook can auto-run linters or formatters after the AI edits code. Hooks ensure these critical steps *always* happen as required, rather than hoping the AI follows instructions.

By leaning on these native features, our design stays concise and robust. Anthropic's best-practice guide for Claude Code emphasizes using first-class configuration (subagents, hooks, etc.) for consistent behavior rather than relying on prompt heuristics. In the next sections, we define the core subagents and workflow, then detail how hooks and scripts tie everything together.

## Core AI Subagents and Their Roles

We will set up a suite of core subagents to tackle different aspects of development. Each subagent is a specialized AI assistant with a clear purpose and limited tools. Below are the primary subagents in this workflow and how they operate:

### 1. Context Synthesizer

**Purpose:** Summarize the repository's content (code and docs) into a concise JSON "context digest" for use in prompts. This agent compresses the project's knowledge into <500 tokens so that complex projects can be handled in a few-shot manner across sessions. By providing Claude with a brief but information-rich summary of the codebase, we avoid feeding in megabytes of code context and instead supply only the *relevant* details each time. This enables Claude to quickly get up to speed on the project state at the start of any session or task.

**Implementation:** We implement a custom slash command `/context-synth` that accepts file glob patterns (e.g. `src/**/*.py docs/ARCHITECTURE.md`) and produces a JSON summary of those files. The command's Markdown definition in `.claude/commands/context-synth.md` might look like:

```markdown
---
description: Summarize given files into a 300-token JSON brief
argument-hint: file-glob(s)
allowed-tools: Read, Glob   # allow reading files and globbing paths
---

ROLE: Context Synthesizer
GOAL: Preserve semantic signal, drop syntactic noise.

1. Read everything in $ARGUMENTS.
2. Ignore license headers/comments when tight on space.
3. Output **strict JSON** with structure:

   {
     "files": [ { "path": "...", "main_roles": ["..."], "apis": ["..."], "todos": ["..."] } ],
     "cross_cutting": ["..."],
     "open_questions": ["..."]
   }

Hard limit: 300 tokens.

```

This command instructs Claude to gather the content of all files matching the user-specified globs (Claude will use the **Read** and **Glob** tools to do this automatically), then produce a structured summary. The JSON includes a per-file summary of main roles (key classes/functions), any API usage, and TODO comments, plus any cross-cutting concerns and open questions discovered. By design, the output is capped at ~300 tokens and excludes boilerplate like license text to maximize useful information.

**Context-Synthesizer Subagent with Git-based Incremental Processing:** For very large codebases, the above command might strain Claude's context window. Therefore, we also define a dedicated subagent (e.g. `.claude/agents/context-synth-agent.md`) whose sole job is to perform large-scale context synthesis with incremental processing. This **Context Synthesizer agent** has its own isolated context and can be invoked when needed (using Claude's `Task` tool) to summarize many files efficiently. The agent's system prompt includes a defined algorithm for efficient operation:

- **Tools:** Allowed to use `Read` and `Glob` only (no Bash needed for the new approach)
- **Algorithm:** When tasked, the agent will:
    1. Check `.claude/context/last-build-commit` to get the commit hash when context was last built
    2. Use `git diff --name-only [last-commit] HEAD` to identify changed files since last summary
    3. Load existing summaries from `.claude/context/summaries/` for unchanged files
    4. For each new or modified file, read its content and generate a 300-token JSON summary (following the same schema as the `/context-synth` command)
    5. Save individual file summaries to `.claude/context/summaries/[file-hash].json`
    6. Merge all summaries into a final combined JSON object
    7. Update `.claude/context/last-build-commit` with current HEAD commit

This Git-based approach means that if you run the context synthesizer repeatedly, it will skip unchanged files and reuse their previous summaries (to save time and tokens). Small changes to a single file won't bust the entire context - only that specific file needs re-summarization. We leverage Git's built-in change tracking instead of maintaining our own hashing system, eliminating the need for `cache_hash.py` and the `.cache/` directory entirely.

Overall, the Context Synthesizer ensures that at the start of each development session or task, Claude has a fresh, high-level understanding of the codebase. This enables a form of *few-shot learning* for complex projects: we feed Claude a small JSON brief that contains the most salient project information, instead of prompting from scratch or relying on lengthy conversation history. As a result, *every future Claude session can be kept lean by piping in a <300-token digest instead of megabytes of code*.

### 2. Architect

**Purpose:** Review architectural implications of proposed changes and make high-level system design decisions before implementation begins. The Architect subagent ensures that new features align with existing architecture and identifies potential technical debt or design pattern violations before they're coded.

**Implementation:** The **Architect subagent** (e.g. `.claude/agents/architect.md`) would be configured with read-only access to understand the system deeply but not modify it during analysis. Its system prompt might instruct: *"You are a senior software architect. Given proposed changes or features, analyze their architectural impact, suggest appropriate design patterns, identify potential issues with system coherence, and recommend architectural improvements. Consider scalability, maintainability, and consistency with existing patterns."*

**Tools:** `Read`, `Grep` only - no write permissions

**Workflow Integration:** The Architect agent is engaged:
- Before the Planner agent for major features (to ensure the plan aligns with architecture)
- When modifying core system components
- When the developer explicitly requests architectural review

A typical usage would be:
1. Developer describes a new feature or major change
2. Architect agent analyzes the existing system architecture
3. Provides recommendations on design patterns, potential refactoring needs, and architectural considerations
4. These insights feed into the Planner's implementation strategy

This front-loads architectural thinking and prevents technical debt from accumulating through ad-hoc implementations.

### 3. Planner

**Purpose:** Convert high-level feature requests or bug reports into a concrete implementation plan. The Planner subagent decomposes a brief (e.g. a user story or feature description) into phases, tasks, and acceptance criteria. This helps structure the development process before coding begins.

**Implementation:** We can leverage Claude's capabilities or built-in agents for strategic planning. Anthropic Claude Code includes a "strategic-planning-agent" in some contexts, which might be utilized if available. Otherwise, we create a custom `planner` subagent.

The **Planner subagent** (e.g. `.claude/agents/planner.md`) would be configured with access to reading relevant docs (to understand context) but typically no code-modifying tools. Its system prompt might instruct: *"You are a planning assistant. Given a project brief (in JSON or text form), break it down into a step-by-step implementation roadmap. Outline phases or milestones, and for each, list specific tasks with bullet-point acceptance criteria."* The planner may reference architecture docs or the context summary to inform the plan.

A typical usage would be:

1. First, run the `/context-synth` command on any requirement documents or specification files to produce a JSON brief of the feature request (and possibly the current architecture).
2. If it's a major feature, engage the Architect agent first for design guidance.
3. Then, prompt Claude: *"Use the planner subagent to craft an implementation plan for the given brief."* Claude will delegate to the planner agent, which returns a structured plan (for example, a list of phases with tasks).
4. Review the plan with a human eye – adjusting any unrealistic parts (removing "fantasy" tasks Claude suggested that don't make sense) – and then proceed to execute the tasks.

The plan provides a clear breakdown so that we (and Claude) can tackle one task at a time in a focused manner. By front-loading this step, we ensure the overall development stays on track and the AI has a reference for what needs to be done, reducing the chance of meandering. (Note: because planning is largely a reasoning task, we rely on Claude's intelligence here; no complicated custom code needed, just a well-written system prompt or using Anthropic's own planning agent.)

### 4. Tester

**Purpose:** Enforce a **unit-test-first workflow** by generating tests *before* implementation and validating functionality via test runs. The Tester agent helps implement **TDD (Test-Driven Development)**: every new feature or bug fix starts with writing failing tests, which define the expected behavior, and only then writing code to make those tests pass.

**Implementation:** The testing workflow can be achieved with a combination of direct Claude prompts and a specialized subagent. One approach is to have a **Tester subagent** dedicated to writing test cases and possibly executing them. The Tester agent (e.g. `.claude/agents/tester.md`) would be configured with:

**Enhanced Tool Permissions:**
- `Write` - but only to `tests/` directory (enforced via path restrictions)
- `Read` - everywhere (to understand the code being tested)
- `Bash` - but only test runner commands (e.g., `pytest`, `npm test`, `go test`)

Its instructions would cover best practices in test writing (cover edge cases, use clear assertions, prefer small, independent tests, etc.) and to report results.

In practice, the workflow for each task is:

1. **Start with tests:** Begin a fresh Claude session (or clear prior context) for the task, and instruct Claude that we will do test-first development. For example, the user might say: *"We're working on Task 123 (implement feature X). First, write the necessary failing unit tests for this feature, then proceed to implementation until the tests pass."* This primes Claude (and any agents) to follow the TDD cycle. A UserPromptSubmit hook could even be used here to automatically prepend a reminder or check that tests exist before code is written (enforcing policy that no production code is added without tests).
2. **Generate test cases:** Claude will likely invoke the Tester subagent to generate the appropriate test code. The tester writes test functions or scenarios covering the new functionality. These tests are saved to the repository (Claude uses the `Write` tool to create or modify test files in the `tests/` directory only).
3. **Run tests (expected to fail):** Next, the tests are executed. Claude can call a shell command to run the test suite (e.g., `pytest` or `npm test` depending on the stack). The first run should fail, as the feature isn't implemented yet. The failure output provides valuable information.
4. **Implement code to pass tests:** Now Claude (the main agent or a coding subagent) writes the minimal code needed to make the tests pass. This could involve creating new source files or editing existing ones (using Claude's editing tools). Claude iteratively writes code and runs tests until all test assertions pass.
5. **Confirm test pass and commit:** Once the tests go green (pass), Claude can finalize the changes. Ideally, it should also update documentation or notes if needed and then run a Git commit (this could be automated or left for the user) to record the changes along with the tests. The commit message can note that tests are passing for the implemented feature.

Throughout this loop, the Tester agent might be re-engaged if new edge cases arise or if additional tests are needed (for example, if a bug is found during implementation, we add a test for it first, then fix). This strict **red-green-refactor** cycle ensures high confidence in the code. It also has the effect of "locking in" the intended behavior early with tests, which prevents later agents or edits from unintentionally breaking functionality – any regression will show up as a test failure immediately.

*Example:* Suppose our task is to implement a new API endpoint. We prompt the tester agent to write tests for all expected outcomes (success, error conditions). Claude, via the Tester agent, writes these tests in a file `test_new_api.py`. We run them – they fail because `new_api()` is not yet implemented. Claude then writes the `new_api()` function until `pytest` reports all tests passed. Only then do we consider the implementation done. This pattern, repeated for each task, keeps development rigorously test-driven.

### 5. Debugger

**Purpose:** Assist in diagnosing failing tests, runtime errors, or general bugs by analyzing error output and proposing targeted fixes. The Debugger agent kicks in when something goes wrong – for example, a test fails unexpectedly or an exception is thrown – to figure out why and how to resolve it.

**Implementation:** The **Debugger subagent** (`.claude/agents/debugger.md`) would be configured with:

**Enhanced Tool Permissions:**
- `Read` - all files (to analyze code and understand context)
- `Grep` - for searching patterns and known issues
- `Bash` - restricted to test/debug commands only (no write operations)

Its system prompt might encourage it to be an expert at reading stack traces, log files, and code, then pinpointing the likely cause of a failure. This agent does not automatically fix the code (to avoid it taking reckless actions); instead, it outputs a diagnosis and a proposed solution for the developer or main agent to implement.

In a typical flow:

- A test fails or an error occurs during code execution. Claude (main) or the user can explicitly invoke the debugger agent: e.g. *"Use the debugger subagent to analyze why the test X is failing."*
- The Debugger agent might use the **Read** tool on relevant files (the test file, the code under test, maybe logs) and use **Grep** to search for known issues or patterns. If allowed, it might rerun the failing command with more verbose output.
- The agent then produces an analysis, e.g.: *"Test `test_edge_case` failed because the function did not handle the empty input case, leading to a `TypeError` on line 45. The logic assumes a non-empty list. To fix this, we should add a check for empty input and return an appropriate response."* It might even suggest a code diff or specific changes.
- At this point, either the main Claude agent or the developer applies the fix (using the standard coding workflow). The tests are run again to verify the solution.

We explicitly avoid giving the Debugger agent permission to use `Edit` or `Write` tools on code, keeping it focused on diagnosis rather than implementation. This keeps a human or the main agent in the loop to validate the fix.

In practice, the Debugger agent speeds up the *find-and-fix* loop. Instead of the developer manually reading logs or guessing at the cause, the AI can quickly highlight the relevant portion of a stack trace and recall similar issues or known bug patterns. It's another example of specialization: the debugger is tuned to a different mode of reasoning (critical, detail-oriented troubleshooting) than the planner or coder, improving the overall productivity.

*(Note: We could integrate the debugger more tightly by using hooks to automatically invoke it on test failures. For instance, a PostToolUse hook after a test run could detect a non-zero exit status and then call the debugger agent. However, such automation should be used carefully to avoid infinite loops. For now, we assume the developer or Claude will call the debugger agent explicitly when needed.)*

### 6. Cleaner (Refactorer)

**Purpose:** Refactor and clean up code once it's working, to improve readability, maintainability, and adherence to style conventions. The Cleaner agent can also handle code formatting and simple optimizations. This agent essentially performs the "refactor" step in the TDD mantra "red -> green -> refactor," ensuring the codebase stays clean after iterative additions.

**Implementation:** The **Cleaner subagent** (we could name it `refactorer` in `.claude/agents/cleaner.md`) focuses on code improvements without changing functionality. We will configure it with:

**Enhanced Tool Permissions:**
- `Edit` only - no `Write` permission (prevents creating new files/scope creep)
- `Read` - to understand existing code
- `Grep` - to find code smells or style violations
- `Bash` - restricted to test runners only (to verify refactoring doesn't break tests)

Its system prompt might say: *"You are a code janitor and refactoring expert. After functionality is confirmed, your job is to simplify and improve the code: remove duplication, clarify names, add comments if needed, and ensure the code meets our style guidelines (without altering behavior)."*

When invoked (either manually by the user or possibly automatically after tests pass), the Cleaner agent could:

- Search the code for common issues (unused variables, overly complex functions, inconsistent naming).
- Make small, safe changes. For example, it might split a long function into smaller ones, rename a confusing variable, or reformat a section for clarity. Because Claude Code's Edit tool can suggest diffs for file modifications, the agent can propose a diff that the developer can review before applying.
- Run an auto-formatter if not already done by hooks (though our setup will likely already handle basic formatting on save via hooks, as described later).
- Ensure any refactoring doesn't break tests: it should run the tests again (the agent or main Claude can do this) to confirm everything still passes after refactoring. Only then are the changes kept.

A benefit of a dedicated refactoring agent is that it can have a different persona: more cautious, focusing on structure and style rather than rushing to implement features. It can also be prompted with guidelines specific to refactoring. For instance, we might include in its instructions a reminder of the project's style rules or a mandate to always keep changes minimal and reversible (so that if the refactor accidentally introduces a bug, it's easy to undo).

In summary, the Cleaner agent helps maintain code quality continuously, rather than letting tech debt accumulate. After each feature, running the cleaner ensures that the new code integrates nicely with the codebase and is easy for humans to understand.

### 7. Code Reviewer (Code Auditor)

**Purpose:** Provide multi-pass **code quality gates** – including static analysis, security review, style compliance, and an AI-driven code review – before changes are finalized. The Code Reviewer (or Code Auditor) agent acts as an AI "pair reviewer" that catches issues the tests might not, ensuring robustness and best practices.

**Implementation:** Our code review pipeline consists of multiple layers, both automated tools and the AI agent. We consolidate these into a single orchestrated command for simplicity:

**Consolidated Review Command:** A single `/review` command that orchestrates all checks by default, with optional flags for specific reviews:
- `/review` - runs all checks in sequence
- `/review --static-only` - just static analysis
- `/review --security-only` - just security audit
- `/review --style-only` - just style linting
- `/review --ai-only` - just AI code review

The `.claude/commands/review.md` file would contain:
```markdown
---
description: Orchestrate comprehensive code review
argument-hint: [--static-only|--security-only|--style-only|--ai-only]
allowed-tools: Bash(git diff:*), Bash(ruff:*), Bash(mypy:*), Bash(bandit:*), Bash(prettier:*), Task
---

Run comprehensive code review based on arguments:
1. Parse $ARGUMENTS for specific review type or default to all
2. Execute reviews in sequence:
   - Static: ruff, mypy (for Python) or equivalent
   - Security: bandit or security scanner
   - Style: prettier/black auto-formatting
   - AI: Invoke code-reviewer subagent
3. Compile results and provide summary
```

The **Code Reviewer subagent** (e.g. `.claude/agents/code-reviewer.md`) is an AI agent that performs a deeper semantic review. We configure it with:

**Tool Permissions:**
- `Read` - source code and diffs
- `Bash` - restricted to `git diff` and other read-only queries
- No write/edit permissions

Its prompt will instruct it to act like a meticulous senior engineer reviewing a pull request. For instance:

- It could first list the files changed in the last commit (`git diff --name-only`) to understand the scope.
- Then systematically go through each file's diff, prioritizing any critical bugs or security issues, then style improvements, etc. It should flag things like improper error handling, potential performance bottlenecks, or deviations from project conventions.
- The agent should provide feedback in a structured way, possibly even suggesting concrete code changes (in diff format) to address the issues it finds. We instruct it to keep suggestions minimal and focused, to avoid overwhelming the developer with nitpicks. For example: *"Function X might crash on null input – consider adding a check. Here's a diff to do so..."*.

Claude can automatically invoke this code-reviewer agent after code edits, or the user can explicitly request it. A typical usage might be: *"Use the code-reviewer subagent to audit my recent changes."* Claude would then produce a summary of issues or confirm that everything looks good.

Finally, a human team member can do a quick pass and then approve the changes. The result is a layered defense: even if Claude's own outputs have mistakes, the subsequent review steps (both automated and AI) catch them before they make it into production. In practice, this **multi-pass review pipeline** can catch subtle bugs or security vulnerabilities that basic testing might miss, and it helps enforce consistent code quality standards with minimal human effort.

### 8. Integration Tester (Optional)

**Purpose:** Focus on integration and end-to-end tests after unit tests pass, ensuring system-wide functionality beyond unit tests.

**Implementation:** The **Integration Tester subagent** (`.claude/agents/integration-tester.md`) is explicitly kept out of standard workflow chains and only invoked when:
- The user explicitly requests it
- The main agent detects integration points have changed and suggests its use

**Tool Permissions:**
- `Write` - restricted to `tests/integration/` directory only
- `Read` - all files
- `Bash` - test runner commands

**Workflow Integration:** After completing features that touch multiple components, the main Claude agent might prompt: *"I've completed the API integration and all unit tests are passing. Would you like to run end-to-end integration tests to verify the full flow? (Use: 'Run integration-tester agent')"*

This keeps full E2E testing optional but discoverable, recognizing that integration tests are less frequent than unit tests but valuable for system-wide validation.

### Additional Agents (Extensibility)

The subagents described above are the core set for most projects. However, the architecture is extensible – new agents can be added as needed without altering the others, thanks to Claude Code's flexible routing by description. A few examples of additional subagents that could be useful:

- **Documentation Writer:** An agent that generates or updates documentation (like README, API docs, or inline docstrings) after features are implemented. It could be prompted to summarize how new code works and ensure usage examples are up to date.
- **Performance Optimizer:** An agent that profiles the code or analyzes performance hotspots and suggests optimizations. For instance, after a feature is complete, you might run a profiler and feed results to a "performance-tuning" subagent that recommends improvements (e.g. refactoring a slow loop, adding caching for expensive computations).
- **"Verifier" Agent:** A specialized agent (like the community-inspired "Karen" agent) whose role is to double-check that tasks marked as done are truly completed and meet the requirements. It could systematically validate that implemented features match the acceptance criteria from the Planner's plan and that nothing was glossed over. If it finds a discrepancy (e.g. a feature is claimed complete but tests or usage show otherwise), it flags it for further work.

Since subagents are just Markdown configs, one can iteratively introduce new ones to cover emerging needs. The guiding principle is to keep each subagent **single-purpose and well-scoped**, with a clear trigger described in its YAML `description`. Claude will automatically choose to delegate to a subagent when the task matches its description, or users can explicitly invoke them. This modular approach means our workflow can grow in capability without entangling the subagents' behaviors.

## Workflow: Orchestrating the Agents in Practice

With the core agents in place, we now describe how they work together in a typical development workflow. To make agent orchestration explicit and reproducible, we define workflow configurations that specify standard agent chains.

### Workflow Configuration

We create a `.claude/workflows/` directory containing YAML files that define standard agent chains. This makes the sequencing explicit and allows for both automated and parallel execution where appropriate.

**Example workflow configuration (`.claude/workflows/feature-development.yaml`):**
```yaml
name: feature-development
description: Standard TDD workflow for feature implementation
parallel_groups:  # Groups that can run in parallel
  review_checks:
    - static-analyzer
    - security-scanner
    - style-checker
steps:
  - agent: context-synthesizer
    params: "src/**/*.py docs/*.md"
    description: "Build project context"
  
  - agent: architect
    condition: "major_feature"
    description: "Review architectural implications"
  
  - agent: planner
    description: "Create implementation plan"
  
  - name: "TDD Loop"
    repeat_until: "tests_pass"
    substeps:
      - agent: tester
        description: "Write failing tests"
      
      - agent: main
        action: implement
        description: "Implement until tests pass"
      
      - agent: debugger
        condition: "on_test_failure"
        description: "Diagnose test failures"
  
  - agent: cleaner
    condition: "on_tests_pass"
    description: "Refactor code"
  
  - parallel_group: review_checks
    description: "Run all review checks in parallel"
  
  - agent: code-reviewer
    description: "AI code review"
```

### Standard Development Flow

**A. Context Setup (Context Synthesizer):** At the start of a new Claude session or when picking up a new feature/bug, compress the current project state into a short prompt. Run the `/context-synth` command on the most relevant parts of the code (and docs) for the task at hand. This returns a JSON digest which can be given to Claude as a reference. For example, you might do:

```bash
claude /context-synth src/utils/**/*.py docs/ARCHITECTURE.md
```

Claude will output a summary JSON. You then say: *"Here is an overview of the current project context:"* and paste that JSON into the conversation (or, since you ran it via CLI, it may already be present). This ensures Claude (and its subagents) have up-to-date context. This step is especially important if you've switched tasks or come back after a break – it essentially "primes" the AI with all it needs to know.

**B. Architecture Review (Architect - for major features):** For significant changes, engage the Architect agent before planning: *"Review the architectural implications of adding feature X."* The architect analyzes the system and provides design recommendations that inform the implementation plan.

**C. Planning (Planner):** Use the Planner agent to break down the feature. Provide the feature brief (possibly as JSON from context-synth if it's a spec document) and any architectural guidance to the planner: *"Plan the implementation steps for this feature."* Receive the plan, discuss or refine it as needed, and identify the first task to implement.

**D. Task Implementation Loop (TDD with Tester & Debugger):** For each task (e.g. "Add function X to do Y"), follow a cycle:

1. *Write Tests First:* Prompt Claude/Tester to generate tests for the task. Ensure these tests reflect the acceptance criteria. Save them to the repository (the AI will use the Write tool, restricted to `tests/` directory). Possibly run `/context-synth` again including the new test files and the specific module under development to keep context focused.

2. *Run Tests (fail):* Execute the tests (Claude uses Bash: e.g. `!pytest -q`). Observe the failures. This provides confirmation that the tests are exercising the intended functionality (and of course they fail initially).

3. *Implement Code:* Now Claude writes the minimum code to make the tests pass. It may not need a special subagent here – the main Claude agent can handle implementation using the context and tools (file edit/write). If the task is complex, Claude might call the Planner agent again for a mini-plan of how to implement, or call a specialized coding subagent if one exists. Generally, it will iteratively code and run tests.
    - If a test fails partway through, and the reason isn't obvious, Claude or the user can call the Debugger agent to analyze the failure. The debugger suggests a fix, which is then applied.
    - Continue this code->run tests->debug loop until all tests pass green.

4. *Refactor (Cleaner):* Once tests pass, optionally invoke the Cleaner agent to polish the code. For instance, *"Use the cleaner agent to refactor the new function for clarity."* The cleaner might propose some small changes or simply confirm that no refactoring is needed. Rerun tests to ensure nothing broke.

5. *Review (Consolidated Review Command):* Before considering the task done, run the comprehensive review:
    - Use the consolidated `/review` command to run all checks (or `/review --static-only` for just static analysis, etc.)
    - The command orchestrates static analysis, security scanning, style checking, and AI review in sequence (or in parallel where configured)
    - Address any issues found by making further edits (possibly engaging the Cleaner again for fixes if they are non-trivial)
    - After everything is clean, you (the developer) do a final skim and then commit the changes. E.g., `git commit -am "Implement feature X (tests passing, reviewed)"`

6. *Integration Testing (Optional):* If the feature touches multiple components, the main agent might suggest: *"This feature involves multiple system components. Would you like to run integration tests? (Use 'Run integration-tester agent')"* This keeps E2E testing available but not mandatory.

7. *Log & Move on:* The commit is logged with agent attribution (see Audit Trail section), and we have a record that the task was completed by AI assistance at a given commit hash. Now pick the next task in the plan and repeat.

Throughout this loop, **Claude's main agent orchestrates calls to subagents as needed**, or the developer can explicitly instruct when to use a particular agent or command. Claude Code's internal routing will often automatically delegate. For example, if you simply say, *"Please review the code for any potential issues,"* Claude might decide to utilize the code-reviewer subagent behind the scenes (because the description matches a review task). Each subagent uses its own context window, so the tester can focus on testing, the debugger on debugging, etc., without the solution chatter polluting the main conversation.

### Parallel Execution Configuration

For efficiency, certain independent checks can run in parallel. The workflow configuration supports this via `parallel_groups`:

```yaml
parallel_groups:
  review_checks:  # These can run simultaneously
    - static-analyzer
    - security-scanner
    - style-checker
  test_suite:  # If tests are independent
    - unit-tests
    - integration-tests
```

When Claude encounters a parallel group in the workflow, it can execute these agents simultaneously (if the Claude Code runtime supports it) or at least recognize they're independent and could be run in any order.

It's important to note that after each major step, we **preserve the context**. The `/context-synth` can be run again to update the project summary (especially after significant code changes or at the end of a task) and that summary can be stored (for example, appended to an `ARCHITECTURE_BRIEF.md` log). We also regularly use Claude's `/compact` command to compress the conversational history while keeping important details, so the chat remains within token limits. In effect, we maintain a tight feedback loop: tests and code drive each other, and the context summary plus compacting ensures Claude never loses the thread even across multiple sessions.

By adhering to this TDD-centric, multi-agent workflow with explicit orchestration via workflow files, we can *few-shot* our way through complex projects. Each new session or agent call has the distilled wisdom of prior work (via test cases, context summaries, and logs) without needing to reload entire code files or lengthy chats. This significantly boosts productivity and keeps the AI's output focused and relevant.