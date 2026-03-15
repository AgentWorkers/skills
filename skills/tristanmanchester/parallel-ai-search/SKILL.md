---
name: parallel-ai-search
description: 使用 Parallel 的 `parallel-cli` 工具可以执行以下操作：实时网络搜索、URL 提取（生成格式规范的 Markdown 文本）、深度研究报告生成、批量数据清洗（CSV/JSON 格式）、FindAll 实体信息查询、以及网络监控。适用于以下场景：用户需要在线查找信息、获取当前来源或引用资料、提供可供阅读或总结的 URL、进行深入或全面的研究、利用网络数据丰富数据集、获取实体列表（公司/人物/地点），或希望监控网页内容随时间的变化情况。
compatibility: Requires parallel-cli installed + authenticated (PARALLEL_API_KEY or parallel-cli login) and internet access.
metadata:
  author: openclaw
  version: "2.0.0"
  homepage: "https://docs.parallel.ai/integrations/cli"
  openclaw: '{"emoji":"🔎","primaryEnv":"PARALLEL_API_KEY","cli":"parallel-cli"}'
allowed-tools: Bash(parallel-cli:*) Bash(curl:*) Bash(pipx:*) Read
---
# 并行AI搜索（CLI Master）

这是一个**单一的“主”技能**，它取代了之前基于Node脚本的`parallel-ai-search`版本。

该技能会根据任务需求路由到相应的`parallel-cli`功能：

- **搜索**：快速进行网络查询并附上引用链接（`parallel-cli search`）
- **提取**：将URL（包括PDF和JavaScript含量较高的页面）转换为适合大型语言模型（LLM）处理的文本（`parallel-cli extract`）
- **深度研究**：进行多源报告分析（`parallel-cli research ...`）
- **丰富数据**：向CSV/JSON格式中添加从网络获取的列（`parallel-cli enrich ...`）
- **查找所有**：从网络中发现符合条件的实体（`parallel-cli findall ...`）
- **监控**：定期跟踪网站变化（可选，可通过Webhook实现）（`parallel-cli monitor ...`）

## 路由规则（选择其中一个）

选择最简单/成本最低的方法来满足用户请求：

1. **提取**：当用户提供一个或多个URL，或者请求“阅读/总结此页面”、“提取内容”、“引用信息”、“获取页面内容”等时。
2. **深度研究**：仅当用户明确要求进行**深入的、全面的、系统的调查**，或者需要多源报告时使用。
3. **丰富数据**：当用户提供列表/表格（CSV/JSON/内联对象）并希望添加CEO、收入、资金、联系方式等新列时使用。
4. **查找所有**：当用户希望发现符合特定条件的多个实体（公司/人物/场所等）时使用。
5. **监控**：当用户需要持续跟踪网站变化时使用（例如“提醒我”、“定期监控”）。
6. **搜索**：对于其他需要当前网络信息或引用链接的情况，默认使用此方法。

如果用户直接调用此技能，可以使用以下前缀：
- `search: ...`
- `extract: ...`
- `research: ...`
- `enrich: ...`
- `findall: ...`
- `monitor: ...`

如果使用了前缀，请按照前缀的指示执行相应操作。

## 设置和身份验证（仅在需要时）

在运行任何`parallel`命令之前，请确保身份验证功能正常工作：

```bash
parallel-cli auth
```

如果`parallel-cli`未安装，请先安装它：

```bash
curl -fsSL https://parallel.ai/install.sh | bash
```

如果无法使用安装脚本，可以使用`pipx`进行安装：

```bash
pipx install "parallel-web-tools[cli]"
pipx ensurepath
```

然后进行身份验证（选择合适的方法）：

```bash
# Interactive OAuth (opens browser)
parallel-cli login

# Headless / SSH / CI
parallel-cli login --device

# Or environment variable
export PARALLEL_API_KEY="your_api_key"
```

## 输出和引用规则

- **始终引用网络来源的信息**，并使用内联Markdown链接：`[来源标题](https://...)`。
- 在使用搜索/提取/研究功能后，务必附上来源列表。
- 尽量使用**官方/主要**来源。
- 对于较长的输出结果，将其保存到`/tmp/`目录中，并在聊天中提供摘要。

## 搜索（默认的网络查询）

使用搜索功能快速获取带有引用链接的答案。

### 命令模板

```bash
parallel-cli search "$OBJECTIVE"   --mode agentic   --max-results 10   --json
```

仅在相关情况下添加以下选项：
- `--after-date YYYY-MM-DD`（设置结果更新时间）
- `--include-domains a.com b.org`（限制搜索来源）
- `--exclude-domains spam.com`（排除某些来源）
- 一个或多个`-q "关键词查询"`参数（用于进一步筛选）
- `-o "/tmp/$SLUG.search.json"`（将完整结果保存为JSON文件）

### 解析和响应

从JSON结果中提取**标题**、**URL**以及**发布日期**和**摘录**字段。
回答用户的问题，并对每个结果进行引用。

## 提取（提取一个或多个URL的内容）

当需要获取特定URL的实际内容（网页、PDF文件或JavaScript含量较高的网站）时，使用提取功能。

### 命令模板

```bash
parallel-cli extract "$URL" --json
```

仅在相关情况下添加以下选项：
- `--objective "关注领域"`（例如价格、API使用情况等）
- `--full-content`（仅当用户需要完整页面内容时）
- `--no-excerpts`（仅提取内容）
- `-o "/tmp/$SLUG.extract.json"`（将完整结果保存为JSON文件）

### 响应

- 如果用户请求摘要，请结合引用链接进行总结。
- 如果用户请求原始文本，请仅提供摘录部分（前提是文本长度适中）；否则提供关键内容，并建议用户查看保存的结果文件。

## 深度研究（仅在用户明确要求时使用）

深度研究耗时较长，可能比搜索功能更昂贵。仅在用户明确需要深入分析时使用。

### 第一步——启动（始终异步执行）

```bash
parallel-cli research run "$QUESTION" --processor pro-fast --no-wait --json
```

从JSON结果中解析`run_id`（以及任何用于监控的URL），并告知用户任务已开始。

### 第二步——轮询（设置超时时间）

选择一个简短的文件名（小写字母-连字符组合），然后执行以下操作：

```bash
parallel-cli research poll "$RUN_ID" -o "/tmp/$SLUG" --timeout 540
```

- 分享轮询命令生成的**执行摘要**。
- 提及输出文件路径：
  - `/tmp/$SLUG.md`
  - `/tmp/$SLUG.json`

如果轮询超时，重新执行相同的命令——任务将在服务器端继续进行。

## 丰富数据（CSV/JSON或内联数据）

使用丰富数据功能向结构化数据中添加网络来源的列。

### 第一步——（可选）建议添加的列

当用户知道目标数据格式但不知道具体输出结构时，使用此步骤。

### 第二步——执行（大型任务始终异步执行）

对于CSV数据：

```bash
parallel-cli enrich run   --source-type csv   --source "input.csv"   --target "/tmp/enriched.csv"   --source-columns '[{"name":"company","description":"Company name"}]'   --intent "$INTENT"   --no-wait --json
```

对于内联JSON数据：

```bash
parallel-cli enrich run   --data '[{"company":"Google"},{"company":"Apple"}]'   --target "/tmp/enriched.csv"   --intent "$INTENT"   --no-wait --json
```

从JSON结果中解析`taskgroup_id`。

### 第三步——轮询

```bash
parallel-cli enrich poll "$TASKGROUP_ID" --timeout 540 --json
```

任务完成后：
- 告知用户输出文件的路径（即`--target`参数指定的文件）。
- 使用文件阅读工具预览部分数据，并报告数据行数。

如果轮询超时，重新执行任务——任务将在服务器端继续进行。

## 查找所有（实体发现）

当用户需要发现一组实体时（例如“医疗领域的AI初创公司”、“夏洛特市的屋顶公司”、“YC开发工具公司”等），使用查找所有功能。

### 第一步——启动任务

```bash
parallel-cli findall run "$OBJECTIVE" --generator core --match-limit 25 --no-wait --json
```

有用选项：
- `--dry-run --json`（在付费前预览数据结构）
- `--exclude '[{"name":"Example Corp","url":"example.com"}]'`（排除已知实体）
- `--generator preview|base|core|pro`（默认为“基础”模式；“pro”模式适用于复杂查询）

从JSON结果中解析`run_id`。

### 第二步——轮询并获取结果

```bash
parallel-cli findall poll "$RUN_ID" --json
parallel-cli findall result "$RUN_ID" --json
```

响应内容包括：
- 找到的实体总数
- 最匹配实体的列表/表格（包含名称、URL和关键属性）
- 对于模糊匹配的结果，提供相应的说明

## 监控（网站变化跟踪）

当用户需要持续跟踪网站变化时，使用监控功能。

### 创建监控任务：

```bash
parallel-cli monitor create "$OBJECTIVE" --cadence daily --json
```

可选参数：
- `--cadence hourly|daily|weekly|every_two_weeks`（设置监控频率）
- `--webhook https://example.com/hook`（将事件结果发送到外部）
- `--output-schema '<JSON schema string>'`（指定事件数据的结构）

### 管理监控任务

```bash
parallel-cli monitor list --json
parallel-cli monitor get "$MONITOR_ID" --json
parallel-cli monitor update "$MONITOR_ID" --cadence weekly --json
parallel-cli monitor delete "$MONITOR_ID"
parallel-cli monitor events "$MONITOR_ID" --json
parallel-cli monitor simulate "$MONITOR_ID" --json
```

响应中需包含监控任务的ID以及获取事件结果的方法（或确认Webhook的配置方式）。

## 参考资料

- 命令模板和常用模式：`references/command-templates.md`
- 常见故障排除方法：`references/troubleshooting.md`