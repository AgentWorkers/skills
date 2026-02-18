# Feishu 会议助手

该工具会扫描您的 Feishu 日历中即将举行的事件（这些事件可能附带文档，如 Doc、Sheet 或 Bitable），读取文档内容，并为用户生成一份简明的会议概要卡片。

## 使用方法

```bash
# Check upcoming meetings (next 24h) and generate briefings
node skills/feishu-meeting-assistant/check.js
```

## 主要功能
- 检测未来 24 小时内的会议。
- 解析会议描述中的 Feishu Doc/Sheet/Bitable 链接。
- 使用 `feishu-doc` 工具获取文档内容。
- 生成包含会议关键信息的简明概要卡片。
- 通过 `feishu-card` 将概要卡片发送给用户。

## 配置要求
- 需要安装并配置 `feishu-calendar` 和 `feishu-doc` 两个插件。