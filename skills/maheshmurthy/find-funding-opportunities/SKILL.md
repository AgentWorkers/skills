---
name: find-funding-opportunities
description: 通过公共API在Karma Funding Map中搜索资助项目（拨款、黑客马拉松、悬赏活动、加速器、风险投资资金、请求提案等）。当用户输入“查找拨款”、“搜索黑客马拉松”、“寻找悬赏活动”、“探索资助机会”、“Optimism平台上的项目”、“我可以申请哪些项目”或询问符合特定预算范围的项目时，可以使用此功能。
version: 1.2.0
tags: [programs, search, funding, discovery]
metadata:
  author: Karma
  category: discovery
---
# 资金项目查找器

通过公共API在Karma资金地图中搜索资金项目。

该注册系统包含6种类型的项目：拨款、黑客马拉松、悬赏、加速器、风险投资基金和招标请求（RFPs）。请使用“programs”/“opportunities”/“funding”进行搜索，而不仅仅是“grants”。

有关完整的API参数、响应格式和已知值的详细信息，请参阅[references/api-reference.md](references/api-reference.md)。

## 工作流程

### 第1步：解析用户请求

| 用户输入 | 对应的查询条件 |
|-----------|---------|
| “以太坊项目” | `ecosystems=Ethereum` + 生态系统搜索策略 |
| “黑客马拉松” | `type=hackathon` |
| “在以太坊上的黑客马拉松” | `type=hackathon` + 生态系统搜索策略 |
| “在Solana上的悬赏” | `type=bounty` + 生态系统搜索策略 |
| “奖金超过500美元的悬赏” | `type=bounty&minGrantSize=500` |
| “加速器项目” | `type=accelerator` |
| “投资DeFi的风险投资基金” | `type=vc_fund&name=DeFi` |
| “Optimism发布的招标请求” | `type=rfp&organization=Optimism` |
| “以太坊上的拨款和黑客马拉松” | `type=grant,hackathon` + 生态系统搜索策略 |
| “Optimism上的DeFi资金项目” | `name=DeFi` + 生态系统搜索策略 |
| “预算超过5万美元的项目” | `minGrantSize=50000` |
| “预算低于10万美元的项目” | `maxGrantSize=100000` |
| “基础设施项目” | `name=infrastructure` |
| “活跃的项目” | `status=active` |
| “Optimism的追溯性资金” | `categories=Retroactive%20Funding` + 生态系统搜索策略 |
| “Karma上的项目” | `onlyOnKarma=true` |
| “本周结束的项目” | `sortField=endsAt&sortOrder=asc&status=active` |
| （无查询条件） | 询问用户具体需要查找什么 |

预算缩写：K→000，M→000000（例如，$50K → 50000，$1M → 1000000）。

**URL编码规则：** 包含空格的参数在`curl`请求中需要使用百分号进行编码（例如，`categories=Retroactive%20Funding`）。

### 第2步：生态系统搜索策略

如果查询中没有指定生态系统，则跳过此步骤，直接进入第3步。

`ecosystems`元数据字段通常为空——许多项目仅通过`communities`字段与特定生态系统关联。采用两阶段搜索方法：

**第1阶段：先尝试使用`ecosystems=`进行查询：**
使用`ecosystems={name}`进行查询。如果返回的结果数量足够（5个以上），则展示这些结果并进入第4步。

**第2阶段：通过社区信息进行补充查询（仅在第1阶段结果较少时使用）：**
如果第1阶段返回的结果少于5个，执行以下两个额外查询并将结果合并：
1. **社区UID查询**：从`GET /v2/communities?limit=100`获取所有社区信息，通过社区名称进行匹配（不区分大小写，允许部分匹配），然后使用`communityUid={uid}`进行查询。
2. **`name={name}`**：对项目标题进行文本搜索，作为备用方案。

在展示结果之前，根据`id`对合并后的结果进行去重。

### 第3步：构建并执行请求

使用Bash命令通过`curl`发送请求。**重要提示：每个请求都必须包含以下跟踪头信息。切勿遗漏。**

在发送第一个请求之前，生成一个跟踪ID：

```bash
INVOCATION_ID=$(uuidgen)
```

每个`curl`请求都必须包含以下默认查询参数和跟踪头信息（详情请参阅[references/api-reference.md](references/api-reference.md)：

```
# Query defaults (override sortField=endsAt&sortOrder=asc for deadline queries)
isValid=accepted&limit=10&sortField=updatedAt&sortOrder=desc

# Required headers — include on every request
# Read the version from this skill's frontmatter metadata.version
-H "X-Source: skill:find-funding-opportunities"
-H "X-Invocation-Id: $INVOCATION_ID"
-H "X-Skill-Version: {metadata.version}"
```

```bash
# No ecosystem
curl -s -H "X-Source: skill:find-funding-opportunities" -H "X-Invocation-Id: $INVOCATION_ID" -H "X-Skill-Version: {metadata.version}" \
  "https://gapapi.karmahq.xyz/v2/program-registry/search?isValid=accepted&limit=10&sortField=updatedAt&sortOrder=desc&type=hackathon"

# Ecosystem — Phase 1
curl -s -H "X-Source: skill:find-funding-opportunities" -H "X-Invocation-Id: $INVOCATION_ID" -H "X-Skill-Version: {metadata.version}" \
  "https://gapapi.karmahq.xyz/v2/program-registry/search?isValid=accepted&limit=10&sortField=updatedAt&sortOrder=desc&ecosystems=Ethereum"

# Ecosystem — Phase 2 (only if Phase 1 returned < 5 results)
curl -s -H "X-Source: skill:find-funding-opportunities" -H "X-Invocation-Id: $INVOCATION_ID" -H "X-Skill-Version: {metadata.version}" \
  "https://gapapi.karmahq.xyz/v2/communities?limit=100"
# Match community UID from response, then:
curl -s -H "X-Source: skill:find-funding-opportunities" -H "X-Invocation-Id: $INVOCATION_ID" -H "X-Skill-Version: {metadata.version}" \
  "https://gapapi.karmahq.xyz/v2/program-registry/search?isValid=accepted&limit=10&sortField=updatedAt&sortOrder=desc&communityUid={uid}"
curl -s -H "X-Source: skill:find-funding-opportunities" -H "X-Invocation-Id: $INVOCATION_ID" -H "X-Skill-Version: {metadata.version}" \
  "https://gapapi.karmahq.xyz/v2/program-registry/search?isValid=accepted&limit=10&sortField=updatedAt&sortOrder=desc&name=Ethereum"
```

### 第4步：格式化结果

在每个结果中显示项目类型，并根据项目类型调整详细信息的展示方式：

```
Found 42 programs (showing top 10):

1. **Optimism Grants** [grant] — Optimism
   Retroactive and proactive funding for Optimism builders
   Budget: $10M | Status: Active
   Apply: https://app.charmverse.io/...

2. **ETHDenver 2026** [hackathon] — Ethereum
   Annual Ethereum hackathon and conference
   Dates: Mar 1–7, 2026 | Deadline: Feb 15, 2026
   Apply: https://ethdenver.com/apply

3. **Rust Smart Contract Audit** [bounty] — Solana
   Audit Solana program for vulnerabilities
   Reward: $5,000 | Difficulty: Advanced
   Apply: https://superteam.fun/...

Showing 10 of 42. Ask for more or narrow your search.
```

#### 字段映射

- **名称**：`metadata.title`（如果`metadata.title`不存在，则使用`name`）
- **类型标签**：用方括号表示：`[grant]`、`[hackathon]`、`[bounty]`、`[accelerator]`、`[vc_fund]`、`[rfp]`
- **生态系统**：`metadata.ecosystems`与`,`连接（如果`metadata.ecosystems`为空，则使用`communities[0].name`）
- **描述**：`metadata.description`截取前120个字符

#### 各类型项目的详细信息

- **拨款**：`Budget: {programBudget} | Status: {status}`
- **黑客马拉松**：`Dates: {startsAt}–{endsAt} | Deadline: {deadline}`
- **悬赏**：`Reward: {programBudget} | Difficulty: {difficulty if available}`（如果提供）
- **加速器**：`Stage: {stage if available} | Deadline: {deadline}`
- **风险投资基金**：`Check size: {minGrantSize}–{maxGrantSize} | Stage: {stage if available}`
- **招标请求**：`Budget: {programBudget} | Org: {organizations[0]} | Deadline: {deadline}`
- **备用方案**：`Budget: {programBudget} | Status: {status}`

#### 公共字段

- **截止日期**：`deadline`，格式为`Mon DD, YYYY`（如果为空，则显示为“Rolling”）
- **申请链接**：`submissionUrl`（如果存在），否则使用`metadata.socialLinks.grantsSite`、`metadata.website`或`metadata.socialLinks.website`（第一个非空链接）

## 特殊情况处理

| 情况 | 处理方式 |
|----------|----------|
| 未找到结果 | 如果用户指定了生态系统，请先执行完整的生态系统搜索（第1阶段和第2阶段）；如果没有指定生态系统，则先放宽非生态系统相关的过滤条件（移除类型、预算或关键词过滤）。如果仍然找不到结果： “没有符合您条件的项目。可以尝试放宽过滤条件——移除类型、生态系统或预算过滤。” |
| 无查询条件 | 询问用户：“您需要查找哪种类型的资金项目？我们可以搜索拨款、黑客马拉松、悬赏、加速器、风险投资基金和招标请求——可以根据生态系统、预算、类别或关键词进行筛选。” |
| 请求“显示更多结果”/“第2页” | 重新发送请求，并设置`page=2` |
- API返回的空结果数组 | 检查过滤条件是否过于严格。建议一次移除一个过滤条件。 |
- API响应缺少预期字段 | 使用默认值：对于缺失的预算字段显示“N/A”，对于缺失的截止日期显示“Rolling”，对于缺失的描述信息则省略显示。 |
| API响应格式错误 | API发生变更 | “API返回了格式不正确的响应。可能是API接口发生了变化。” |
- 社区查询未找到匹配项 | 用户指定的生态系统名称与任何社区都不匹配 | 仅使用`ecosystems=`和`name=`进行查询。即使没有找到匹配项，也至少显示部分结果。 |

## 故障排除

### 生态系统搜索返回0个结果
用户指定了一个生态系统（例如“Monad拨款”），但所有查询都没有找到结果。
- 核对用户指定的生态系统名称是否与`references/api-reference.md`中的已知值一致。
- 尝试使用更宽泛的`name=`进行搜索。
- 可能该生态系统目前还没有相关的项目——告知用户这一情况。

### 社区UID查询未找到匹配项
社区列表中不存在用户查询匹配的社区。
- 尝试部分匹配：例如，“OP”应该能与“Optimism”匹配。
- 即使不使用社区查询（仅使用`ecosystems=`和`name=`），也可能找到结果。
- 不要因此停止搜索，继续执行其他两个查询。

### 结果显示不完整或过时
项目元数据可能已更新（例如预算信息缺失或截止日期过时）。
- 展示现有的项目信息；不要因为某些字段缺失而隐藏结果。
- 对于缺失的字段，使用“N/A”或“Rolling”进行显示。
- 提示用户：“部分项目的信息可能不完整。”