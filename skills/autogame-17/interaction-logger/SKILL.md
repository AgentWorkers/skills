# 交互日志记录器（Interaction Logger）

这是一个功能强大的工具，用于将交互日志追加到用户特定的历史文件中。它简化了 JSON 解析、文件 I/O 操作以及数据结构验证的复杂性。

## 工具使用方法

直接调用 `interaction_logger` 工具：

```json
{
  "action": "log",
  "target": "zhy",
  "role": "assistant",
  "content": "Hello world"
}
```

```json
{
  "action": "sync"
}
```

## 命令行界面（CLI）使用方法（旧版本）

```bash
node skills/interaction-logger/index.js --action log --target <target_alias> --role <role> --content <message>
```

## 参数

- `--action`：`log` 或 `sync`  
- `--target`：用户别名。  
  - `zhy`、`shiqi`、`master` → `memory/master_history.json`  
  - `fmw`、`big-brother` → `fmw/history.json`  
- `--role`：说话者角色（`user` | `assistant` | `system`）。默认值：`assistant`。  
- `--content`：要记录的文本内容。

## 为什么使用这个工具？

- **安全性**：避免因手动编辑 JSON 代码而导致的语法错误。  
- **便捷性**：只需一条命令即可完成日志的记录、读取或写入操作，无需多步骤操作。  
- **合规性**：确保遵循了 `MEMORY.md` 中规定的日志记录规则。

## 主要特性：
- **原子性写入**：通过使用临时文件（`.tmp`）并重命名来防止系统崩溃时数据损坏。  
- **日志轮换**：当日志文件大小超过 5MB 时，会自动将其旋转为 `filename_YYYY-MM-DD-HHmmss.json` 格式。  
- **动态目标路径**：为新用户自动生成日志文件，存储在 `memory/users/` 目录下。  
- **自动同步**：会自动将会话日志同步到历史文件中。