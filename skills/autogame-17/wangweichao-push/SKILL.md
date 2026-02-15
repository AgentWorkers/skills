# 王伟超每日推送技能

这是一个为用户 `ou_cea17106dcef3d45a73387d049bf2ebe` 提供的自动化知识传播服务，遵循 `memory/protocols/wangweichao_push_protocol.md` 中定义的协议。

## 功能特点
- **自动生成内容**：利用大型语言模型（LLM）生成每日的三个主题（人文、科技、游戏设计相关内容）。
- **丰富的格式化效果**：发送结构化格式的 Feishu 帖子。
- **内容跟踪**：记录每日推送的内容，避免重复推送。

## 使用方法
```bash
node skills/wangweichao-push/push.js --force
```

## 依赖项
- `feishu-post`（用于发送格式化的文本）
- `memory/protocols/wangweichao_push_protocol.md`（协议规范）