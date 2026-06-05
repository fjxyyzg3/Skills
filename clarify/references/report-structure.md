# Clarify Report Structure

Use this reference when generating a standalone HTML report for a codebase explanation.

## Required Sections

1. Title and scope
   - State the exact question being answered.
   - State project, date, and any assumptions when known.

2. Executive answer
   - Give the short answer before details.
   - Separate source-backed facts from inferences.

3. Evidence map
   - Table columns: Role, Symbol, File, Lines, Why it matters.
   - Include only files actually inspected.

4. Architecture diagram
   - Use Mermaid `flowchart LR` or `classDiagram`.
   - Show modules, important classes/functions, and ownership boundaries.

5. Execution flow
   - Use Mermaid `sequenceDiagram` or `flowchart TD`.
   - Show entry point, dispatch/registration, key branches, and final effects.

6. Code walkthrough
   - Explain important code in source order or runtime order.
   - Keep snippets short and cite exact locations.

7. Ambiguities and follow-up
   - List assumptions, uncertain inferences, and suggested follow-up inspection.

## Diagram Guidance

- Prefer two readable diagrams over one dense diagram.
- Keep node names stable and close to real symbol names.
- Add short edge labels only when they clarify ownership, data movement, or conditions.
- Avoid styling that hides semantics. Let text explain what the diagram cannot.

## HTML Guidance

- Escape `<`, `>`, and `&` in code snippets.
- Use `<pre class="mermaid">` blocks for diagrams.
- Use tables for evidence and compact lists for findings.
- Include a small footer with timestamp and source project when appropriate.
