---
name: governance.wrapper
description: **强制性的严格模式执行包装器**：用于自主操作，具备证据记录（证据日志记录）和策略执行功能。
---
所有在严格模式下的自主操作都必须通过以下脚本执行：

```
python3 /home/openclaw/.openclaw/workspace/governance/governance_wrapper.py
```

所需参数：

- `--requested-skill`：请求的技能
- `--system-prompt`：系统提示信息
- `--input-context`：输入上下文

该脚本在严格模式下执行的控制措施包括：

- 模型锁定（使用 `opencode/big-pickle` 方法，无备用方案，温度限制为 0.0）
- 从工具界面清单中强制执行技能允许列表
- 对出站 HTTP 请求强制执行网络允许列表
- 限制子代理的并发数量（使用 `maxConcurrentSubagents` 参数）
- 强制生成 `execution-evidence.v1` 格式的执行证据
- 使用哈希链技术进行只读的日志记录

任何违反政策的行为都会导致执行被阻止，并会记录相应的证据。