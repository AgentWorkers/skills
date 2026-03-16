---
name: demo-slap
description: 使用 Demo-Slap API 从演示视频中生成 CS2 的精彩片段（highlights）和片段电影（fragmovies），支持与 Leetify 的集成；若 Leetify 无法使用，则可回退到 Demo-Slap 的比赛历史记录来选择最近的比赛数据。该功能适用于用户请求录制精彩片段、渲染视频片段、制作片段电影，或将 CS2 演示视频转换为 MP4 格式时。
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["DEMOSLAP_API_KEY"],
        "bins": ["python3", "openclaw"]
      }
    }
  }
---
# Demo-Slap 高亮技能

该技能用于从 CS2 演示视频中生成 MP4 格式的高亮片段和片段电影。

此技能专为 OpenClaw 环境设计，该环境支持后台任务、本地辅助脚本以及基于聊天的结果推送功能。它使用 Python 3 脚本和 `requests` 包来访问 HTTP API。

**预期的运行时输入参数：**
- **必填参数：** `DEMOSLAP_API_KEY`
- **可选参数：** `LEETIFY_API_KEY`
- **可选的部署辅助工具：** `DEMO_SLAP_watchDOG_JOB_ID`

## 脚本

请在技能根目录下的 `scripts/` 目录中运行相关脚本。

### Demo-Slap
| 脚本 | 功能 |
|--------|---------|
| `demo_slap_matches.py` | 列出 Demo-Slap 的最新比赛记录（位于 `/public-api/matches`）|
| `demo_slap.resolve.py` | 根据索引尝试解析 Demo-Slap 比赛历史记录中的回放/演示视频 URL；如果 API 仅返回 `jobId` 时，会明确显示错误信息|
| `demo_slap_match_pick.py` | 根据索引选择一场 Demo-Slap 比赛，并返回包含 `jobId` 的结构化比赛信息|
| `demo_slap_analyze.py` | 提交比赛进行解析，持续轮询直到解析完成，然后输出高亮片段 JSON 数据|
| `demo_slap_render.py` | 渲染一个或多个高亮片段，持续轮询直到渲染完成，然后输出视频片段 URL|
| `demo_slap_common.py` | 公共辅助工具（配置、API 调用、状态管理）|

### Leetify
| 脚本 | 功能 |
|--------|---------|
| `leetify/leetify_matches.py` | 列出最新的比赛记录|
| `leetify/leetify.resolve.py` | 根据用户名和比赛索引解析回放视频 URL|
| `leetify/leetify_save_id.py` | 将用户名映射到 Steam64 ID|
| `leetify/leetify_common.py` | 公共的 Leetify 辅助工具|

### 比赛来源选择
- 当 `LEETIFY_API_KEY` 可用时，优先使用 Leetify 来查找最新的比赛记录。
- 如果未配置 `LEETIFY_API_KEY` 但 `DEMOSLAP_API_KEY` 可用，则使用 Demo-Slap 的 `/public-api/matches` 来查找比赛记录。
- Swagger 文档地址：`https://api-doc.demo-slap.net/`
- 将 Demo-Slap 的比赛记录作为备用路径，用于列出比赛记录以及在分析/渲染之前选择已分析的比赛或回放内容。

## 运行时文件

在执行过程中，可以使用以下文件作为可选的本地运行时状态文件：
- `data/state.json`
- `data/highlights.json`
- `data/history.log`
- `data/steam_ids.json`
- `data/config.json`

这些文件是用于本地操作的运行时辅助文件，理解或检查技能包本身并不需要这些文件。

`state.json` 文件用于跟踪当前的操作状态：
```json
{
  "status": "idle|analyzing|rendering|done|error",
  "job_id": "...",
  "render_job_id": "...",
  "chat_id": "telegram:182314856",
  "clip_urls": {"highlight_id": "https://..."},
  "progress": "polling 3/30",
  "last_completed_op": "analyze|render",
  "notification": {
    "sent": false,
    "sent_at": null,
    "last_attempt_at": null,
    "error": null
  },
  "updated_at": "ISO timestamp"
}
```

## 工作流程

### 1. 查找比赛记录
- **当 `LEETIFY_API_KEY` 可用时，优先使用的路径：**
```bash
python3 scripts/leetify/leetify_matches.py <USERNAME> [--limit 10]
```

- **当 `LEETIFY_API_KEY` 不存在但 `DEMOSLAP_API_KEY` 可用时，使用的备用路径：**
```bash
python3 scripts/demo_slap_matches.py [<USERNAME>] [--limit 10]
```
  - 使用 Demo-Slap 的 `/public-api/matches` 路径
  - 如需查看 API 的详细规范，请参考 Demo-Slap 的 Swagger 文档：`https://api-doc.demo-slap.net/`
  - 如果提供了 `<USERNAME>` 并且已进行映射，尽可能根据该玩家的 Steam ID 过滤比赛记录
- 用户选择比赛记录后，执行以下操作：**
```bash
python3 scripts/demo_slap_match_pick.py [<USERNAME>] --match-index <N>
```
  - 将返回的 `jobId` 作为后续 Demo-Slap 操作的主要标识符

### 2. 解析回放视频 URL
- **使用 Leetify 时，优先使用的路径：**
```bash
python3 scripts/leetify/leetify_resolve.py <USERNAME> --match-index <N>
```

- **使用 Demo-Slap 作为备用路径时：**
```bash
python3 scripts/demo_slap_match_pick.py [<USERNAME>] --match-index <N>
```
  - 使用返回的 `jobId` 作为选定的比赛标识符
  - 如果存在 `demoUrl`，可以继续使用基于 URL 的解析方法
  - 如果没有 `demoUrl`，则跳过 URL 解析，直接通过接受现有 `jobId` 的 API 端点进行解析
  - 使用 `GET /public-api/analyze/{jobId}/status` 和 `GET /public-api/analyze/{jobId}/data` 来查看现有的高亮片段
  - 如果用户需要已存在的视频片段和高亮片段，可以直接从该 `jobId` 进行渲染

### 3. 在后台进行分析
```bash
python3 -u scripts/demo_slap_analyze.py --url '<REPLAY_URL>' --username <USERNAME> --chat-id <CHAT_ID>
```

使用 `exec(background: true)` 运行脚本，并保留返回的进程/会话 ID。

**针对 OpenClaw 环境的可选部署监控模式：**
- 仅在后台分析/渲染工作需要定期检查时使用监控工具。
- 如果已有现有的部署监控工具，可以直接重用，无需总是创建新的持久性调度任务。
- 如果部署选择通过内置的 `cron` 工具创建或启用监控工具，请确保其作用范围仅限于当前运行任务，并在任务完成后禁用它。
- 默认的间隔时间为 2 分钟。
- 使用 `scripts/demo_slap_watchdog.sh status|tail|job` 仅作为本地辅助工具，用于检查运行时状态、日志或特定于部署的任务信息。
- 在运行时，以 `data/state.json` 和 `data/highlights.json` 作为数据来源。

**代理工作流程：**
1. 选择比赛来源：
   - 如果 `LEETIFY_API_KEY` 存在，则使用 Leetify
   - 如果 `LEETIFY_API_KEY` 不存在但 `DEMOSLAP_API_KEY` 存在，则使用 Demo-Slap 的 `/public-api/matches`
2. 如果使用 Leetify，解析回放视频 URL 并进行分析
3. 如果使用 Demo-Slap 作为备用方案，选择比赛记录并获取返回的 `jobId`
4. 如果选定的 Demo-Slap 比赛已有分析数据，直接使用 `jobId` 继续处理，而无需再次进行基于 URL 的分析
5. 仅在长时间的分析/渲染任务需要时启用监控工具
6. 启动分析或渲染操作，并保存返回的进程/会话 ID
7. 如果部署使用了监控工具，让监控工具来传递结果
8. 在任务完成后禁用监控工具

### 4. 在后台进行渲染
```bash
# Single highlight
python3 -u scripts/demo_slap_render.py <JOB_ID> <HIGHLIGHT_ID> --chat-id <CHAT_ID>

# Fragmovie
python3 -u scripts/demo_slap_render.py <JOB_ID> <ID1> <ID2> ... --fragmovie --chat-id <CHAT_ID>
```

使用 `exec/background: true)` 运行脚本，并保留返回的进程/会话 ID。

**针对 OpenClaw 环境的可选部署监控模式：**
- 仅在后台分析/渲染工作需要定期检查时使用监控工具。
- 如果已有现有的部署监控工具，可以直接重用，无需总是创建新的持久性调度任务。
- 如果部署选择通过内置的 `cron` 工具创建或启用监控工具，请确保其作用范围仅限于当前运行任务，并在任务完成后禁用它。
- 默认的间隔时间为 2 分钟。
- 使用 `scripts/demo_slap_watchdog.sh status|tail|job` 仅作为本地辅助工具，用于检查运行时状态、日志或特定于部署的任务信息。
- 在运行时，以 `data/state.json` 和 `data/highlights.json` 作为数据来源。

**代理工作流程：**
1. 仅在当前运行任务需要时启用或重用部署监控工具
2. 启动渲染操作并保存返回的进程/会话 ID
3. 轮询进程输出中的 `Estimated finish:` 行，如果存在该信息，则告知用户预计完成时间
4. 如果使用了监控工具，让监控工具来传递结果
5. 在任务完成后禁用监控工具

**重要提示：** 从传入的元数据中设置 `<CHAT_ID>`。硬编码的聊天标识符仅作为本地示例使用，不应作为可重用的默认值。

### 5. 检查状态
读取 `data/state.json` 文件以获取状态信息。

## 设置

### 将用户名映射到 Steam ID
```bash
python3 scripts/leetify/leetify_save_id.py <USERNAME> <STEAM_64_ID>
```

### 配置 API 密钥
建议使用环境变量：
- `DEMOSLAP_API_KEY` - 必填
- `LEETIFY_API_KEY` - 可选，仅用于基于 Leetify 的比赛查找
- `DEMO_SLAP_watchDOG_JOB_ID` - 可选的部署辅助工具，用于监控脚本的运行

**来源选择规则：**
- 如果 `LEETIFY_API_KEY` 存在，使用 Leetify 来查找比赛记录。
- 如果 `LEETIFY_API_KEY` 不存在但 `DEMOSLAP_API_KEY` 存在，则使用 Demo-Slap 的 `/public-api/matches` 来查找比赛记录。
- `DEMOSLAP_API_KEY` 是进行分析/渲染操作的必备参数。

**针对受控的本地部署环境的可选设置：** 将相关配置放入 `data/config.json` 文件中。

## 支持

如需访问和支持，请加入我们的 Discord 社区：https://discord.gg/8nfh26W9wQ