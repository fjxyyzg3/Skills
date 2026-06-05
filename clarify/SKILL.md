---
name: clarify
description: Clarify ambiguous codebase questions, inspect source code instead of asking when details are discoverable, and produce source-grounded explanations with file locations, code walkthroughs, Mermaid architecture and flow diagrams, plus optional HTML documentation. Use when the user asks how code works, where behavior lives, what calls what, how a feature flows, or requests detailed code analysis, diagrams, reports, or generated documentation.
---

# Clarify

Turn a codebase question into a source-grounded explanation. Clarify only what cannot be discovered, inspect the relevant source deeply enough to avoid guessing, and answer with code locations, code explanations, diagrams, and a document when useful.

## Core Rules

- Ask at most one clarification question at a time, and include your recommended default answer.
- If a detail can be discovered from code, docs, config, examples, tests, history, or generated artifacts, inspect those sources instead of asking.
- Mark inferences as inferences. Do not present guesses as source facts.
- Prefer precise file and line references over vague module names.

## Workflow

1. Define the target question.
   - Restate the user's question as the concrete behavior, subsystem, or flow to explain.
   - Identify the answer shape needed: source locations, main symbols, call/data flow, diagrams, and documentation output if requested.
   - If the requested scope is ambiguous and code exploration cannot resolve it, ask one question and recommend a default path.

2. Explore the codebase.
   - Inspect project documentation that explains architecture, domain language, setup, or feature behavior when it helps answer the question.
   - Use the available source navigation tools for the environment: symbol search, text search, caller/callee lookup, dependency graphs, tests, logs, and focused file reads.
   - Start from user-provided names, error text, feature terms, API names, classes, functions, config keys, routes, commands, tests, and docs.
   - Follow the path through callers, callees, registration points, config, tests, generated code, and adjacent implementations until the explanation has enough evidence.
   - Keep an evidence map with `file:line`, symbol, role in the flow, and confidence.

3. Synthesize the answer.
   - Answer the question first, then show the supporting code path.
   - Explain each important class/function/module in plain language and why it matters.
   - Include key code references with clickable paths when the environment supports them.
   - Explain control flow and data flow separately when both matter.
   - Call out unresolved ambiguity, version-dependent behavior, missing tests, or places that require runtime verification.

4. Draw diagrams.
   - Include Mermaid diagrams for non-trivial architecture or flow questions.
   - Use `flowchart`, `sequenceDiagram`, or `classDiagram` based on the question.
   - Keep node labels short, quote labels that contain punctuation, and avoid diagrams so dense that they replace explanation.
   - Use architecture diagrams for ownership/module relationships and flow diagrams for execution paths.

5. Generate documentation when requested or when the answer is substantial.
   - Read `references/report-structure.md` before creating an HTML document.
   - Use `assets/clarify-report-template.html` as the starting point when writing a standalone report.
   - Save the report in a user-specified path when provided; otherwise choose a clear, local path based on the topic and project layout.
   - Check the generated HTML enough to avoid broken markup. If visual Mermaid rendering cannot be checked, say so explicitly.

## Output Shape

For concise answers:

- Direct answer
- Code locations
- Walkthrough
- Mermaid diagram when useful
- Remaining questions or risks

For document-generation answers:

- State the generated file path
- Summarize the key conclusion
- Summarize the evidence inspected
- Mention unresolved ambiguity when it remains
