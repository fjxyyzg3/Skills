# Visual Companion Guide（Visual Companion 指南）

Browser-based visual brainstorming companion for showing mockups, diagrams, and options.

> **中文译文：** 基于浏览器的可视化 brainstorming companion，用于展示 mockup、diagram 和选项。

## When to Use（何时使用）

Decide per-question, not per-session. The test: **would the user understand this better by seeing it than reading it?**

> **中文译文：** 按问题决定，而不是按 session 决定。判断标准是：**用户通过看而不是读，是否能更好地理解？**

**Use the browser** when the content itself is visual:

- **UI mockups** — wireframes, layouts, navigation structures, component designs
- **Architecture diagrams** — system components, data flow, relationship maps
- **Side-by-side visual comparisons** — comparing two layouts, two color schemes, two design directions
- **Design polish** — when the question is about look and feel, spacing, visual hierarchy
- **Spatial relationships** — state machines, flowcharts, entity relationships rendered as diagrams

> **中文译文：** 当内容本身具有视觉性时，**使用浏览器**：
>
> - **UI mockup** —— wireframe、layout、导航结构和 component 设计。
> - **Architecture diagram** —— 系统 component、data flow 和关系图。
> - **并排视觉对比** —— 比较两种 layout、两种配色方案或两种设计方向。
> - **设计打磨** —— 问题涉及外观与质感、间距或视觉层级时。
> - **空间关系** —— 以 diagram 呈现的状态机、流程图和实体关系。

**Use the terminal** when the content is text or tabular:

- **Requirements and scope questions** — "what does X mean?", "which features are in scope?"
- **Conceptual A/B/C choices** — picking between approaches described in words
- **Tradeoff lists** — pros/cons, comparison tables
- **Technical decisions** — API design, data modeling, architectural approach selection
- **Clarifying questions** — anything where the answer is words, not a visual preference

> **中文译文：** 当内容是文本或表格时，**使用 terminal**：
>
> - **需求和 scope 问题** —— “X 是什么意思？”“哪些 feature 在 scope 内？”
> - **概念性的 A/B/C 选择** —— 在用文字描述的方案之间选择。
> - **Trade-off 列表** —— 优缺点和对照表。
> - **技术决策** —— API 设计、数据建模和 architecture 方案选择。
> - **澄清问题** —— 答案是文字而非视觉偏好的任何问题。

A question *about* a UI topic is not automatically a visual question. "What kind of wizard do you want?" is conceptual — use the terminal. "Which of these wizard layouts feels right?" is visual — use the browser.

> **中文译文：** 一个*关于* UI 话题的问题并不会自动成为视觉问题。“你想要哪种 wizard？”是概念性问题——使用 terminal。“这些 wizard layout 中哪一种感觉合适？”是视觉问题——使用浏览器。

## How It Works（工作原理）

The server watches a directory for HTML files and serves the newest one to the browser. You write HTML content to `screen_dir`, the user sees it in their browser and can click to select options. Selections are recorded to `state_dir/events` that you read on your next turn.

> **中文译文：** server 监视一个目录中的 HTML 文件，并向浏览器提供最新文件。你把 HTML 内容写入 `screen_dir`，用户会在浏览器中看到内容，并可点击选择选项。选择会记录到 `state_dir/events`，供你在下一轮读取。

**Content fragments vs full documents:** If your HTML file starts with `<!DOCTYPE` or `<html`, the server serves it as-is (just injects the helper script). Otherwise, the server automatically wraps your content in the frame template — adding the header, CSS theme, connection status, and all interactive infrastructure. **Write content fragments by default.** Only write full documents when you need complete control over the page.

> **中文译文：** **内容片段与完整文档：** 如果 HTML 文件以 `<!DOCTYPE` 或 `<html>` 开头，server 会原样提供它（仅注入 helper script）。否则，server 会自动使用 frame 模板包装内容，并添加 header、CSS 主题、连接状态和全部交互基础设施。**默认编写内容片段。** 只有需要完全控制页面时才编写完整文档。

## Starting a Session（启动 Session）

```bash
# Start AFTER the user approves the companion. --open auto-opens their browser on
# the first screen; --project-dir persists mockups and enables same-port restart.
scripts/start-server.sh --project-dir /path/to/project --open

# Returns: {"type":"server-started","port":52341,
#           "url":"http://localhost:52341/?key=ab12…",
#           "screen_dir":"/path/to/project/.superpowers/brainstorm/12345-1706000000/content",
#           "state_dir":"/path/to/project/.superpowers/brainstorm/12345-1706000000/state"}
```

> **中文译文：** 用户批准 companion 后，使用 `--project-dir` 启动 server，以持久化 mockup 并支持在同一 port 重启；使用 `--open` 让浏览器自动打开第一个 screen。命令返回 server 的 port、带 session key 的完整 URL、`screen_dir` 和 `state_dir`。

Save `screen_dir` and `state_dir` from the response. With `--open`, the browser opens itself when you push the first screen — you don't need to ask the user to open it, but still share the URL as a fallback (headless/remote setups won't auto-open).

> **中文译文：** 保存响应中的 `screen_dir` 和 `state_dir`。使用 `--open` 时，推送第一个 screen 后浏览器会自动打开；无需再要求用户打开，但仍应分享 URL 作为 fallback，因为 headless 或远程环境不会自动打开。

**The URL contains a session key (`?key=…`).** The server rejects any request
without it, so always give the user the **complete** URL from the `url` field —
never strip the query string, and never hand out a bare `http://host:port`. The
key gates HTTP and WebSocket access so a stray browser tab or another machine on
the network can't read the screens or inject events. After the first load the
browser remembers the key via a cookie, so reloads and `/files/*` assets work
without repeating it.

> **中文译文：** **URL 包含 session key（`?key=…`）。** server 会拒绝不带 key 的请求，因此必须始终向用户提供 `url` 字段中的**完整** URL；不得移除 query string，也不得提供裸 `http://host:port`。该 key 会限制 HTTP 和 WebSocket 访问，防止无关浏览器 tab 或网络上的其他机器读取 screen 或注入 event。首次加载后，浏览器通过 cookie 记住 key，因此 reload 和 `/files/*` asset 无需重复携带 key。

**Finding connection info:** The server writes its startup JSON to `$STATE_DIR/server-info`. If you launched the server in the background and didn't capture stdout, read that file to get the URL and port. When using `--project-dir`, check `<project>/.superpowers/brainstorm/` for the session directory.

> **中文译文：** **查找连接信息：** server 会把启动 JSON 写入 `$STATE_DIR/server-info`。如果在后台启动 server 且没有捕获 stdout，请读取该文件获取 URL 和 port。使用 `--project-dir` 时，在 `<project>/.superpowers/brainstorm/` 下查找 session 目录。

**Note:** Pass the project root as `--project-dir` so mockups persist in `.superpowers/brainstorm/` and survive server restarts. Without it, files go to `/tmp` and get cleaned up. Remind the user to add `.superpowers/` to `.gitignore` if it's not already there.

> **中文译文：** **注意：** 把项目根目录作为 `--project-dir` 传入，使 mockup 持久化到 `.superpowers/brainstorm/` 并在 server 重启后保留。不传时，文件会写入 `/tmp` 并被清理。如果 `.superpowers/` 尚未加入 `.gitignore`，请提醒用户添加。

**Launching the server by platform:**

> **中文译文：** **按平台启动 server：**

**Claude Code:**
```bash
# Default mode works — the script backgrounds the server itself.
scripts/start-server.sh --project-dir /path/to/project --open
```

On Windows, the script auto-detects and switches to foreground mode (which blocks the tool call). Use `run_in_background: true` on the Bash tool call so the server survives across conversation turns, then read `$STATE_DIR/server-info` on the next turn to get the URL and port.

> **中文译文：** 默认模式可用，脚本会自行让 server 在后台运行。Windows 上脚本会自动检测并切换到会阻塞 tool call 的前台模式；在 Bash tool call 上使用 `run_in_background: true`，使 server 能跨对话轮次存活，然后在下一轮读取 `$STATE_DIR/server-info` 获取 URL 和 port。

**Codex:**
```bash
# Codex reaps background processes. The script auto-detects CODEX_CI and
# switches to foreground mode. Run it normally — no extra flags needed.
scripts/start-server.sh --project-dir /path/to/project --open
```

> **中文译文：** Codex 会回收后台进程。脚本会自动检测 `CODEX_CI` 并切换到前台模式；正常运行即可，无需额外 flag。

**Gemini CLI:**
```bash
# Use --foreground and set is_background: true on your shell tool call
# so the process survives across turns
scripts/start-server.sh --project-dir /path/to/project --open --foreground
```

> **中文译文：** 使用 `--foreground`，并在 shell tool call 上设置 `is_background: true`，使进程跨轮次存活。

**Copilot CLI:**
```bash
# Use --foreground and start the server via the bash tool with mode: "async"
# so the process survives across turns. Capture the returned shellId for
# read_bash / stop_bash if you need to interact with it later.
scripts/start-server.sh --project-dir /path/to/project --open --foreground
```

> **中文译文：** 使用 `--foreground`，并通过 mode 为 `async` 的 Bash tool 启动 server，使进程跨轮次存活。保存返回的 `shellId`，以便需要时交给 read_bash 或 stop_bash。

**Other environments:** The server must keep running in the background across conversation turns. If your environment reaps detached processes, use `--foreground` and launch the command with your platform's background execution mechanism.

> **中文译文：** **其他环境：** server 必须跨对话轮次持续在后台运行。如果环境会回收 detached 进程，请使用 `--foreground`，并通过所在平台的后台执行机制启动命令。

If the URL is unreachable from your browser (common in remote/containerized setups), bind a non-loopback host:

```bash
scripts/start-server.sh \
  --project-dir /path/to/project \
  --host 0.0.0.0 \
  --url-host localhost
```

Use `--url-host` to control what hostname is printed in the returned URL JSON.

> **中文译文：** 如果浏览器无法访问该 URL（远程或容器化环境中很常见），请按上例绑定非 loopback host。使用 `--url-host` 控制返回的 URL JSON 中打印哪个 hostname。

## The Loop（主循环）

1. **Check server is alive**, then **write HTML** to a new file in `screen_dir`:
   - **Required: confirm the server is alive before referring to the URL or pushing a screen.** Check that `$STATE_DIR/server-info` exists and `$STATE_DIR/server-stopped` does not. If it has shut down, restart it with `start-server.sh` using the **same `--project-dir`** — it reuses the same port, so the user's open tab reconnects on its own (it shows a "paused" overlay while the server is down) and you don't need to send a new URL. The server auto-exits after 4 hours idle (configurable with `--idle-timeout-minutes`).
   - Use semantic filenames: `platform.html`, `visual-style.html`, `layout.html`
   - **Never reuse filenames** — each screen gets a fresh file
   - Use your file-creation tool — **never use cat/heredoc** (dumps noise into terminal)
   - Server automatically serves the newest file

> **中文译文：**
> 1. **确认 server 存活**，然后把 HTML 写入 `screen_dir` 中的新文件：
>    - **引用 URL 或推送 screen 前，必须确认 server 存活。** 检查 `$STATE_DIR/server-info` 存在且 `$STATE_DIR/server-stopped` 不存在。如果 server 已停止，用**同一个 `--project-dir`** 通过 `start-server.sh` 重启；它会复用同一 port，因此用户已打开的 tab 会自动重连（server 停止时显示 “paused” overlay），无需发送新 URL。server 在空闲 4 小时后自动退出，可通过 `--idle-timeout-minutes` 配置。
>    - 使用语义化文件名，例如 `platform.html`、`visual-style.html`、`layout.html`。
>    - **绝不复用文件名**——每个 screen 都使用新文件。
>    - 使用你的文件创建 tool；**绝不使用 cat/heredoc**，因为它会向 terminal 输出噪音。
>    - server 会自动提供最新文件。

2. **Tell user what to expect and end your turn:**
   - Remind them of the URL (every step, not just first)
   - Give a brief text summary of what's on screen (e.g., "Showing 3 layout options for the homepage")
   - Ask them to respond in the terminal: "Take a look and let me know what you think. Click to select an option if you'd like."

> **中文译文：**
> 2. **告诉用户会看到什么，然后结束当前轮次：**
>    - 每一步都提醒用户 URL，而不只是第一次。
>    - 用简短文本概述 screen 内容，例如“正在展示首页的 3 种 layout 选项”。
>    - 请用户在 terminal 中回复：“看一下并告诉我你的想法；如果愿意，可以点击选择一个选项。”

3. **On your next turn** — after the user responds in the terminal:
   - Read `$STATE_DIR/events` if it exists — this contains the user's browser interactions (clicks, selections) as JSON lines
   - Merge with the user's terminal text to get the full picture
   - The terminal message is the primary feedback; `state_dir/events` provides structured interaction data

> **中文译文：**
> 3. **下一轮**——用户在 terminal 中响应后：
>    - 如果 `$STATE_DIR/events` 存在，就读取它；该文件以 JSON 行记录用户的浏览器交互（点击和选择）。
>    - 与用户的 terminal 文本合并，得到完整反馈。
>    - terminal 消息是主要反馈；`state_dir/events` 提供结构化交互数据。

4. **Iterate or advance** — if feedback changes current screen, write a new file (e.g., `layout-v2.html`). Only move to the next question when the current step is validated.

> **中文译文：**
> 4. **迭代或推进**——如果反馈改变了当前 screen，就写入新文件（例如 `layout-v2.html`）。只有当前步骤通过验证后，才能进入下一个问题。

5. **Unload when returning to terminal** — when the next step doesn't need the browser (e.g., a clarifying question, a tradeoff discussion), push a waiting screen to clear the stale content:

   ```html
   <!-- filename: waiting.html (or waiting-2.html, etc.) -->
   <div style="display:flex;align-items:center;justify-content:center;min-height:60vh">
     <p class="subtitle">Continuing in terminal...</p>
   </div>
   ```

   This prevents the user from staring at a resolved choice while the conversation has moved on. When the next visual question comes up, push a new content file as usual.

> **中文译文：**
> 5. **返回 terminal 时卸载内容**——如果下一步不需要浏览器（例如澄清问题或 trade-off 讨论），推送如上 waiting screen 来清除过时内容。这样可避免对话已推进时，用户仍盯着已经解决的选项。下一个视觉问题出现后，再照常推送新的内容文件。

6. Repeat until done.

> **中文译文：** 6. 重复以上步骤，直到完成。

## Writing Content Fragments（编写内容片段）

Write just the content that goes inside the page. The server wraps it in the frame template automatically (header, theme CSS, connection status, and all interactive infrastructure).

> **中文译文：** 只编写页面内部的内容。server 会自动用 frame 模板包装内容，并添加 header、主题 CSS、连接状态和全部交互基础设施。

**Minimal example:**

> **中文译文：** **最小示例：**

```html
<h2>Which layout works better?</h2>
<p class="subtitle">Consider readability and visual hierarchy</p>

<div class="options">
  <div class="option" data-choice="a" onclick="toggleSelect(this)">
    <div class="letter">A</div>
    <div class="content">
      <h3>Single Column</h3>
      <p>Clean, focused reading experience</p>
    </div>
  </div>
  <div class="option" data-choice="b" onclick="toggleSelect(this)">
    <div class="letter">B</div>
    <div class="content">
      <h3>Two Column</h3>
      <p>Sidebar navigation with main content</p>
    </div>
  </div>
</div>
```

That's it. No `<html>`, no CSS, no `<script>` tags needed. The server provides all of that.

> **中文译文：** 仅此而已。不需要 `<html>`、CSS 或 `<script>` tag；server 会提供这些内容。

## CSS Classes Available（可用的 CSS Class）

The frame template provides these CSS classes for your content:

> **中文译文：** frame 模板为内容提供以下 CSS class：

### Options (A/B/C choices)（选项：A/B/C 选择）

```html
<div class="options">
  <div class="option" data-choice="a" onclick="toggleSelect(this)">
    <div class="letter">A</div>
    <div class="content">
      <h3>Title</h3>
      <p>Description</p>
    </div>
  </div>
</div>
```

**Multi-select:** Add `data-multiselect` to the container to let users select multiple options. Each click toggles the item's selected styling.

> **中文译文：** **多选：** 在容器上添加 `data-multiselect`，允许用户选择多个选项。每次点击都会切换该项的 selected 样式。

```html
<div class="options" data-multiselect>
  <!-- same option markup — users can select/deselect multiple -->
</div>
```

### Cards (visual designs)（卡片：视觉设计）

```html
<div class="cards">
  <div class="card" data-choice="design1" onclick="toggleSelect(this)">
    <div class="card-image"><!-- mockup content --></div>
    <div class="card-body">
      <h3>Name</h3>
      <p>Description</p>
    </div>
  </div>
</div>
```

### Mockup container（Mockup 容器）

```html
<div class="mockup">
  <div class="mockup-header">Preview: Dashboard Layout</div>
  <div class="mockup-body"><!-- your mockup HTML --></div>
</div>
```

### Split view (side-by-side)（分屏视图：并排）

```html
<div class="split">
  <div class="mockup"><!-- left --></div>
  <div class="mockup"><!-- right --></div>
</div>
```

### Pros/Cons（优缺点）

```html
<div class="pros-cons">
  <div class="pros"><h4>Pros</h4><ul><li>Benefit</li></ul></div>
  <div class="cons"><h4>Cons</h4><ul><li>Drawback</li></ul></div>
</div>
```

### Mock elements (wireframe building blocks)（Mock 元素：wireframe 构建块）

```html
<div class="mock-nav">Logo | Home | About | Contact</div>
<div style="display: flex;">
  <div class="mock-sidebar">Navigation</div>
  <div class="mock-content">Main content area</div>
</div>
<button class="mock-button">Action Button</button>
<input class="mock-input" placeholder="Input field">
<div class="placeholder">Placeholder area</div>
```

### Typography and sections（排版与分区）

- `h2` — page title
- `h3` — section heading
- `.subtitle` — secondary text below title
- `.section` — content block with bottom margin
- `.label` — small uppercase label text

> **中文译文：**
> - `h2` —— 页面标题。
> - `h3` —— 小节标题。
> - `.subtitle` —— 标题下方的次要文本。
> - `.section` —— 带底部 margin 的内容块。
> - `.label` —— 小号大写 label 文本。

## Browser Events Format（浏览器 Event 格式）

When the user clicks options in the browser, their interactions are recorded to `$STATE_DIR/events` (one JSON object per line). The file is cleared automatically when you push a new screen.

> **中文译文：** 用户在浏览器中点击选项时，交互会记录到 `$STATE_DIR/events`，每行一个 JSON 对象。推送新 screen 时，该文件会自动清空。

```jsonl
{"type":"click","choice":"a","text":"Option A - Simple Layout","timestamp":1706000101}
{"type":"click","choice":"c","text":"Option C - Complex Grid","timestamp":1706000108}
{"type":"click","choice":"b","text":"Option B - Hybrid","timestamp":1706000115}
```

The full event stream shows the user's exploration path — they may click multiple options before settling. The last `choice` event is typically the final selection, but the pattern of clicks can reveal hesitation or preferences worth asking about.

> **中文译文：** 完整 event stream 会显示用户的探索路径——他们可能在最终决定前点击多个选项。最后一个 `choice` event 通常是最终选择，但点击模式可能揭示值得追问的犹豫或偏好。

If `$STATE_DIR/events` doesn't exist, the user didn't interact with the browser — use only their terminal text.

> **中文译文：** 如果 `$STATE_DIR/events` 不存在，说明用户没有与浏览器交互——只使用他们的 terminal 文本。

## Design Tips（设计建议）

- **Scale fidelity to the question** — wireframes for layout, polish for polish questions
- **Explain the question on each page** — "Which layout feels more professional?" not just "Pick one"
- **Iterate before advancing** — if feedback changes current screen, write a new version
- **2-4 options max** per screen
- **Use real content when it matters** — for a photography portfolio, use actual images (Unsplash). Placeholder content obscures design issues.
- **Keep mockups simple** — focus on layout and structure, not pixel-perfect design

> **中文译文：**
> - **让 fidelity 匹配问题** —— layout 问题使用 wireframe，设计打磨问题使用精细稿。
> - **在每页解释问题** —— 写“哪个 layout 更专业？”，而不只是“Pick one”。
> - **推进前先迭代** —— 如果反馈改变当前 screen，就编写新版本。
> - **每个 screen 最多提供 2-4 个选项。**
> - **在重要时使用真实内容** —— 例如摄影 portfolio 使用真实图片（Unsplash）。placeholder 内容会掩盖设计问题。
> - **保持 mockup 简洁** —— 聚焦 layout 和结构，而不是像素级完美设计。

## File Naming（文件命名）

- Use semantic names: `platform.html`, `visual-style.html`, `layout.html`
- Never reuse filenames — each screen must be a new file
- For iterations: append version suffix like `layout-v2.html`, `layout-v3.html`
- Server serves newest file by modification time

> **中文译文：**
> - 使用语义化名称，如 `platform.html`、`visual-style.html`、`layout.html`。
> - 绝不复用文件名——每个 screen 必须使用新文件。
> - 迭代时追加版本后缀，如 `layout-v2.html`、`layout-v3.html`。
> - server 按修改时间提供最新文件。

## Cleaning Up（清理）

```bash
scripts/stop-server.sh $SESSION_DIR
```

If the session used `--project-dir`, mockup files persist in `.superpowers/brainstorm/` for later reference. Only `/tmp` sessions get deleted on stop.

> **中文译文：** 如果 session 使用了 `--project-dir`，mockup 文件会持久化到 `.superpowers/brainstorm/`，供以后参考。停止时只会删除 `/tmp` session。

## Reference（参考）

- Frame template (CSS reference): `scripts/frame-template.html`
- Helper script (client-side): `scripts/helper.js`

> **中文译文：**
> - Frame 模板（CSS 参考）：`scripts/frame-template.html`。
> - Helper script（客户端）：`scripts/helper.js`。
