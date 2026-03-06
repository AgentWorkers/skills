---
name: session-rotate-80
description: 当 OpenClaw 的上下文使用率达到 80% 时，自动创建一个新的会话，而无需依赖 Mem0 或文件内存系统。此功能适用于希望 OpenClaw 自动轮换会话的用户，以防止在长时间聊天过程中出现上下文溢出的情况。
---
# 会话轮换（Session Rotate 80）

## 概述
当上下文的使用率达到80%时，触发标准的`[NEW_SESSION]`消息。  
此功能与内存系统无关，适用于普通的OpenClaw配置。

## 工作流程
1. 从运行时状态中读取当前的上下文使用情况。
2. 运行`scripts/context_guard.py <used_tokens> <max_tokens>`命令。
3. 如果达到阈值，输出新会话的触发信息及切换提示。
4. 仅保留旧会话以用于短暂的任务交接，然后在新会话中继续执行任务。

## 命令
```bash
python scripts/context_guard.py <used_tokens> <max_tokens> --threshold 0.8 --channel boss
```

## 示例
```bash
python scripts/context_guard.py 220000 272000 --threshold 0.8 --channel boss
```

## 预期输出
当达到或超过阈值时：
- `[ROTATE_NEEDED]`
- `[NEW_SESSION] 上下文使用率达到80%（used/max），系统将自动切换到新会话`
- `[HANDOFF_HINT] ...`

当低于阈值时：
- `[ROTATE_NOT_NEEDED] 使用率=x.xx < 0.800`

## 集成提示（Heartbeat机制）
在Heartbeat机制中，读取上下文使用情况后：
1. 调用`context_guard.py`。
2. 如果需要轮换会话（`[ROTATE_NEEDED]`），直接输出`[NEW_SESSION]...`。
3. 停止在旧会话中处理新任务，仅完成交接确认。

## 相关脚本
- `scripts/context_guard.py`：用于检测阈值并触发会话轮换的脚本（不依赖内存）。