---
name: baz
description: 您可以通过终端创建专业的动态图形和视频。该工具采用人工智能技术，支持多轨道分层、编排、配音以及Lambda函数渲染等功能。其五阶段的工作流程确保了最终作品的质量。
metadata:
  openclaw:
    requires:
      env:
        - BAZ_API_KEY
      bins:
        - node
        - baz
    primaryEnv: BAZ_API_KEY
    install:
      - id: node
        kind: node
        package: bazaar.it
        bins:
          - baz
        label: Install Bazaar CLI (npm)
    homepage: https://bazaar.it
    emoji: "\U0001F3AC"
---
# baz CLI — 强制性视频生成工作流程

当用户希望通过 Bazaar CLI (`baz`) 创建、编辑或导出视频时，请使用此工作流程。

**这是一个有步骤的工作流程。** 你必须按顺序完成每个阶段，不得跳过任何阶段。在底部的完成检查列表未通过之前，不得声明“完成”。

---

## 入门（新用户）

如果你还没有 Bazaar 账户或 API 密钥，请通过编程方式注册：

```bash
# 1. Discover what Bazaar can do
curl https://bazaar.it/api/v1/capabilities

# 2. Register (one POST, no human needed)
curl -X POST https://bazaar.it/api/v1/register \
  -H "Content-Type: application/json" \
  -d '{"email":"your-agent@example.com","name":"My Agent"}'
# Returns: api_key, auth header name, quickstart steps, endpoint URLs

# 3. Save your API key — authenticate all future requests with:
#    -H "x-api-key: <your-api-key>"

# 4. Check pricing before you start
curl https://bazaar.it/api/v1/pricing

# 5. Install the CLI
npm install -g bazaar.it
baz auth login <your-api-key>
```

**初始余额为 $0**。当你进行付费操作时，会收到一个 HTTP 402 错误响应，响应体中包含 `top_up_url`。使用 `{"amount_cents": 500}`（最低 $5）调用 `POST /api/v1/top-up` 来获取 Stripe 结账 URL。

**快捷方式：** 如果你的团队成员在 bazaar.it 上注册了账户，他们将获得 $4 的初始余额。请让他们从仪表板获取 API 密钥，然后你可以直接跳到第 5 步。

已经拥有 API 密钥？请跳到第 1 阶段。

---

## 使用场景

- 用户希望通过 CLI 创建、编辑或导出视频
- 用户希望自动化视频生成
- 用户提到了 “baz”、“bazaar CLI” 或 “从终端生成视频”

## 使用 `baz prompt` 与 `spar` 的区别

- **直接使用 `baz prompt`** — 用于场景创建、编辑以及完整的代理协调
- **`baz prompt --spar`** — 仅用于规划对话（不涉及时间轴的修改）

---

## 第 1 阶段：设置上下文（必填 — 不得跳过）

在生成任何场景之前，你必须设置项目上下文。这为合成代理提供了所需的信息，以确保第一次尝试就能生成正确的输出。

### 最小所需上下文：
1. **目标** — 这个视频的目的是什么？目标受众是谁？他们应该有什么感受或行为？
2. **要求** — 视频必须包含的具体、可验证的内容
3. **品牌** — 颜色、字体、标志位置、视觉风格

```bash
# Create or select project
baz project create --name "Descriptive Name - Date/Purpose" --json
# OR
baz project use <id>

# Set goal (be specific — audience, purpose, desired outcome)
baz context add "Create 45-60 second feature announcement for [Product]. \
Audience: [who]. Key value: [what they get]." --label "goal"

# Add requirements (each one should be independently verifiable)
baz context add "Show [specific feature interaction]" --label "requirement"
baz context add "Include CTA: '[specific text]'" --label "requirement"
baz context add "Total duration: [range]" --label "requirement"

# Set brand guidelines
baz context add "Brand: [Name]. Primary [hex], accent [hex]. Font: [name]. \
[Logo placement]. [Visual style notes]." --label "brand"
```

### 验证上下文是否已设置：
```bash
baz context list --json
```

**规则：** 在 `baz context list` 显示至少一个目标、一个要求和一个品牌信息之前，不得进入第 2 阶段。

---

## 第 2 阶段：生成视频

现在，提示代理创建场景。你可以使用一个完整的提示，或者逐个场景地发送提示。

```bash
# Option A: One comprehensive prompt
baz prompt "Create a video with: [scene 1 description], [scene 2], ..." --stream-json

# Option B: Scene-by-scene (more control)
baz prompt "Scene 1 (5s): Dark gradient intro, logo top-left, title slides up" --stream-json
baz prompt "Scene 2 (7s): Problem statement with mock UI..." --stream-json
baz prompt "Scene 3 (18s): Feature walkthrough..." --stream-json
```

提示技巧：
- 在每个提示中包含视频时长
- 明确指定动画效果、颜色和布局
- 参考第 1 阶段中设置的品牌信息

### 多场景视频的编排（必填）

对于包含 3 个或更多场景的视频，需要在生成之前规划好各场景的播放顺序。这样可以避免所有元素在同一帧边界同时切换的“同步幻灯片”效果。

#### 角色规划模板

在发送提示之前，先规划好各个角色的行为：

| 角色 | 跟踪（Track） | 持续时间（Lifetime） | 角色（Role） |
|-------|-------|----------|------|
| 背景（Background） | 0 | 整个视频时长 | 动态渐变效果、粒子效果 |
| 主角（Hero） | 1 | 60-80% | 主要用户界面元素，进入画面后淡出到角落，再重新出现 |
| 辅助角色（Supporting） | 1-2 | 20-40% | 图片/图表，在主角淡出时出现 |
| 文本（Text） | 2+ | 10-30% | 标题，在节奏关键点出现，有明确的退出效果 |

#### 5 条提示优化规则：

1. **每个内容提示都必须包含退出指令**（例外情况：持续显示的背景、最后的呼叫行动）
2. **在 Track 0 上优先使用一个背景**，且该背景在整个视频期间保持不变
3. **每个叠加层（overlay）的提示都必须指定位置和大小** — 共享屏幕时间的场景不能共享屏幕空间
4. 为主角元素指定动画效果（例如：`spring()` 用于主角进入）
5. 在提示中包含能量级别的提示（如“高能量进入”、“平静持续的部分”）

#### 良好的示例 — 结合上下文和自然语言提示：
```bash
baz context add "CHOREOGRAPHY: Every overlay scene must specify its position and size. \
  Use spring() for hero elements. Every non-final scene must have exit animations. \
  Prefer one continuous background." --label "instructions"

baz prompt "Create a 15-second product demo: dark theme intro with logo, \
  feature showcase with 3 cards, area chart showing growth, and a CTA. \
  Brand: #6366f1 purple, #10b981 green, Inter font." --stream-json
```

使用一个自然语言的提示，合成代理会根据编排上下文在内部处理内容的拆分和空间布局。

---

## 第 3 阶段：审核与验证（必填 — 绝不跳过）

生成视频后，你必须进行审核和验证。这两步都是必须完成的。

### 第 1 步：审核
```bash
baz review --json
```

阅读生成的视频内容，并将其与第 1 阶段中的要求进行对比。

### 第 2 步：验证
```bash
baz verify --criteria "requirement 1,requirement 2,requirement 3" --json
```

将第 1 阶段中的所有要求作为逗号分隔的参数传递给 `verify` 命令。该命令会逐一检查这些要求是否满足。

### 解释验证结果：

```json
{
  "passedAll": true,
  "results": [
    { "criteria": "...", "passed": true },
    { "criteria": "...", "passed": false, "reason": "..." }
  ]
}
```

**规则：** 如果 `passedAll: false`，你必须进入第 4 阶段。不得直接导出视频，也不得声明“完成”。

---

## 第 4 阶段：迭代（如果第 3 阶段失败，则需要执行）

修复所有未满足的要求，然后重新进行验证。

```
LOOP:
  1. Read failing criteria from Phase 3
  2. Fix with: baz prompt "Fix: [specific issue]" --stream-json
  3. Re-run: baz review --json
  4. Re-run: baz verify --criteria "req1,req2,req3" --json
  5. If passedAll: false → GOTO 1
  6. If passedAll: true → proceed to Phase 5
```

在 `passedAll: true` 之前，不要退出这个循环。

---

## 第 5 阶段：导出（仅在用户明确要求的情况下进行）

只有当用户请求生成视频，并且第 3 和第 4 阶段都通过验证后，才能进行导出。

```bash
baz export start --wait --json
```

---

## 命令快速参考

| 命令 | 功能 |
|---------|---------|
| `baz project create --name "..." --json` | 创建新项目 |
| `baz project use <id>` | 设置当前项目 |
| `baz context add "..." --label "goal"` | 设置项目目标 |
| `baz context add "..." --label "requirement"` | 添加可验证的要求 |
| `baz context add "..." --label "brand"` | 设置品牌规范 |
| `baz context list --json` | 查看所有上下文信息 |
| `baz prompt "..." --stream-json` | 生成或编辑场景 |
| `baz prompt "..." --spar` | 仅用于规划对话（不进行编辑） |
| `baz review --json` | 获取项目完整状态以供审核 |
| `baz verify --criteria "..." --json` | 验证特定要求是否满足 |
| `baz scenes list --json` | 列出所有场景 |
| `baz export start --wait --json` | 生成最终视频 |

## 错误处理

| 错误类型 | 处理方式 |
|---------|--------|
| **临时错误（Transient）** | 重试（等待 `retry_after` 秒数） |
| **验证错误（Validation）** | 修复输入数据，不要重复发送相同的请求 |
| **认证错误（Auth）** | 使用 `baz auth status` 检查 API 密钥 |
| **致命错误（Fatal）** | 停止操作并向用户报告错误 |

---

## 完成检查列表

只有在满足以下所有条件后，才能认为工作完成：

- [ ] 第 1 阶段：`baz context list` 显示目标、要求和品牌信息
- [ ] 第 2 阶段：通过 `baz prompt` 生成了视频场景
- [ ] 第 3 阶段：执行了 `baz review --json` 并且 `baz verify --criteria "req1,req2,..." --json` 也通过验证
- [ ] 第 4 阶段：`passedAll: true`（或者在第一次验证时就已经满足）
- [ ] 第 5 阶段：已开始导出视频（仅在用户请求的情况下）

**如果你跳过了审核或验证步骤，请返回并重新执行这些步骤。**

---

## 外部接口

| URL | 方法 | 发送的数据 | 功能 |
|-----|--------|-----------|---------|
| `bazaar.it/api/v1/capabilities` | GET | 无 | 查看可用工具 |
| `bazaar.it/api/v1/register` | POST | 电子邮件、用户名 | 注册代理账户 |
| `bazaar.it/api/v1/pricing` | GET | 无 | 查看操作费用 |
| `bazaar.it/api/v1/estimate` | POST | 操作类型和数量 | 预估费用 |
| `bazaar.it/api/v1/top-up` | POST | 金额（单位：美分） | 获取 Stripe 结账 URL |
| `bazaar.it/api/generate-stream` | POST | 提示内容、项目 ID | 生成视频场景（SSE 格式） |
| `bazaar.it/api/trpc/*` | POST | 不同操作 | 项目 CRUD 操作、场景管理 |

## 安全性与隐私

- **认证**：所有非查询接口都需要 `x-api-key` 请求头
- **发送的数据**：你的提示内容、项目元数据和场景代码会被发送到 Bazaar 服务器进行人工智能处理
- **数据存储**：项目信息、场景内容和生成的资产存储在 Bazaar 的基础设施中（Neon DB + Cloudflare R2）
- **无本地文件访问**：此工具仅使用 `baz` CLI 程序，不会读取或修改本地文件（除了 `~/.bazaar/config.json` 中的配置文件）
- **费用消耗**：操作会消耗余额。在进行大型任务前，请使用 `baz auth status` 查看剩余余额
- **导出结果**：生成的视频会存储在 Bazaar 的 CDN 上，并可通过 URL 访问

## Web 界面访问

你的团队成员也可以通过以下链接直接在浏览器中编辑项目：
`https://bazaar.it/projects/<project-id>/generate`

创建项目后，分享该链接，以便他们可以预览场景、调整代码或配合 CLI 工作流程进行手动编辑。