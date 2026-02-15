# claw-clawbridge

> **智能连接桥梁**：一个夜间运行的高效率搜索代理，帮助您与合适的人建立联系。

## 概述

Clawbridge 将简单的人类指令转化为持续的、每晚进行的搜索操作。它不仅寻找潜在候选人，还能在您的目标与能够帮助您实现目标的人之间架起桥梁。

1. **人类指令**：您只需一次性定义您所提供的服务和您正在寻找的人。
2. **夜间搜索**：每晚，该代理会遍历 Moltbook、专业社区和公开网络。
3. **智能匹配**：根据指令信号、可信度和近期活动对候选人进行筛选和排名。
4. **连接简报**：每天提供一份“连接简报”，其中包含基于证据的匹配结果和个人化的联系草稿。
5. **人工审核**：您需要审核这些匹配结果，并决定是否与候选人联系，从而完全掌控最终的沟通过程。

## 安装

### 推荐方式：通过 ClawHub

```bash
# Install the ClawHub CLI
npm install -g clawhub

# Install this skill
clawhub install claw-clawbridge
```

### 传统方式：通过 clawdbot CLI

```bash
# From registry
clawdbot skills install claw-clawbridge

# From GitHub
clawdbot skills install github:YOUR_USERNAME/clawbridge-skill
```

### 手动安装

将代码克隆并复制到您的 OpenClaw 工作区：

```bash
git clone https://github.com/YOUR_USERNAME/clawbridge-skill.git ~/.openclaw/workspace/skills/claw-clawbridge
openclaw gateway restart
```

## 输入参数

该技能需要以下输入信息：

### 1. 项目概况（必填）

```yaml
offer: "What your agency/company offers"
ask: "What you want (partners, clients, co-marketing, advisors)"
ideal_persona: "Exact target persona(s)"
verticals:
  - "keyword1"
  - "keyword2"
  - "keyword3"
geo_timezone: "optional - geographic/timezone preferences"
disallowed:
  - "do not contact constraints"
tone: "Short style guidance for draft messages"
```

### 2. 限制条件（可选）

```yaml
no_spam_rules:
  - "No cold outreach to competitors"
  - "Respect unsubscribe requests"
regions:
  - "US"
  - "EU"
avoid_list:
  - "competitor@example.com"
  - "@spam_account"
```

### 3. 目标人群（可选）

```yaml
venues:
  - "moltbook"
  - "web"
  - "communities"
query_templates:
  - "{vertical} + hiring + partner"
  - "{vertical} + looking for + {ask}"
```

### 4. 运行预算（可选）

```yaml
max_searches: 20
max_fetches: 50
max_minutes: 10
```

## 使用的工具

该技能使用了以下 OpenClaw 工具：

| 工具 | 用途 | 使用场景 |
|------|---------|-----------|
| `web_search` | 发现候选人页面 | 快速搜索网站信息 |
| `web_fetch` | 提取页面内容 | 读取候选人资料 |
| `browser` | 处理包含大量 JavaScript 的网站 | 仅在 `web_search` 失败时使用 |

## 安全要求

⚠️ **必须遵守以下安全规范**：

1. **不要在指令中透露敏感信息** – 仅通过环境变量或配置文件传递敏感数据。
2. **使用严格的工具白名单** – 仅在主动搜索时启用 `web_*` 系列工具。
3. **人工审核** – 在 MVP 阶段，切勿自动发送联系信息。
4. **限制执行频率** – 遵守运行预算限制。
5. **避免联系黑名单中的对象** – 绝不联系 `avoid_list` 中的候选人。

## 执行流程

```
┌─────────────────────────────────────────────────────────────────┐
│                     DISCOVERY PHASE                             │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐                  │
│  │web_search│───▶│ Filter   │───▶│ Dedupe   │                  │
│  │ (venues) │    │ Results  │    │ & Queue  │                  │
│  └──────────┘    └──────────┘    └──────────┘                  │
└─────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                     ENRICHMENT PHASE                            │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐                  │
│  │web_fetch │───▶│ Extract  │───▶│ Validate │                  │
│  │ (pages)  │    │ Signals  │    │ Evidence │                  │
│  └──────────┘    └──────────┘    └──────────┘                  │
└─────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                     RANKING PHASE                               │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐                  │
│  │  Score   │───▶│  Rank    │───▶│  Top K   │                  │
│  │ Heuristic│    │  Sort    │    │ Selection│                  │
│  └──────────┘    └──────────┘    └──────────┘                  │
└─────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                     DRAFTING PHASE                              │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐                  │
│  │  Draft   │───▶│  Review  │───▶│  Output  │                  │
│  │ Messages │    │  Tone    │    │  Brief   │                  │
│  └──────────┘    └──────────┘    └──────────┘                  │
└─────────────────────────────────────────────────────────────────┘
```

## 输出结果

该技能以两种格式输出结果：

### 1. 结构化 JSON 文件（`run.json`）

详细格式请参考 `schema/connection_brief.json`。

### 2. 人类可读的 Markdown 文件（`run.md`）

示例报告请参见 `examples/sample_run.md`。

## 候选人筛选规则

### 必需满足的条件（缺少这些条件将导致候选人被排除）

- ✅ 每位候选人至少提供 2 个可信的参考链接。
- ✅ 参考链接必须与您的需求明确相关。
- ✅ 候选人的最近活动时间在 N 天以内（可配置，默认为 30 天）。

## 风险提示

如果候选人符合以下情况，将被标记为风险候选人：

- 🟡 **证据不足** – 参考链接数量较少。
- 🟡 **内容可疑** – 包含促销或可疑信息。
- 🟡 **身份不明确** – 无法核实候选人的真实身份。
- 🟡 **过度推销** – 内容过于宣传性。
- 🟡 **不相关** – 与您的需求关联度低。

## 评分规则（版本 1）

每位候选人的评分依据如下：

| 评分因素 | 权重 | 说明 |
|--------|--------|-------------|
| 相关性 | 30% | 是否与您的需求关键词匹配 |
| 意图 | 25% | 候选人是否正在积极寻找工作或需要招聘 |
| 可信度 | 20% | 在多个来源中的一致性表现 |
| 最新活动 | 15% | 最近的活动记录 |
| 互动性 | 10% | 与您的共同兴趣或所属社区 |

**输出结果**：排名前 K 位的候选人（默认 K=3，可配置为 5-10）。

## 示例

请查看 `examples/` 目录中的文件：

- `sample_run.json` – 完整的 JSON 输出示例。
- `sample_run.md` – 人类可读的报告示例。

## 指令模板

该技能使用位于 `prompts/` 目录下的模块化指令模板：

- `discovery.md` – 如何搜索候选人。
- `filtering.md` – 如何设置筛选条件。
- `ranking.md` – 如何对候选人进行评分和排名。
- `drafting.md` – 如何撰写联系信息。

## 搜索渠道

针对不同渠道的搜索策略位于 `venues/` 目录下：

- `moltbook.md` – Moltbook 平台的搜索策略。
- `web.md` – 通用网络搜索策略。
- `communities.md` – 社区/论坛的搜索策略。

## 配置设置

### 环境变量

```bash
# Optional: Override defaults
CLAWBRIDGE_TOP_K=5                    # Number of candidates to return
CLAWBRIDGE_RECENCY_DAYS=30           # Activity recency threshold
CLAWBRIDGE_MAX_SEARCHES=20           # Max search queries per run
CLAWBRIDGE_MAX_FETCHES=50            # Max page fetches per run
```

### 工作区配置

该技能会从运行环境或配置文件中读取工作区配置信息：

```yaml
workspace_id: "ws_abc123"
workspace_token: "tok_..."  # For vault uploads
delivery_target: "discord"  # or "slack" or "email"
```

## 许可证

采用 MIT 许可证。详细信息请参阅 LICENSE 文件。

## 贡献方式

欢迎贡献代码！请仔细阅读指令模板，确保任何修改都遵循以下原则：

1. 保持输出结果的确定性。
2. 不要在指令中透露任何敏感信息。
3. 确保始终有人参与最终决策过程。
4. 候选人的选择必须基于客观证据。