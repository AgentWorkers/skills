---
# SKILL.md — lgf (Lead Gen Factory) skill for Claude Code and OpenClaw.
#
# Compatible with:
#   - Claude Code: auto-loaded from .claude/skills/lgf/SKILL.md
#   - OpenClaw:    publishable to ClawHub → `clawhub install lgf`
#
# The `name` field becomes the /slash-command trigger.
# The `description` field is the primary signal for auto-invocation by the AI.

name: lgf
description: 使用 lgf（Lead Gen Factory）进行 B2B 市场潜在客户的研究。当需要寻找潜在客户、评估目标公司、研究行业关键参与者（ICPs）、确定决策者，或为任何 B2B 目标群体生成潜在客户列表时，请使用该工具。
allowed-tools:
  - Bash
  - Read
  - Write
---
# lgf — 领导力生成工厂（Lead Generation Factory）

这是一个命令行工具（CLI），它接收一个免费的理想客户画像（Ideal Customer Profile, ICP）作为输入，并返回一份经过评分和去重处理的B2B潜在客户列表，支持CSV和结构化JSON两种格式。

## 先决条件

请先安装一次lgf（需要Python 3.12或更高版本）：

```bash
# From the repo root
pip install -e .

# Or via pipx for isolated install
pipx install git+https://github.com/Catafal/lead-gen-factory.git
```

验证安装是否成功：

```bash
lgf doctor
```

所需的API密钥（存储在`~/.lgf/.env`文件中）：
- `TAVILY_API_KEY` — 用于网络搜索
- `OPENROUTER_API_KEY` — 用于大语言模型（LLM）的评分和数据提取

---

## 核心命令

使用`--json`标志时，工具会将结果以结构化JSON的形式输出到标准输出（stdout），非常适合AI代理直接捕获和处理，而无需访问文件系统。所有面向人类的进度信息会输出到标准错误流（stderr），可以通过`2>/dev/null`将其抑制。

---

## 使用方式

### 1. 快速生成理想客户画像（最常见的方式）

```bash
lgf research --icp-text "HR Directors at SaaS companies in Spain, 50-500 employees" --json 2>/dev/null
```

### 2. 从文件中读取理想客户画像（适用于复杂的客户资料）

```bash
lgf research --icp icp_examples/skillia_spain.md --json 2>/dev/null
```

### 3. 根据特定条件筛选潜在客户

```bash
lgf research --icp-text "Tech companies in Madrid" --focus "only companies hiring L&D managers" --json 2>/dev/null
```

### 4. 按最低评分筛选潜在客户

```bash
lgf research --icp-text "..." --min-score 8 --json 2>/dev/null
```

### 5. 仅查看搜索结果（不进行爬取或调用大语言模型）

```bash
lgf research --icp-text "..." --dry-run
```

### 6. 检查当前配置

```bash
lgf config
```

---

## JSON输出格式

当使用`--json`标志时，输出到标准输出的JSON数据结构如下：

```json
{
  "leads": [
    {
      "business": "Acme Corp",
      "first": "Ana",
      "last": "García",
      "email": "ana.garcia@acme.com",
      "linkedin": "https://linkedin.com/in/anagarcia",
      "website": "https://acme.com",
      "phone": null,
      "date": "2026-03-09",
      "place_of_work": "Acme Corp, Madrid",
      "icp_fit_score": 9,
      "icp_fit_reason": "HR Director at 120-person SaaS, exact ICP match",
      "source_url": "https://acme.com/team"
    }
  ],
  "count": 1,
  "output_file": "leads_20260309.csv",
  "icp": {
    "target_roles": ["HR Director", "People Director"],
    "company_size_min": 50,
    "company_size_max": 500,
    "industries": ["SaaS", "Tech"],
    "geographies": ["Spain"],
    "min_fit_score": 7
  }
}
```

### 有用的JSON数据处理技巧（使用jq）

```bash
# All emails
lgf research --icp-text "..." --json 2>/dev/null | jq '.leads[].email'

# Count of leads found
lgf research --icp-text "..." --json 2>/dev/null | jq '.count'

# First lead's company + score
lgf research --icp-text "..." --json 2>/dev/null | jq '.leads[0] | {business, icp_fit_score}'

# Filter leads scoring 9+
lgf research --icp-text "..." --json 2>/dev/null | jq '[.leads[] | select(.icp_fit_score >= 9)]'

# LinkedIn URLs only
lgf research --icp-text "..." --json 2>/dev/null | jq '[.leads[].linkedin | select(. != null)]'
```

---

## 如何编写有效的理想客户画像（Ideal Customer Profile）

理想客户画像应包含以下信息：
- **角色**：决策者的职位（例如：“人力资源总监”、“学习与发展经理”、“首席采购官”）
- **公司规模**：员工数量范围（例如：“50-500名员工”）
- **行业**：所属领域（例如：“SaaS”、“金融科技”、“咨询”）
- **地理位置**：所在国家或城市（例如：“西班牙”、“巴塞罗那”、“拉丁美洲航空集团”）
- **附加信息**：公司的发展阶段、技术栈、招聘活动等（可选）

示例理想客户画像内容：
```
HR Directors and People Ops leads at B2B SaaS companies in Spain with 50-500 employees.
Focus on companies with active hiring in engineering or sales. Avoid BPO and consulting firms.
```

---

## 所有可用命令

| 命令          | 功能                         |
|---------------|-----------------------------|
| `lgf research`    | 完整的处理流程：搜索 → 爬取 → 数据提取 → 评分 → 生成CSV文件 |
| `lgf validate-icp`   | 解析并显示理想客户画像内容（不执行完整流程） |
| `lgf config`      | 显示当前配置信息（API密钥已隐藏） |
| `lgf config set KEY VALUE` | 更新`~/.lgf/.env`中的配置项 |
| `lgf profile list`   | 列出已保存的理想客户画像 |
| `lgf profile add <name>` | 将当前理想客户画像保存为指定名称的文件 |
| `lgf doctor`     | 检查工具运行状态（API密钥和网络连接情况） |
| `lgf init`       | 首次使用时的设置向导 |

---

## 评分解释

| 评分          | 含义                         |
|---------------|-----------------------------|
| 8–10           | 非常符合要求——优先考虑这些潜在客户         |
| 6–7            | 较符合要求——值得进一步评估             |
| < 6            | 不太符合要求——系统会使用默认筛选规则       |

默认的最低评分值为7分。可以通过`--min-score`参数进行修改。