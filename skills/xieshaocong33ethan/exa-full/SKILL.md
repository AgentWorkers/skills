---
name: exa-full
version: 1.2.1
description: Exa AI 搜索 + 研究 API：支持网页搜索、代码搜索、内容提取以及异步的多步骤研究任务，并提供输出结果格式（outputSchema）。
homepage: https://exa.ai
metadata: {"openclaw":{"emoji":"🔍","requires":{"bins":["curl","jq"],"env":["EXA_API_KEY"]}}}
---

# Exa - 搜索与研究

使用此技能可进行网页搜索、代码上下文搜索、URL内容提取以及异步研究工作流程。

## 该技能的功能

- 执行Exa网页搜索，支持选择类别和域名过滤器。
- 获取完整页面内容（可选：爬取子页面）。
- 为编程查询查找代码和文档上下文。
- 运行异步研究任务（一次性执行或创建/轮询工作流程）。
- 支持通过`outputSchema`输出结构化数据。

## 设置

使用以下方法之一设置`EXA_API_KEY`。

```bash
export EXA_API_KEY="your-exa-api-key"
```

```bash
# .env next to SKILL.md
EXA_API_KEY=your-exa-api-key
```

**行为说明：**
- 如果环境中未设置`EXA_API_KEY`，脚本将仅从`.env`文件中加载该值。
- 其他`.env`文件中的变量将被忽略。

## 安全性与数据处理

- `SCHEMA_FILE`的内容会作为`outputSchema`发送到`https://api.exa.ai/research/v1`。
- 请勿使用敏感的本地文件作为`SCHEMA_FILE`（例如：`.env`文件、密钥/证书文件、机密信息或内部文档）。
- `research_create.sh`脚本会屏蔽明显的敏感路径或文件扩展名（例如：`.env`、`.pem`、`.key`、`.p12`、`.pfx`、`id_rsa`）。

## 命令快速参考

### 搜索

```bash
bash scripts/search.sh "query"
```

**主要环境变量：**
- `NUM=10`（最多100个结果）
- `TYPE=auto`（`auto`、`neural`、`fast`、`deep`、`instant`）
- `CATEGORY=`（`company`、`research paper`、`news`、`tweet`、`personal site`、`financial report`、`people`）
- `DOMAINS=domain1.com,domain2.com`
- `EXCLUDE=domain1.com,domain2.com`
- `SINCE=YYYY-MM-DD`
- `UNTIL=YYYY-MM-DD`
- `LOCATION=NL`

**限制：**
- 当`CATEGORY`为`company`或`people`时，不支持`EXCLUDE`选项。
- 当`CATEGORY`为`company`或`people`时，不支持`SINCE`和`UNTIL`选项。
- 当`CATEGORY`为`people`时，`DOMAINS`仅接受LinkedIn相关的域名（`linkedin.com`、`www.linkedin.com`、`*.linkedin.com`）。

### 内容提取

```bash
bash scripts/content.sh "url1" "url2"
```

**主要环境变量：**
- `MAX_CHARACTERS=2000`
- `HIGHLIGHT_SENTENCES=3`
- `HIGHLIGHTS_PER_URL=2`
- `SUBPAGES=10`
- `SUBPAGE_TARGET="docs,reference,api"`
- `LIVECRAWL=preferred`（`preferred`、`always`、`fallback`）
- `LIVECRAWL_TIMEOUT=12000`

### 代码上下文搜索

```bash
bash scripts/code.sh "query" [num_results]
```

### 研究（一次性执行）

```bash
bash scripts/research.sh "instructions"
```

**主要环境变量：**
- `MODEL=exa-research` 或 `MODEL=exa-research-pro`
- `SCHEMA_FILE=path/to/schema.json`
- `POLL_INTERVAL=2`
- `MAX_WAIT_SECONDS=240`
- `EVENTS=true`

### 研究（创建/轮询）

```bash
bash scripts/research_create.sh "instructions" | jq
bash scripts/research_poll.sh "researchId" | jq
```

## 代理决策规则

### 选择搜索类型

请按照以下顺序进行决策：
1. 用户明确要求实时搜索或自动完成搜索 -> `TYPE=instant`。
2. 任务需要广泛的信息覆盖或深入的分析 -> `TYPE=deep`。
3. 用户要求在速度和质量之间取得平衡 -> `TYPE=fast`。
4. 其他情况 -> `TYPE=auto`（默认值）。

**回退/升级规则：**
- 如果搜索速度过慢或时间敏感 -> `deep` -> `auto` -> `fast` -> `instant`。
- 如果搜索结果过于肤浅 -> `instant` -> `fast` -> `auto` -> `deep`。
- 用户的明确要求始终具有最高优先级。

**推荐使用模式：**

```bash
TYPE=auto bash scripts/search.sh "query"
```

## 常见问题**

- 请勿将敏感文件传递给`SCHEMA_FILE`。
- 不要将`CATEGORY=people|company`与`EXCLUDE`、`SINCE`或`UNTIL`选项同时使用。
- 建议使用`https://docs.exa.ai/`作为子页面爬取的起始链接（比`https://exa.ai/docs/reference/`更可靠）。

## 更多示例

请参阅[EXAMPLES.md]以获取分组命令示例和边缘情况的工作流程。