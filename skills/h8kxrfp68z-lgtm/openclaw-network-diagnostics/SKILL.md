---
name: openclaw-network-diagnostics
description: OpenClaw 提供了独立的高级网络诊断工具，用于持续检测从 OpenClaw 代理到 Telegram Bot API 的端到端连接情况，以及数据传输到个人 Telegram 客户端的过程。该工具适用于排查以下问题：延迟突然增加、数据包丢失、网络流量限制/阻断、DNS 服务不稳定、TLS/TCP 协议故障、路由变化、最大传输单元（MTU）调整、重试/超时机制问题，以及 Telegram 的速率限制。诊断过程中会生成结构化的 JSON 日志文件。
---
# OpenClaw 网络诊断工具

## 概述

通过命令行（CLI）运行一个专门用于网络诊断的进程，持续监控以下组件之间的连接状态：
1. OpenClaw 运行时主机
2. Telegram 机器人 API (`apiTelegram.org`)
3. 通过发送验证机制来模拟个人 Telegram 客户端的通信过程

确保网络诊断功能与 OpenClaw 的大型语言模型（LLM）流程相互独立：
- 不使用任何 LLM 相关的调用。
- 不消耗任何 AI 令牌。
- 以独立的异步线程形式运行。

## 相关技能文件

- `scripts/netdiag.py`：独立的 CLI 工具（支持 `run`、`start`、`stop`、`status` 和 `validate-config` 操作）
- `references/config.example.json`：完整的配置示例文件
- `references/example-log-entries.jsonl`：结构化的 JSON 日志样本
- `references/openclaw-integration.md`：集成方案（包含优缺点）
- `references/ai-log-analysis.md`：基于 AI 的日志分析工作流程

## 先决条件

请确保已安装并验证以下软件：
1. Python 3.11 及更高版本
2. macOS 系统的网络诊断工具：`dig`、`ping`、`traceroute`
3. Telegram 机器人的访问令牌以及个人聊天 ID

## 安装方法

从技能目录（skill root）开始安装：

```bash
cd /Users/ivanbelugin/Documents/Connection\ Monitoring\ System/openclaw-network-diagnostics
python3 scripts/netdiag.py validate-config --config references/config.example.json
```

根据示例文件创建实际的配置文件，并填写真实的凭据：

```bash
cp references/config.example.json config.json
```

接下来编辑 `config.json` 文件，设置以下参数：
- `telegram_bot_token`：Telegram 机器人的访问令牌
- `telegram.personal_chat_id`：个人 Telegram 账号的 ID

## 运行网络诊断工具

### 前台模式（可通过 Ctrl+C 手动停止）

```bash
python3 scripts/netdiag.py run --config config.json --pid-file ./logs/netdiag.pid
```

**运行方式：**
- 通过 CLI 手动启动。
- 持续运行，直到手动停止。
- 停止时将诊断结果以 JSON 格式输出到标准输出（stdout）。
- 将诊断结果保存到 `logging.summary_file_path` 文件中。

### 后台模式（非阻塞服务）

```bash
python3 scripts/netdiag.py start --config config.json --pid-file ./logs/netdiag.pid
python3 scripts/netdiag.py status --pid-file ./logs/netdiag.pid
python3 scripts/netdiag.py stop --pid-file ./logs/netdiag.pid
```

此模式可避免阻塞 OpenClaw 的主线程。

## 监控机制

每隔 `intervals_sec.ping` 秒（默认值为 30 秒）执行一次网络诊断任务：
1. 使用系统默认的 DNS 解析器及公共 DNS 服务器解析域名。
2. 向 Telegram 机器人 API 发送请求（`getMe`），并测量往返延迟。
3. 执行消息发送验证流程（`sendMessage`）并记录确认结果。
4. 发送 `ping` 请求以检测数据包丢失情况，并记录相关指标。
5. 更新网络中断、恢复情况以及异常事件的计数。

**额外的定期诊断任务：**
- 使用 `traceroute` 命令检查网络路径（`intervals_sec.traceroute`）。
- 通过二分查找法检测最大传输单元（MTU）（`intervals_sec.mtu_test`）。
- 定期重新解析 DNS（`intervals_sec.dns_reresolve`）。

## 消息发送验证方式

可以选择以下三种验证模式之一：
- `bot_api_ack`（默认值）：仅确认机器人 API 是否成功接收了消息。
- `user_reply_ack`：等待用户通过 `getUpdates` 回复，以更准确地判断消息是否到达客户端并触发用户交互。
- `callback_ack`：发送一个内嵌的按钮链接，并等待用户的点击确认。

**注意：**  
Telegram 机器人 API 并不提供直接的消息接收确认机制。因此，`user_reply_ack` 和 `callback_ack` 是实际应用中常用的替代方案。

## 推荐的配置参数

- `timeouts_ms.connect`：连接超时时间（4000 毫秒）
- `timeouts_ms.request`：请求超时时间（10000 毫秒）
- `retry.max_retries`：最大重试次数（2 次）
- `retry.backoff_base_ms`：重试间隔时间（500 毫秒）
- `diagnostics.latency_anomaly_threshold_ms`：异常延迟阈值（1200 毫秒）

**设置理由：**
- 可及时发现短暂性的网络故障，同时不会忽略持续性的网络中断。
- 在限制请求频率或速率限制的情况下，有助于防止重试请求过多导致的系统负担。

## 日志记录机制

所有诊断日志都会以 JSON 格式写入旋转式的日志文件中，系统会对日志文件的大小进行限制：
- 单个文件的最大容量：`logging.max_file_size_mb`
- 所有日志文件的总容量上限：`logging.max_total_size_mb`（可根据需求设置为 500 MB）

**敏感数据处理：**
- 可通过 `logging.redact_sensitive_fields` 配置选项来决定是否屏蔽日志中的敏感信息。

## OpenClaw 集成方式

### 方案 A：外部进程（推荐）

使用 OpenClaw 的任务钩子（task hooks）来控制 `start`、`stop` 和 `status` 操作：
- 与 OpenClaw 运行时环境强隔离。
- 设计上为非阻塞模式，便于独立重启和故障处理。
- 需要管理进程 ID（pid 文件）的生命周期。

### 方案 B：在 OpenClaw 内部运行

将诊断工具作为进程集成到 OpenClaw 的主循环中：
- 适用于单进程部署场景。
- 但可能导致 OpenClaw 主线程出现故障。
- 对于需要大量网络请求的诊断任务，隔离效果较差。

在生产环境中，建议默认使用方案 A。

## 停止与日志汇总

当手动停止诊断工具时（通过发送 `SIGINT` 或 `SIGTERM` 信号），工具会执行以下操作：
1. 将最终的诊断数据刷新到内存。
2. 将诊断结果以 JSON 格式输出到标准输出。
3. 将结果保存到 `logging.summary_file_path` 文件中。

**日志汇总内容包括：**
- 总运行时间
- 总共发送的 ping 请求次数
- 失败的 ping 请求次数
- 平均延迟
- 最大延迟
- 发生连接中断的次数
- DNS 解析结果的变化
- 最大传输单元（MTU）的变化
- 异常事件的统计信息

## 使用 AI 工具分析日志

请参考 `references/ai-log-analysis.md` 文档，了解如何使用 AI 工具对日志进行深入分析：
1. 从 `logs/netdiag.jsonl` 文件中提取所需的数据片段。
2. 在本地计算相关统计指标。
3. 将这些数据以及日志摘要通过结构化的提示输入到 ChatGPT Codex 中。
4. 提出关于事件时间线、根本原因、异常模式以及配置优化建议的请求。