---
name: memory-analyzer
version: 1.0.0
description: 分析对话历史记录，提取用户偏好和反馈信息，并自动更新内存文件。
homepage: https://clawhub.com/skills/memory-analyzer
metadata: {"openclaw":{"emoji":"🧠","category":"system","keywords":["memory","analysis","learning","automation"],"model":"google/gemini-3-flash-preview"}}
---

# 内存分析器技能

该工具可自动分析对话历史并更新相关内存文件。

## 使用方法

**默认设置：Google Gemini 3 Flash Preview**

```
Run memory-analyzer skill with Google model
```

或者手动操作：

```
Run /home/ubuntu/.openclaw/workspace/skills/memory-analyzer/analyzer.py with google/gemini-3-flash-preview model
```

## 功能介绍

1. **从会话中读取**对话历史记录。
2. **提取**用户的偏好设置和反馈模式。
3. **更新**以下内存文件：
   - MEMORY.md（长期存储的用户数据）
   - AGENTS.md（代理规则）
   - USER.md（用户偏好设置）
   - IDENTITY.md（身份信息）
   - SOUL.md（用户个性特征）

## 触发条件

当用户说出以下内容时，该工具会自动执行更新：
- “你应该这样做”
- “我更喜欢这种工作方式”
- “我喜欢/不喜欢这种格式”
- 任何直接的反馈或偏好表达

## 输出结果

系统会根据新的信息自动更新相关内存文件。

## 默认模型

**google/gemini-3-flash-preview**（由Tevfik配置）