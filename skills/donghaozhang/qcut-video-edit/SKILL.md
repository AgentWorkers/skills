---
name: native-cli
description: 运行 QCut 的原生 TypeScript 命令行界面（CLI），用于 AI 内容生成、视频分析、文字转录、YAML 流程处理、ViMax 视频制作以及项目管理。此外，该 CLI 还可用于编辑器的 HTTP 自动化任务（如状态快照、事件处理、事务管理以及通知桥接控制），尤其是在用户需要具备确定性状态感知控制功能时。
---
# 原生管道命令行工具（Native Pipeline CLI）

运行 QCut 内置的 TypeScript 管道命令行工具（`qcut-pipeline` 或 `bun run pipeline`）。

## 额外资源

- 有关独立的命令行工具（生成、分析、转录、管道处理、ViMax、项目管理、API 密钥等功能），请参阅 [REFERENCE.md](REFERENCE.md)。
- 有关编辑器相关命令（媒体处理、项目管理、时间轴操作、编辑功能、导出、诊断工具、MCP 等），请参阅 [editor-core.md](editor-core.md)。
- 有关编辑器 AI 功能（视频分析、转录、AI 生成、Remotion 插件等），请参阅 [editor-ai.md](editor-ai.md)。
- 有关编辑器状态自动化（快照、事件流、关联 ID、事务处理、功能及通知机制等），请参阅 [editor-state-control.md](editor-state-control.md)。

## 第一步：确保 QCut 正在运行

在执行任何 `editor:*` 命令之前，请先检查 QCut 是否正在运行。如果未运行，请先构建并启动 QCut。

```bash
# Check if QCut is running
curl -s --connect-timeout 2 http://127.0.0.1:8765/api/claude/health || echo "NOT_RUNNING"
```

如果 QCut 未运行：

```bash
bun run build                # Build first
bun run electron &           # Launch in background
sleep 5                      # Wait for startup
```

## 第二步：查找项目、媒体文件及时间轴数据

大多数编辑器命令需要 `--project-id`、`--media-id` 或 `--element-id` 参数。运行相应的命令来获取这些信息。

```bash
# 1. List projects → get project-id
bun run pipeline editor:navigator:projects

# 2. Open a project (navigates the editor)
bun run pipeline editor:navigator:open --project-id <project-id>

# 3. List media → get media-id values
bun run pipeline editor:media:list --project-id <project-id> --json

# 4. Export timeline → get track-id and element-id values
bun run pipeline editor:timeline:export --project-id <project-id> --json
```

现在你已经获得了执行其他所有编辑器命令所需的 ID。

## 使用方法

```bash
bun run pipeline <command> [options]            # Dev (recommended)
bun run electron/native-pipeline/cli/cli.ts <command> [options]  # Direct source
qcut-pipeline <command> [options]               # Production binary
```

## 快速命令

```bash
bun run pipeline list-models                          # List all models
bun run pipeline generate-image -t "A cinematic portrait at golden hour"
bun run pipeline create-video -m kling_2_6_pro -t "Ocean waves at sunset" -d 5s
bun run pipeline generate-avatar -m omnihuman_v1_5 -t "Hello world" --image-url avatar.png
bun run pipeline analyze-video -i video.mp4 --analysis-type summary
bun run pipeline transcribe -i audio.mp3 --srt
bun run pipeline run-pipeline -c pipeline.yaml -i "A sunset" --no-confirm
bun run pipeline estimate-cost -m veo3 -d 8s
```

## ViMax 快速入门

```bash
bun run pipeline vimax:idea2video --idea "A detective in 1920s Paris" -d 120
bun run pipeline vimax:script2video --script script.json --portraits registry.json
bun run pipeline vimax:novel2movie --novel book.txt --max-scenes 20
```

## API 密钥设置

API 密钥存储在 `~/.qcut/.env` 文件中（文件权限设置为 `0600`）。

```bash
bun run pipeline setup          # Create .env template
bun run pipeline set-key --name FAL_KEY   # Set a key (interactive)
bun run pipeline check-keys     # Check configured keys
```

**支持的密钥：** `FAL_KEY`、`GEMINI_API_KEY`、`GOOGLE.AI_API_KEY`、`OPENROUTER_API_KEY`、`ELEVENLABS_API_KEY`、`OPENAI_API_KEY`、`RUNWAY_API_KEY`、`HEYGEN_API_KEY`、`DID_API_KEY`、`SYNTHESIA_API_KEY`

## 全局选项

| 选项 | 简写 | 说明 |
|------|-------|-------------|
| `--output-dir` | `-o` | 输出目录（默认：`./output`） |
| `--model` | `-m` | 使用的模型 |
| `--json` | | 以 JSON 格式输出结果 |
| `--quiet` | `-q` | 抑制进度提示 |
| `--verbose` | `-v` | 显示详细日志 |
| `--stream` | | 将进度信息以 JSONL 格式输出到标准错误流（stderr） |
| `--help` | `-h` | 显示帮助信息 |

## 相关源文件

| 组件 | 文件路径 |
|-----------|------|
| 命令行工具入口点 | `electron/native-pipeline/cli/cli.ts` |
| 命令路由处理逻辑 | `electron/native-pipeline/cli/cli-runner/runner.ts` |
| 编辑器相关处理逻辑 | `electron/native-pipeline/cli/cli-handlers-editor.ts` |
| 管理员相关处理逻辑 | `electron/native-pipeline/cli/cli-handlers-admin.ts` |
| 媒体处理逻辑 | `electron/native-pipeline/cli/cli-handlers-media.ts` |
| ViMax 处理逻辑 | `electron/native-pipeline/cli/vimax-cli-handlers.ts` |
| Remotion 插件处理逻辑 | `electron/native-pipeline/cli/cli-handlers-remotion.ts` |
| Moyin 插件处理逻辑 | `electron/native-pipeline/cli/cli-handlers-moyin.ts` |
| 密钥管理逻辑 | `electron/native-pipeline/key-manager.ts` |