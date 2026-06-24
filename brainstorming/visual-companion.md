# Visual Companion Guide

Browser-based visual companion 用于在 brainstorming 中展示 mockups、diagram 和选项对比。它是工具，不是模式；只有视觉问题才使用。

## 何时使用

按每个问题单独判断：用户看见画面是否比阅读描述更容易判断？

使用 browser：

- UI mockups：wireframes、layout、navigation、component designs。
- Architecture diagrams：system components、data flow、relationship maps。
- Side-by-side visual comparisons：布局、配色、视觉方向对比。
- Design polish：look and feel、spacing、visual hierarchy。
- Spatial relationships：state machines、flowcharts、entity relationships。

继续使用 terminal：

- Requirements 和 scope 问题。
- 用文字描述即可判断的 A/B/C 方案。
- Pros/cons、comparison tables。
- API design、data modeling、architecture approach。
- 普通 clarifying questions。

关于 UI 的问题不一定是视觉问题。例如“你想要哪类 wizard？”是概念问题；“这几个 wizard layout 哪个更合适？”才是视觉问题。

## 工作机制

server 监听一个 `screen_dir`，把最新 HTML 文件展示到 browser。你把 HTML fragment 写入 `screen_dir`，用户在 browser 中点击选项；点击事件写入 `state_dir/events`，下一轮再读取。

默认写 HTML fragment。只有需要完全控制页面结构时才写完整 HTML document。fragment 会被 `scripts/frame-template.html` 自动包进统一 frame，包含 header、theme、connection status 和交互脚本。

## 启动 session

只在用户同意 visual companion 后启动：

```bash
scripts/start-server.sh --project-dir /path/to/project --open
```

命令返回 JSON，保存其中的：

- `url`: 完整访问地址，包含 `?key=...`。
- `screen_dir`: 写 HTML screens 的目录。
- `state_dir`: 读取 events 和 server state 的目录。

必须把完整 `url` 给用户，不要去掉 query string。session key 同时保护 HTTP 和 WebSocket 访问。

如果没有捕获 stdout，可读取 `$STATE_DIR/server-info`。使用 `--project-dir` 时，session 默认保存在 `<project>/.superpowers/brainstorm/`。提醒用户如果需要避免提交临时 visual files，应把 `.superpowers/` 加入 `.gitignore`。

### 平台提示

Codex 环境可能回收 detached process。脚本会检测并使用 foreground 方式；如果当前工具调用因此保持运行，不要结束本轮前遗留必须交互的 server。必要时重新打开 shell 或使用当前平台支持的长运行进程机制。

远程或容器环境中 browser 无法访问 loopback 时：

```bash
scripts/start-server.sh \
  --project-dir /path/to/project \
  --host 0.0.0.0 \
  --url-host localhost
```

## 迭代循环

1. 确认 server alive。
   - 检查 `$STATE_DIR/server-info` 存在。
   - 确认 `$STATE_DIR/server-stopped` 不存在。
   - 如果 server 已停，用同一个 `--project-dir` 重启；已有 browser tab 会尝试重连。

2. 写一个新的 HTML file 到 `screen_dir`。
   - 文件名要语义化，例如 `layout.html`、`visual-style-v2.html`。
   - 不要复用文件名。
   - 使用当前环境的文件编辑工具，避免把大段 HTML 直接倒进 terminal。

3. 告诉用户看什么。
   - 每次都给完整 URL。
   - 简短说明屏幕内容。
   - 请用户在 terminal 回复；browser clicks 只是结构化辅助信号。

4. 下一轮读取 feedback。
   - 如果 `$STATE_DIR/events` 存在，读取 JSON lines。
   - 结合 terminal 回复判断用户真实选择。
   - 同一页面可多次点击；最后一次选择通常最重要，但点击顺序也能反映犹豫点。

5. 需要迭代时写新 screen。
   - 例如 `layout-v2.html`。
   - 当前视觉问题确认后再进入下一个问题。

6. 回到 terminal 讨论时推送 waiting screen，避免用户一直看到已经结束的选择。

```html
<div style="display:flex;align-items:center;justify-content:center;min-height:60vh">
  <p class="subtitle">继续在 terminal 中讨论...</p>
</div>
```

## HTML fragments

最小例子：

```html
<h2>哪个布局更合适？</h2>
<p class="subtitle">请关注阅读效率和视觉层级</p>

<div class="options">
  <div class="option" data-choice="a" onclick="toggleSelect(this)">
    <div class="letter">A</div>
    <div class="content">
      <h3>Single Column</h3>
      <p>内容聚焦，阅读路径简单</p>
    </div>
  </div>
  <div class="option" data-choice="b" onclick="toggleSelect(this)">
    <div class="letter">B</div>
    <div class="content">
      <h3>Two Column</h3>
      <p>左侧导航，右侧承载主体内容</p>
    </div>
  </div>
</div>
```

无需写 `<html>`、CSS 或 `<script>`；frame 会提供。

## 常用 CSS classes

Options：

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

Multi-select：

```html
<div class="options" data-multiselect>
  <div class="option" data-choice="a" onclick="toggleSelect(this)">...</div>
</div>
```

Cards：

```html
<div class="cards">
  <div class="card" data-choice="design1" onclick="toggleSelect(this)">
    <div class="card-image"></div>
    <div class="card-body">
      <h3>Name</h3>
      <p>Description</p>
    </div>
  </div>
</div>
```

Mockup container：

```html
<div class="mockup">
  <div class="mockup-header">Preview: Dashboard Layout</div>
  <div class="mockup-body">...</div>
</div>
```

Split view：

```html
<div class="split">
  <div class="mockup">...</div>
  <div class="mockup">...</div>
</div>
```

Pros/Cons：

```html
<div class="pros-cons">
  <div class="pros"><h4>Pros</h4><ul><li>Benefit</li></ul></div>
  <div class="cons"><h4>Cons</h4><ul><li>Drawback</li></ul></div>
</div>
```

Wireframe building blocks：

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

## Browser events

点击事件写入 `$STATE_DIR/events`：

```jsonl
{"type":"click","choice":"a","text":"Option A - Simple Layout","timestamp":1706000101}
{"type":"click","choice":"b","text":"Option B - Hybrid","timestamp":1706000115}
```

如果文件不存在，说明用户没有在 browser 中交互，使用 terminal 回复即可。

## 设计建议

- 根据问题选择 fidelity：layout 用 wireframe，视觉风格才需要更精细 mockup。
- 每页明确问题，例如“哪个 layout 更专业？”而不是只写“选择一个”。
- 每页 2-4 个选项。
- 对依赖真实内容的场景使用真实内容；缺省文本可能掩盖设计问题。
- 保持 mockup 聚焦，不追求 pixel-perfect。

## 清理

```bash
scripts/stop-server.sh $SESSION_DIR
```

使用 `--project-dir` 时，`.superpowers/brainstorm/` 下的 mockups 会保留；临时 `/tmp` session 停止后可删除。

## 参考

- Frame template: `scripts/frame-template.html`
- Helper script: `scripts/helper.js`
