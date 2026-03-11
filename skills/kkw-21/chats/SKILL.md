# Echo Chat

这是一个基于用户记忆的对话式人工智能系统。它能够理解并回应你的需求，通过与植根于你个人记忆中的“代理”进行交流来实现这一点。其回应内容具有上下文相关性，能够感知用户的情感，并引用真实的经历。Echo的核心对话引擎正是实现这一功能的基石。

## 使用方法

```bash
echo-chat start <user-id>          # Start memory-grounded conversation
echo-chat peer <id-a> <id-b>       # Facilitate peer-to-peer memory chat
echo-chat export <thread-id>       # Export conversation with memory refs
```

## 主要功能

- 基于用户记忆的回应，会提供相应的证据支持
- 能够感知用户情绪并调整对话语气
- 支持用户之间的消息传递，并共享彼此的记忆信息
- 支持语音和文本两种交流方式
- 支持跨平台记忆数据的整合（例如与 ChatGPT、Gemini 等平台的数据交互）