---
name: felo-slides
description: "使用 Claude Code 中的 Felo PPT Task API 生成 PPT/幻灯片。适用于用户请求创建、生成或导出演示文稿/幻灯片集的情况，或者当使用类似 `/felo-slides` 的明确命令时。该 API 负责处理 API 密钥验证、任务创建、数据轮询以及最终 PPT 文件的生成与输出。"
---
# Felo Slides 技能

## 使用场景

当用户需要创建演示文稿文件时，可以使用此技能：
- 根据主题或大纲生成幻灯片
- 将笔记转换为 PPT 幻灯片集
- 按照指定的页数要求制作演示文稿
- 将演示文稿内容导出为可分享的链接

触发关键词：
- 与制作幻灯片或演示文稿相关的中文指令
- 英文关键词：slides, PPT, presentation deck, generate presentation
- 明确的命令：`/felo-slides`, `use felo slides`

**禁止使用此技能的场景：**
- 实时信息查询（请使用 `felo-search`）
- 与本地代码库文件相关的问题
- 仅需要纯文本处理、无需生成幻灯片的任务

## 设置

### 1. 获取 API 密钥

1. 访问 [felo.ai](https://felo.ai)
2. 进入设置 -> API 密钥
3. 创建并复制您的 API 密钥

### 2. 配置环境变量

**Linux/macOS：**
```bash
export FELO_API_KEY="your-api-key-here"
```

**Windows PowerShell：**
```powershell
$env:FELO_API_KEY="your-api-key-here"
```

## 执行方式

请严格按照以下步骤使用 Bash 命令执行：

### 第一步：检查 API 密钥

```bash
if [ -z "$FELO_API_KEY" ]; then
  echo "ERROR: FELO_API_KEY not set"
  exit 1
fi
```

如果密钥缺失，请停止操作并返回设置指南。

### 第二步：运行 Node 脚本（创建任务并监控进度）

使用随附的脚本（无需 `jq` 依赖）：

```bash
node felo-slides/scripts/run_ppt_task.mjs \
  --query "USER_PROMPT_HERE" \
  --interval 10 \
  --max-wait 1800 \
  --timeout 60
```

脚本功能：
- 通过 `POST https://openapi.felo.ai/v2/ppts` 创建任务
- 通过 `GET https://openapi.felo.ai/v2/tasks/{task_id}/historical` 监控任务进度
- 将 `COMPLETED`/`SUCCESS` 视为任务成功（不区分大小写）
- 将 `FAILED`/`ERROR` 视为任务失败
- 任务状态发生变化后立即停止监控
- 成功时输出 `ppt_url`（备用方案：`live_doc_url`）

**可选的调试输出：**

```bash
node felo-slides/scripts/run_ppt_task.mjs \
  --query "USER_PROMPT_HERE" \
  --interval 10 \
  --max-wait 1800 \
  --json \
  --verbose
```

输出结构化的 JSON 数据，包括：
- `task_id`
- `task_status`
- `ppt_url`
- `live_doc_url`
- `livedoc_short_id`
- `ppt_business_id`

### 第四步：返回结果

成功时，返回：
- `ppt_url`（脚本的默认输出，备用方案为 `live_doc_url`）
- 如果使用了 `--json` 参数，还需返回 `task_id`、任务状态以及可选的元数据

## 输出格式

使用以下响应格式：

```markdown
## PPT Generation Result
- Task ID: <task_id>
- Status: <status>
- PPT URL: <ppt_url>
- Live Doc URL: <live_doc_url or N/A>

## Notes
- livedoc_short_id: <value or N/A>
- ppt_business_id: <value or N/A>
```

**错误格式：**

```markdown
## PPT Generation Failed
- Error Type: <error code or category>
- Message: <readable message>
- Suggested Action: <next step>
```

## 错误处理

已知的 API 错误代码：
- `INVALID_API_KEY`（401）：API 密钥无效或已被吊销
- `PPT_TASK_CREATE_FAILED`（502）：创建任务失败
- `PPT_TASK_QUERY_FAILED`（502）：查询任务失败

**超时处理：**
- 如果达到超时时间，返回最后一次获取的状态，并提示用户稍后重试
- 包含 `task_id`，以便用户可以再次查询任务状态

## 重要提示：
- 仅当用户意图是生成幻灯片时，才使用此技能。
- 必须返回 `task_id`，以便后续查询可以继续在同一任务上进行。
- 未收到任务状态信息时，不要声称任务已完成。
- 尽量减少 API 调用次数：只需创建一次任务，然后进行监控。

## 参考资料：
- [Felo PPT 任务 API](https://openapi.felo.ai/docs/api-reference/v2/ppt-tasks.html)
- [Felo 开放平台](https://openapi.felo.ai/docs/)