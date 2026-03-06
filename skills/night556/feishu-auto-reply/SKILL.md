---
name: feishu-auto-reply
description: Feishu自动回复机器人 - 根据预设规则自动回复Feishu上的消息
metadata:
  openclaw:
    requires:
      bins: []
---
# Feishu 自动回复机器人

根据自定义规则自动回复 Feishu 消息，具备以下功能：
- 支持关键词匹配
- 支持正则表达式匹配
- 多种回复策略
- 仅支持对 @mention 的回复
- 可配置工作时间
- 提供自定义回复模板
- 支持发送富文本消息

## 使用方法

```bash
# Start auto reply service
openclaw feishu-auto-reply start --config ./config.yaml

# Test rule matching
openclaw feishu-auto-reply test --message "你好" --config ./config.yaml
```

## 配置示例（config.yaml）
```yaml
rules:
  - keyword: "你好"
    reply: "你好！我是自动回复机器人，有什么可以帮你的？"
    match: contains
  - regex: "^(请假|休假)"
    reply: "请假请直接联系人事部门，谢谢！"
    only_mention: true
working_hours:
  - "9:00-18:00"
  - exclude_weekends: true
```

## 所需权限
- `im:message:read`
- `im:message:send`
- `im:chat:read`