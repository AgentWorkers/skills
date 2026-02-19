---
name: toggle
description: 使用此功能来了解用户在一天中的活动情况——每当用户询问自己的工作内容、任务、工作会话、工作效率或任何与时间相关的问题时，都应使用此功能。同时，当用户希望刷新、更新或回忆自己的工作内容时，也可以主动使用此功能。相关关键词包括：我做了什么、我在做什么、今天、昨天、我的一天、活动记录、会话记录、刷新数据、工作效率、时间跟踪等。
metadata:
  openclaw:
    requires:
      env:
        - TOGGLE_API_KEY
      bins:
        - python3
    primaryEnv: TOGGLE_API_KEY
    emoji: "📊"
    homepage: https://x.toggle.pro
---
# 切换（ToggleX）

从 ToggleX 获取原始的工作流程数据，并为用户提供汇总结果。**该脚本仅负责获取并打印原始的 JSON 数据**——所有自然语言的汇总工作均由代理使用这些数据完成，而非脚本本身。

## 端点

此技能会调用官方的 ToggleX OpenClaw 集成端点：

```
https://ai-x.toggle.pro/public-openclaw/workflows
```

`ai-x.toggle.pro` 由 ToggleX（https://x.toggle.pro）提供支持——该服务同时也负责运行仪表板和扩展程序。您的 `TOGGLE_API_KEY` 会作为 `x-openclaw-api-key` 头部字段发送。不会传输其他任何数据。

## 获取 API 密钥

请从 ToggleX OpenClaw 集成页面获取您的 `TOGGLE_API_KEY`：

```
https://x.toggle.pro/new/clawbot-integration
```

切勿将密钥粘贴到聊天中。请将其设置到 OpenClaw 的配置文件中：

```json
{
  "skills": {
    "entries": {
      "toggle": {
        "apiKey": "your_key_here"
      }
    }
  }
}
```

或者您也可以在 shell 中导出该密钥：

```bash
export TOGGLE_API_KEY=your_key_here
```

## 运行脚本

```bash
python3 {baseDir}/scripts/toggle.py
```

运行此脚本需要满足以下条件：系统中已安装 `python3`，并且 `TOGGLE_API_KEY` 已被设置到环境变量中。

### 时间范围

```bash
python3 {baseDir}/scripts/toggle.py --from-date 2026-02-17 --to-date 2026-02-19
```

如果未指定时间范围，系统将默认使用当前日期。

## 解释输出结果

脚本返回的是原始的 JSON 数据。作为代理，您需要执行以下操作来进行数据解析和汇总：
- 重点关注类型为 `WORK` 的记录；除非有特别要求，否则跳过 `BREAK` 类型的记录；
- 如果存在 `LEISURE` 类型的记录，请简要提及；
- 使用 `workflowType` 和 `workflowDescription` 来描述每个工作流程；
- 如果记录中包含 `projectTask`，请一并显示 `projectTask.name` 和 `project.name` 以提供上下文信息；
- 根据 `productivityScore`（0–100 分）来评估工作流程的效率：90 分及以上表示高效，70–89 分表示中等效率，70 分以下表示效率较低；
- 提供一个简短的总结：包括总工作时间、主要的工作重点以及值得注意的工作模式；
- 如果 `totalWorkflows` 的值为 0，说明在该时间段内 Toggle 未运行或未捕获到任何数据。