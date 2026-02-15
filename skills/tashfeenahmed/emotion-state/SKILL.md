---
name: emotion-state
description: 通过 OpenClaw 挂钩实现 NL 情感追踪及提示信息注入
---
# 情绪状态（自然语言）技能

本技能介绍了如何安装和配置“情绪状态”钩子，该钩子会在系统提示中添加一个简洁的 `emotion_state` 块。

## 功能介绍

- 将用户和代理的情绪以简短的自然语言短语的形式进行评估。
- 将用户的情绪状态在会话之间保存在代理的状态目录中。
- 将最新的情绪状态数据以及其变化趋势线显示在系统提示中。

## 安装与启用（工作区钩子）

1) 安装该技能后，将捆绑的钩子文件复制到您的工作区：

```bash
cp -R ./skills/emotion-state/hooks/emotion-state ./hooks/
```

2) 在 OpenClaw 中启用该钩子：

```bash
openclaw hooks enable emotion-state
```

3) 重启 OpenClaw 网关。

## 配置

通过 OpenClaw 的配置文件（例如 `~/.openclaw/openclaw.json`）设置钩子的相关环境变量：

```json
{
  "hooks": {
    "internal": {
      "enabled": true,
      "entries": {
        "emotion-state": {
          "enabled": true,
          "env": {
            "EMOTION_CLASSIFIER_URL": "",
            "OPENAI_API_KEY": "YOUR_KEY",
            "OPENAI_BASE_URL": "https://api.openai.com/v1",
            "EMOTION_MODEL": "gpt-4o-mini",
            "EMOTION_CONFIDENCE_MIN": "0.35",
            "EMOTION_HISTORY_SIZE": "100",
            "EMOTION_HALF_LIFE_HOURS": "12",
            "EMOTION_TREND_WINDOW_HOURS": "24",
            "EMOTION_MAX_USER_ENTRIES": "3",
            "EMOTION_MAX_AGENT_ENTRIES": "2",
            "EMOTION_MAX_OTHER_AGENTS": "3",
            "EMOTION_TIMEZONE": "America/Los_Angeles"
          }
        }
      }
    }
  }
}
```

## 注意事项

- 该钩子将情绪状态数据保存在 `~/.openclaw/agents/<agentId>/agent/emotion-state.json` 文件中。
- 它不存储用户的原始文本，仅保存模型推断出的情绪原因。
- 如果分类器出现故障，情绪状态将默认显示为 `neutral/low/unsure`。