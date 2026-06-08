# HTML Report Format

架构评审报告是写到 OS temp directory 的 self-contained HTML file。它不应落进仓库，除非用户明确要求保存。

## Scaffold

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Architecture review - {{repo name}}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="module">
      import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
      mermaid.initialize({ startOnLoad: true, theme: "neutral", securityLevel: "loose" });
    </script>
    <style>
      .seam { stroke-dasharray: 4 4; }
      .leak { stroke: #dc2626; }
      .deep { background: linear-gradient(135deg, #0f172a, #1e293b); }
    </style>
  </head>
  <body class="bg-stone-50 text-slate-900 font-sans">
    <main class="max-w-5xl mx-auto px-6 py-12 space-y-12">
      <header>...</header>
      <section id="candidates" class="space-y-10">...</section>
      <section id="top-recommendation">...</section>
    </main>
  </body>
</html>
```

## Header

包含 repo name、date 和简短 legend：

- solid box = module
- dashed line = seam
- red arrow = leakage
- thick dark box = deep module

不要写长 introduction。直接进入 candidates。

## Candidate Card

每个 candidate 使用一个 `<article>`：

- Title: 短标题，直接命名 deepening。
- Badge row: recommendation strength，取值 `Strong`、`Worth exploring`、`Speculative`。
- Dependency tag: `in-process`、`local-substitutable`、`ports & adapters`、`mock`。
- Files: monospaced file list。
- Before / After diagram: 报告重点，左右对比。
- Problem: 一句话说明 architecture friction。
- Solution: 一句话说明 deepening shape。
- Wins: 不超过 5 个短 bullets，使用 locality、leverage、interface、seam。
- Evidence: 文件和行为证据。
- ADR callout: 如有冲突，用 amber callout 标注。

如果 prose 需要很多段才能解释清楚，优先重画 diagram。

## Diagram Patterns

### Mermaid Graph

适合 dependency graph、call flow 或 sequence。

```html
<div class="rounded-lg border border-slate-200 bg-white p-4">
  <pre class="mermaid">
    flowchart LR
      A[OrderHandler] --> B[OrderValidator]
      B --> C[OrderRepo]
      C -.leak.-> D[PricingClient]
      classDef leak stroke:#dc2626,stroke-width:2px;
      class C,D leak
  </pre>
</div>
```

### Hand-built Boxes and Arrows

当 Mermaid layout 难以表达一个 thick deep module 及其 faded internals 时，用 HTML div 和 inline SVG 手写。

### Cross-section

适合表现 layered shallowness。Before 是多个薄层；After 是一个承担责任的厚 module。

### Mass Diagram

适合表现 interface 几乎和 implementation 一样大。Before 的 interface rectangle 接近 implementation；After 的 interface 小，implementation 大。

### Call-graph Collapse

Before 展示分散 call tree；After 把 tree 收进一个 deep module，内部调用淡化显示。

## Style Guidance

- 风格偏 editorial，不做 dashboard。
- 主色克制：stone/slate 为底，一种 accent，red 只表示 leakage，amber 只表示 warning。
- Diagrams 高度约 320px，保证 before/after 可以并排阅读。
- 模块标签用 `text-xs uppercase tracking-wider`。
- 除 Tailwind CDN 和 Mermaid ESM import 外，不加其他 scripts。

## Top Recommendation

报告末尾放一个更大的 card：

- candidate name
- 一句话说明为什么先做它
- 链接到 candidate card

## Tone

使用简洁 English 或中英混合，但 architecture nouns 必须来自 `language.md`：module、interface、implementation、depth、deep、shallow、seam、adapter、leverage、locality。

避免：component、service、unit、API、signature、boundary。
