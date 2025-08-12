---
description: Start test-driven development cycle for a feature
argument-hint: feature-description
---

# TDD Workflow Command

Starting Test-Driven Development cycle for: **$ARGUMENT**

I'll guide you through the complete TDD workflow using our specialized agents:

## 🎯 TDD Workflow Overview

**Red → Green → Refactor** cycle with specialized agent assistance:

1. **📋 Planning Phase**: Break down the feature into testable tasks
2. **🔴 Red Phase**: Write failing tests first
3. **🟢 Green Phase**: Implement minimal code to make tests pass
4. **🔄 Refactor Phase**: Improve code while maintaining test coverage
5. **✅ Review Phase**: Quality and security validation

---

## Phase 1: Planning 📋

First, I'll engage the **planner agent** to break down this feature into concrete, testable tasks.

> **Trigger**: "Plan implementation for: $ARGUMENT"

*The planner will analyze the feature and create a structured implementation plan with clear acceptance criteria.*

---

## Phase 2: Test-First Development 🔴

For each planned task, we'll follow strict TDD:

### Red Phase (Failing Tests)
> **Trigger**: "Write failing tests for [current task]"

*The tester agent will create comprehensive tests that define the expected behavior.*

### Green Phase (Minimal Implementation)
Once tests are written and failing, I'll implement the minimal code needed to make them pass.

### Refactor Phase (if needed)
After tests pass, we'll clean up the implementation while maintaining test coverage.

---

## Phase 3: Quality Review ✅

Before completing the feature:

> **Trigger**: "Review the implemented code"

*The reviewer agent will check for:*
- Correctness and logic issues
- Security vulnerabilities  
- Performance considerations
- Code maintainability
- Style consistency

---

## Ready to Begin?

Let me start by creating an implementation plan for your feature. This will help us approach the development systematically and ensure we don't miss any important aspects.

**Next**: Engaging planner agent to break down "$ARGUMENT" into testable tasks...