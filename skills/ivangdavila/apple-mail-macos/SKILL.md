---
name: Apple Mail (MacOS)
slug: apple-mail-macos
version: 1.0.0
homepage: https://clawic.com/skills/apple-mail-macos
description: 在 macOS 上，可以使用本地的命令行工具（CLI）来管理已同步到 Apple Mail 中的 Gmail、Outlook、iCloud、Yahoo、Fastmail 等邮件账户，而无需使用任何 API 或 OAuth。
changelog: Initial release with deterministic Apple Mail command paths, provider-aware operations, and safety gates for send and delete actions.
metadata: {"clawdbot":{"emoji":"✉️","requires":{"bins":[],"anyBins":["osascript","shortcuts","sqlite3"],"config":["~/apple-mail-macos/"]},"os":["darwin"],"configPaths":["~/apple-mail-macos/"]}}
---
## 设置

首次使用时，请按照 `setup.md` 的说明来定义提供者范围（provider scope）、命令路径偏好设置（command path preferences）以及安全默认值（safety defaults），然后再执行任何写入操作。

## 使用场景

用户希望通过命令行（CLI）来控制 Apple Mail，同时让 Mail.app 负责账户同步。该工具会处理已连接到 Apple Mail 的各个账户中的读、搜索、分类、草稿创建、发送、移动、归档和删除等操作。

## 系统要求

- 安装了 macOS 并启用了 Mail.app 账户访问功能，以便进行终端自动化操作。
- 至少需要一个可用的命令路径：`osascript`、`shortcuts` 或 `sqlite3`（用于只读索引查询）。
- 用户的提供者账户（如 Gmail、Outlook、iCloud、Yahoo、Fastmail 或通过 Bridge 连接的 Proton）已成功连接到 Mail.app。
- 在执行发送、删除或批量操作之前，必须获得用户的明确确认。

## 架构

所有数据存储在 `~/apple-mail-macos/` 目录下。具体存储结构请参考 `memory-template.md`。

```text
~/apple-mail-macos/
├── memory.md               # Status, provider map, safety defaults
├── command-paths.md        # Working command path and fallback notes
├── provider-coverage.md    # Provider-specific behavior and caveats
├── safety-log.md           # Send/delete confirmations and rollback notes
└── operation-log.md        # Operation IDs, verification evidence, outcomes
```

## 快速参考

| 主题          | 文件            |
|----------------|-----------------|
| 设置与首次运行行为    | `setup.md`         |
| 内存结构        | `memory-template.md`      |
| 命令层级与执行路径    | `command-paths.md`      |
| 提供者行为矩阵    | `provider-coverage.md`     |
| 写入操作前的安全检查    | `safety-checklist.md`     |
| 确定性操作模式      | `operation-patterns.md`     |
| 故障处理与恢复      | `troubleshooting.md`     |

## 数据存储

所有相关文件均存储在 `~/apple-mail-macos/` 目录下。在创建或修改本地文件之前，请先描述预期的写入操作并获取用户的确认。

## 核心规则

### 1. 将 Mail.app 视为统一的账户管理层

- 假设用户已配置好提供者账户的同步功能，并在此基础上进行操作。
- 除非用户明确请求设置帮助，否则不要尝试直接与提供者进行 OAuth 验证。

### 2. 每次操作前检测命令路径

- 按照以下顺序检测命令路径：`osascript`、`shortcuts`、`sqlite3`（仅用于只读索引查询）。
- 如果没有安全的命令路径可用，立即停止操作并报告具体问题，切勿猜测原因。

### 3. 对写入操作进行模拟测试

- 对于草稿创建、回复、移动、归档和删除等操作，先生成包含受影响消息和字段的模拟预览结果。
- 在用户确认模拟结果之前，切勿执行实际修改。

### 4. 强制执行高风险操作前的确认流程

- 对发送、删除、批量移动、批量归档、转发和全部回复等操作，必须获得用户的明确确认。
- 如果添加了外部收件人或收件人数量发生变化，需要再次确认。

### 5. 使用操作 ID 保证操作的可重复性

- 为每个写入操作生成唯一的操作 ID，并将其记录在本地操作日志中。
- 在发送之前，验证是否之前没有使用相同的操作 ID 发送过邮件。

### 6. 先读取数据，再写入，立即验证结果

- 在执行任何写入操作之前，必须通过至少两个字段（消息 ID 或发送者信息、日期）来确认消息的真实性。
- 每次写入操作后，都要进行数据读取验证，并报告最终的邮箱状态。

### 7. 最小化数据暴露范围，优先使用本地数据

- 仅使用任务所需的字段，避免不必要的数据导出。
- 绝不要将邮件正文或附件发送到未指定的外部端点。

## 常见错误

- 在未审核最终收件人的情况下直接发送邮件 -> 导致发送错误。
- 仅根据主题匹配邮件线程 -> 导致回复发送到错误的对话框中。
- 未进行模拟测试就执行批量归档或删除操作 -> 造成数据丢失。
- 假设提供者的文件夹名称完全相同 -> 导致文件移动失败或邮件丢失。
- 跳过数据读取验证 -> 造成错误的操作完成报告。

## 安全性与隐私

**仅存储在本地的数据：**
- 操作上下文和相关默认设置（存储在 `~/apple-mail-macos/`）。
- 执行任务所需的消息元数据。

**可能离开用户设备的数据：**
- 仅当用户确认发送、回复或转发操作后，才会发送邮件内容。

**本工具不会：**
- 在未经用户明确确认的情况下发送邮件。
- 在未进行模拟测试和确认的情况下执行可能破坏邮箱数据的操作。
- 请求未指定的 API 密钥或调用未知的第三方 API。

## 相关工具

用户可以通过 `clawhub install <slug>` 安装以下相关工具：
- `macos`：适用于 macOS 的命令行工作流程和系统自动化工具。
- `mail`：跨平台的邮箱处理方法和协议参考。
- `events`：从通信中提取事件信息并构建操作项。
- `schedule`：用于调度与邮件相关的任务。
- `productivity`：用于日常工作的执行和优先级管理工具。

## 反馈

- 如果本工具对您有帮助，请给它打星（`clawhub star apple-mail-macos`）。
- 要保持工具的最新状态，请使用 `clawhub sync` 功能。