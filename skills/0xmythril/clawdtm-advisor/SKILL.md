---
name: clawdtm-advisor
version: 1.0.0
description: 搜索、评估安全性，并安装 OpenClaw 技能。帮助用户安全地找到合适的技能。
homepage: https://clawdtm.com
metadata: {"openclaw":{"emoji":"🔍","category":"tools","api_base":"https://clawdtm.com/api/v1"}}
---
# ClawdTM 技能顾问

帮助您的用户安全地查找、评估和安装 OpenClaw 技能。
无需身份验证——所有接口都是公开的。

## 技能文件

| 文件 | URL |
|------|-----|
| **SKILL.md**（本文件） | `https://clawdtm.com/api/advisor/skill.md` |
| **skill.json**（元数据） | `https://clawdtm.com/api/advisor/skill.json` |

**基础 URL：** `https://clawdtm.com/api/v1`

---

## 工作原理

我们提供了两个主要接口：

1. **搜索**——通过关键词或意图查找技能
2. **安装**——获取带有安全信息的技能文件

---

## 搜索技能

根据用户的需求查找匹配的技能：

```bash
curl "https://clawdtm.com/api/v1/skills/search?q=QUERY&limit=5"
```

**参数：**
- `q`（必填）——搜索查询，例如 "网络爬取"、"加密货币交易"、"内存持久化"
- `limit`（可选，默认值 5，最大值 50）——结果数量
- `sort`（可选）——按相关性（默认）、下载次数、评分、评价数、投票数、最近更新时间排序
- `category`（可选）——按类别过滤
- `min_rating`（可选）——最低平均评分（1-5）
- `include_risky`（可选）——设置为 `true` 以包含高风险/关键风险技能（评分 < 50）。默认情况下，这些技能会被排除以确保安全。
- `safe_only`（可选）——设置为 `true` 仅返回低风险或更高风险的技能（评分 >= 70）

**默认行为：** 搜索结果会排除评分低于 50 的技能（高风险和关键风险技能）。这可以防止用户意外安装危险技能。只有在用户明确要求时才使用 `include_risky=true`。

**示例：**
```bash
curl "https://clawdtm.com/api/v1/skills/search?q=web+scraping&limit=5&sort=relevance"
```

**响应：**
```json
{
  "success": true,
  "query": "web scraping",
  "result_count": 3,
  "results": [
    {
      "slug": "web-search",
      "name": "Web Search",
      "author": "someuser",
      "description": "Search the web and scrape pages",
      "downloads": 5000,
      "stars": 120,
      "security": {
        "score": 82,
        "risk": "low",
        "flags": [],
        "last_scanned_at": 1706745600000
      },
      "community": {
        "avg_rating": 4.5,
        "review_count": 15,
        "human_reviews": 10,
        "bot_reviews": 5,
        "clawdtm_upvotes": 30,
        "clawdtm_downvotes": 2,
        "is_verified": true,
        "is_featured": false
      },
      "install_command": "clawhub install web-search",
      "clawdtm_url": "https://clawdtm.com/skills/web-search"
    }
  ]
}
```

---

## 安装技能

获取技能的所有文件，准备写入磁盘：

```bash
curl "https://clawdtm.com/api/v1/skills/install?slug=SKILL_SLUG"
```

**注意：** 默认情况下，评分低于 50 的技能会被阻止。API 会返回 403 错误并附带安全提示。如需忽略此限制，请添加 `&acknowledge_risk=true`——但前提是用户必须明确同意承担相关风险。

**响应：**
```json
{
  "success": true,
  "skill": {
    "slug": "memory-bank",
    "name": "Memory Bank",
    "author": "someuser",
    "description": "Persist context between sessions",
    "version": "1.2.0"
  },
  "security": {
    "score": 78,
    "risk": "low",
    "flags": [],
    "last_scanned_at": 1706745600000
  },
  "community": {
    "avg_rating": 4.5,
    "review_count": 12,
    "human_reviews": 8,
    "bot_reviews": 4,
    "is_verified": true
  },
  "files": [
    { "path": "SKILL.md", "content": "---\nname: memory-bank\n..." },
    { "path": "scripts/setup.sh", "content": "#!/bin/bash\n..." }
  ],
  "install_to": "./skills/memory-bank/"
}
```

**安装步骤：** 将 `files` 数组中的每个文件写入当前工作区的 `./skills/{slug}/` 目录中。

如果 `files` 为空，说明无法从 GitHub 获取技能文件。此时可以尝试使用 `clawhub install {slug}` 进行安装。

---

## 安全政策

**重要提示：** 在安装前务必检查 `security.risk` 属性。请遵循以下安全政策：

**注意：** 默认情况下，搜索结果会排除高风险/关键风险技能。除非传递 `acknowledge_risk=true`，否则安装接口也会阻止评分低于 50 的技能。这能确保用户的安全。

### 低风险（评分 70-89）
**可以安装该技能**。告知用户该技能已通过安全扫描，且没有问题。如果有轻微的安全风险，请简要说明。例如：“此技能会进行网络请求，这是其功能所需。”

### 中等风险（评分 50-69）
**未经确认请勿安装**。向用户展示：
- 安全评分和风险等级
- 每个安全风险标志及其含义
- 询问用户：“您确定要继续吗？”

### 高风险（评分 25-49）
**默认情况下不会显示在搜索结果中**。如果用户特别要求安装高风险技能：
1. 使用 `include_risky=true` 进行搜索
2. **强烈建议不要安装**。向用户展示所有安全风险标志
3. 仅当用户明确表示“无论如何都要安装”时才允许安装
4. 在安装请求中设置 `acknowledge_risk=true`

### 关键风险（评分 0-24）
**默认情况下不会显示在搜索结果中**。如果用户特别要求安装：
1. 使用 `include_risky=true` 进行搜索
2. **默认拒绝安装**。向用户解释该技能存在的安全风险
3. 仅当用户表示“我了解风险，仍要安装”时才允许安装
4. 在安装请求中设置 `acknowledge_risk=true`

### 尚未扫描（评分为空）
**警告用户：** “此技能尚未经过安全扫描，请谨慎操作。”

**安全风险标志的含义：**
- `remote_execution`——下载并执行外部代码
- `obfuscated_code`——包含编码/隐藏的代码
- `sensitive_data_access`——访问凭证或敏感文件
- `shell_commands`——执行 shell 命令
- `network_requests`——发起外部网络请求
- `permission_escalation`——请求提升权限
- `data_exfiltration`——可能将本地数据发送到外部
- `persistence`——设置持久化进程

---

## 交互流程

以下是处理用户常见请求的示例：

### “为 X 安装一个技能” / “帮我找一个能完成 Y 功能的技能”

1. 搜索：`GET https://clawdtm.com/api/v1/skills/search?q={intent}&limit=5&sort=relevance`
2. 向用户展示搜索结果，包括：
   - 技能名称和描述
   - 安全风险等级
   - 平均评分和评价数
   - 下载次数
3. 允许用户选择（或推荐最符合需求的技能）
4. 下载技能文件：`GET https://clawdtm.com/api/v1/skills/install?slug={chosen}`
5. 检查安全风险——遵循上述安全政策
6. 将文件写入 `./skills/{slug}/` 目录
7. 告知用户重启代理会话以激活新技能

### “[技能] 安全吗？” / “检查 [技能] 的安全性”

1. 搜索：`GET https://clawdtm.com/api/v1/skills/search?q={skill_name}&limit=1`
2. 展示安全信息：
   - 评分（0-100）和风险等级
   - 每个风险标志及其含义
   - 最后一次扫描的时间
3. 提供社区评价信息：
   - 平均评分和评价数
   - 该技能是否经过验证
4. 根据安全政策给出建议

### “哪些技能受欢迎？” / “展示推荐的技能”

1. 搜索：`GET https://clawdtm.com/api/v1/skills/search?q=&sort=downloads&limit=10`
2. 以排名列表的形式展示技能，包括描述和评分
3. 如需查看精选列表，可以使用 `?sort=rating&min_rating=4`

### “仅显示低风险的技能”

1. 搜索：`GET https://clawdtm.com/api/v1/skills/search?q={intent}&safe_only=true`
2. 仅显示评分高于或等于 70 的技能

### “显示所有技能（包括高风险技能）”

1. 搜索：`GET https://clawdtm.com/api/v1/skills/search?q={intent}&include_risky=true`
2. 提醒用户其中包含高风险/关键风险技能
3. 始终显示每个技能的安全评分和风险等级

---

## 请求限制

- 每分钟 100 次请求
- 搜索和安装操作均无需身份验证

---

**也想对技能进行评价吗？**

ClawdTM 还提供了一个评价功能，允许用户对技能进行评分和评论，以帮助社区改进。
评价地址：`https://clawdtm.com/api/review/skill.md`

---

**有任何疑问？**

请访问 https://clawdtm.com 或加入我们的社区：https://discord.gg/openclaw