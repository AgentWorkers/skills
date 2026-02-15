---
name: magic-8-ball
description: **Magic 8-Ball 算命工具：**  
该工具会从 20 个经典回答中随机选择一个，并记录下结果（包括用户提出的问题以及 UTC 时间戳）。每当用户向 Magic 8-Ball 提出问题、需要获得“是/否”的预测结果，或者说出“8 ball”/“magic ball”等指令时，都可以使用该工具。
---

# 魔法8球（Magic 8 Ball）

为您提供一个无缝的魔法8球体验：仅返回选定的答案（无需额外的文字、解释或后端细节）。

## 工作流程

1. **设置**：
   ```
   exec 'cd /root/.openclaw/workspace/skills/magic-8-ball/scripts && bash setup.sh'
   ```

2. **生成答案**：
   - 捕获用户的问题（触发语句之后的完整信息，例如：“magic-8-ball”之后的所有内容）。
   - 运行命令：`exec 'cd /root/.openclaw/workspace/skills/magic-8-ball/scripts && python3 magic8ball.py "{question}"'`
   - 仅输出：`🔮 {response} 🔮`（不显示其他文字、解释或后端细节）。

## 注意事项
- 日志文件：`/root/.openclaw/workspace/magic8ball-last.json`
- 可重复执行：多次运行是安全的；设置过程是幂等的（即多次执行不会产生不同的结果）。
- 用户界面：用户只能看到魔法8球的答案，例如：“It is certain.”（答案是肯定的。）