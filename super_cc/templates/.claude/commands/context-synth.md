---
description: Synthesize files into concise 300-token JSON context digest
argument-hint: file-glob-pattern(s)
tools: [read, glob]
---

# Context Synthesizer

**ROLE:** Context Synthesizer  
**GOAL:** Preserve semantic signal, drop syntactic noise.

## Task: Create Context Digest

Reading files matching pattern: `${ARGUMENT:-"src/** docs/** *.md"}`

### Step 1: Analyze File Structure
First, I'll identify all matching files and their types to understand the scope.

### Step 2: Extract Core Information
For each file, I'll identify:
- **Main roles**: Key classes, functions, modules, components
- **APIs**: External interfaces, public methods, endpoints
- **TODOs**: Outstanding tasks, known issues, future work

### Step 3: Identify Cross-Cutting Concerns
- Design patterns used across files
- Shared dependencies and utilities
- Architecture patterns and conventions

### Step 4: Generate JSON Summary

Output format (strict JSON, ~300 tokens):
```json
{
  "files": [
    {
      "path": "example/file.py",
      "main_roles": ["UserService", "auth middleware"],
      "apis": ["POST /login", "GET /user/{id}"],
      "todos": ["Add rate limiting", "Improve error handling"]
    }
  ],
  "cross_cutting": [
    "Express.js REST API pattern",
    "JWT authentication",
    "MongoDB persistence layer"
  ],
  "open_questions": [
    "Database migration strategy unclear",
    "Error handling inconsistent across services"
  ]
}
```

### Optimization Rules:
1. **Prioritize**: Focus on interfaces and public APIs over internal implementation
2. **Compress**: Skip license headers, imports, boilerplate when space is tight
3. **Abstract**: Describe patterns rather than listing every function
4. **Filter**: Include only actionable TODOs and meaningful questions

---

*Processing files now...*