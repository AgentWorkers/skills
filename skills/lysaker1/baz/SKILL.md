---
name: baz
description: 您可以通过终端创建专业的动态图形和视频。该工具基于人工智能技术，支持多轨道分层、编排、旁白以及Lambda渲染等功能。其五阶段的工作流程确保了视频的质量。
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

**初始余额为 $0**。当你进行付费操作时，会收到一个 HTTP 402 错误响应，响应体中会包含 `top_up_url`。使用 `POST /api/v1/top-up` 并传递 `{"amount_cents": 500}`（最低金额 $5）来获取 Stripe 结账链接。

**快捷方式：** 如果你的团队成员在 bazaar.it 上创建了账户，他们将获得 $4 的初始余额。请让他们从仪表板获取 API 密钥，然后你可以直接跳到第 5 步。

已经拥有 API 密钥？请跳到第 1 阶段。

---

## 使用场景

- 用户希望通过 CLI 创建、编辑或导出视频
- 用户希望自动化视频生成
- 用户提到“baz”、“bazaar CLI”或“从终端生成视频”

## 使用 `baz prompt` 与 `Recipe` 的区别

- **直接使用 `baz prompt`** — 适用于简单场景、无音频编辑
- **`baz prompt --plan`** — 适用于添加旁白、AI 视频、头像或根据 URL 生成视频的场景

---

## 第 1 阶段：设置上下文（必填 — 不得跳过）

在生成任何视频内容之前，你必须设置项目上下文。这为生成代理提供了必要的信息，以确保首次尝试就能生成正确的输出。

### 最小所需上下文：
1. **目标** — 这个视频的目的是什么？目标受众是谁？他们应该有什么感受或行为？
2. **要求** — 视频必须包含的具体、可验证的内容
3. **品牌** — 颜色、字体、Logo 的位置、视觉风格

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

**注意：** 在 `baz context list` 显示至少一个目标、一个要求和一个品牌设置之前，不得进入第 2 阶段。

---

## 第 2 阶段：生成视频内容

现在，向代理发出指令来创建视频场景。你可以使用一个综合性的指令，也可以分别针对每个场景发出指令。

```bash
# Option A: One comprehensive prompt
baz prompt "Create a video with: [scene 1 description], [scene 2], ..." --stream-json

# Option B: Scene-by-scene (more control)
baz prompt "Scene 1 (5s): Dark gradient intro, logo top-left, title slides up" --stream-json
baz prompt "Scene 2 (7s): Problem statement with mock UI..." --stream-json
baz prompt "Scene 3 (18s): Feature walkthrough..." --stream-json
```

**提示：**
- 在每个指令中指定视频的时长
- 明确要求动画效果、颜色和布局
- 参考第 1 阶段中设置的品牌上下文

### 多场景视频的编排（必填）

对于包含 3 个以上场景的视频，需要在生成前规划好各个场景的播放顺序。这样可以避免出现所有元素在同一时间切换的情况。

#### 角色规划模板

在发出指令之前，先规划好各个角色的播放顺序：

| 角色 | 跟踪路径 | 播放时长 | 角色职责 |
|-------|-------|----------|------|
| 背景 | 0 | 整个视频时长 | 显示渐变效果、粒子效果 |
| 主角 | 1 | 60-80% | 显示主要界面，进入画面后淡出到角落，再重新出现 |
| 辅助角色 | 1-2 | 20-40% | 在主角淡出时出现卡片或图表 |
| 文本 | 2+ | 10-30% | 在关键时间点显示标题，有明确的退出效果 |

#### 5 条指令优化规则：
1. **每个内容指令都必须包含退出指令**（例外情况：持续显示的背景元素、最后的号召行动）
2. **建议在 Track 0 上使用相同的背景效果**，以保持整个视频的视觉一致性
3. **每个叠加层指令都必须指定位置和大小** — 共享屏幕时间的场景不能同时占据相同的屏幕空间
4. 为主演角色指定动画效果（例如：`spring()` 用于主角的进入效果）
5. 在指令中说明角色的能量状态（如“高能量进入”、“平静持续的部分”）

#### 示例指令（包含上下文信息）：
```bash
baz context add "CHOREOGRAPHY: Every overlay scene must specify its position and size. \
  Use spring() for hero elements. Every non-final scene must have exit animations. \
  Prefer one continuous background." --label "instructions"

baz prompt "Create a 15-second product demo: dark theme intro with logo, \
  feature showcase with 3 cards, area chart showing growth, and a CTA. \
  Brand: #6366f1 purple, #10b981 green, Inter font." --stream-json
```

通过一个综合性的指令，生成代理会根据编排规则自动分解场景并安排它们的显示顺序。

---

## 第 3 阶段：审核与验证（必填 — 严禁跳过）

生成视频后，你必须进行审核和验证，这两个步骤都是必不可少的。

### 第 1 步：审核
```bash
baz review --json
```

阅读生成的视频内容，检查是否满足第 1 阶段中的所有要求。

### 第 2 步：验证
```bash
baz verify --criteria "requirement 1,requirement 2,requirement 3" --json
```

将第 1 阶段中的所有要求作为逗号分隔的参数传递给 `verify` 命令，该命令会逐一检查这些要求是否得到满足。

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

**注意：** 如果 `passedAll` 的值为 `false`，你必须进入第 4 阶段，不得直接导出视频，也不得声明“完成”。

---

## 第 4 阶段：迭代（如果第 3 阶段失败，则需要执行）

修复所有未通过验证的要求，然后重新进行验证。

```
LOOP:
  1. Read failing criteria from Phase 3
  2. Fix with: baz prompt "Fix: [specific issue]" --stream-json
  3. Re-run: baz review --json
  4. Re-run: baz verify --criteria "req1,req2,req3" --json
  5. If passedAll: false → GOTO 1
  6. If passedAll: true → proceed to Phase 5
```

在 `passedAll` 的值为 `true` 之前，不要退出这个循环。

---

## 第 5 阶段：导出视频（仅在用户明确请求的情况下执行）

只有当用户明确要求生成视频，并且第 3 和第 4 阶段的验证都通过后，才能执行导出操作。

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
| `baz context list --json` | 查看所有上下文设置 |
| `baz prompt "..." --stream-json` | 生成或编辑视频场景 |
| `baz prompt "..." --plan` | 创建视频制作方案（如添加旁白或使用 AI 生成视频） |
| `baz review --json` | 获取项目完整状态以供审核 |
| `baz verify --criteria "..." --json` | 验证特定要求是否满足 |
| `baz scenes list --json` | 列出所有生成的视频场景 |
| `baz export start --wait --json` | 开始渲染最终视频 |

## 错误处理

| 错误类型 | 处理方式 |
|----------|--------|
| **临时性错误** | 重试（等待 `retry_after` 秒数后再次尝试） |
| **验证错误** | 修复输入数据，不要重复发送相同的请求 |
| **身份验证错误** | 使用 `baz auth status` 检查 API 密钥的有效性 |
| **致命错误** | 停止操作并向用户报告错误 |

---

## 完成检查列表

只有在满足以下所有条件后，才能认为任务完成：

- [ ] 第 1 阶段：`baz context list` 显示目标、要求和品牌设置
- [ ] 第 2 阶段：通过 `baz prompt` 生成了视频场景
- [ ] 第 3 阶段：执行了 `baz review --json` 并通过了 `baz verify --criteria "req1,req2,..." --json` 的验证
- [ ] 第 4 阶段：`passedAll` 的值为 `true`（或者在第一次验证时就已经满足）
- [ ] 第 5 阶段：已开始导出视频（仅在用户请求的情况下）

**如果你跳过了审核或验证步骤，请返回并重新执行这些步骤。**

---

## 外部接口

| URL | 方法 | 发送的数据 | 功能 |
|-----|--------|-----------|---------|
| `bazaar.it/api/v1/capabilities` | GET | 无 | 查看可用的工具 |
| `bazaar.it/api/v1/register` | POST | 提供电子邮件地址和名称 | 注册新账户 |
| `bazaar.it/api/v1/pricing` | GET | 查看操作费用 |
| `bazaar.it/api/v1/estimate` | POST | 提供操作费用估算 |
| `bazaar.it/api/v1/top-up` | POST | 输入金额（以美分为单位） | 获取 Stripe 结账链接 |
| `bazaar.it/api/generate-stream` | POST | 提供指令和项目 ID | 生成视频场景 |
| `bazaar.it/api/trpc/*` | POST | 提供项目相关的 CRUD 操作和场景管理功能 |

## 安全性与隐私政策

- **身份验证**：所有非查询接口都需要在请求头中包含 `x-api-key`
- **数据传输**：你提供的指令、项目元数据和视频场景代码会被发送到 Bazaar 服务器进行 AI 处理
- **数据存储**：项目信息、视频场景和生成的文件存储在 Bazaar 的基础设施（Neon DB + Cloudflare R2）上
- **禁止访问本地文件**：此工具仅使用 `baz` CLI，不会读取或修改本地文件（除了 `~/.bazaar/config.json` 中的配置文件）
- **费用消耗**：操作会消耗账户余额。在执行大型任务前，请使用 `baz auth status` 检查剩余余额
- **视频导出**：生成的视频会存储在 Bazaar 的 CDN 服务器上，并可通过 URL 访问

## 网页界面

用户也可以通过浏览器直接访问项目页面进行编辑：
`https://bazaar.it/projects/<project-id>/generate`

创建项目后，分享该链接，用户可以在浏览器中预览视频场景、修改代码或进行手动编辑。