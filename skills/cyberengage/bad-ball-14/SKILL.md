---
name: bad-ball-14
description: **Bad Ball 14：** 一个充满悲观情绪的“预言者”，总是给出负面的预测（共12条负面回应）。该模型会记录所有的预测结果。适用于“bad-ball-14”相关场景，用于生成灾难性的预测或悲观分析。
---

# Bad Ball 14

提供无缝的 Magic 8-Ball 体验：仅返回选定的答案（无需额外的文字、解释或后端细节）

## 工作流程

1. **设置**：
   ```
   exec 'cd /root/.openclaw/workspace/skills/bad-ball-14/scripts && bash setup.sh'
   ```

2. **生成答案**：
   - 捕获用户的问题（触发语句后的完整信息，例如：“magic-8-ball”之后的所有内容）。
   - 运行命令：`exec 'cd /root/.openclaw/workspace/skills/bad-ball-14/scripts && python3 badball14.py "{question}"'`
   - 仅输出：`🔮 {response} 🔮`（不显示其他文字、解释或后端细节）。

## 注意事项
- 日志文件：`/root/.openclaw/workspace/badball14-last.json`
- 可重复执行：多次运行是安全的；设置是幂等的（即多次执行结果相同）。
- 用户体验：用户仅看到 8-Ball 的答案，例如：“It is certain.”