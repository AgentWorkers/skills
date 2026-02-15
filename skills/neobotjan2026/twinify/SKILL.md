---
name: doppel
description: |
  Create AI digital twins of real people from WhatsApp chat history exports.
  Clone your friends, colleagues, or contacts into AI agents that talk, think, and react like them.
  Use when the user wants to: create a digital twin, clone a WhatsApp contact into an AI agent,
  build a persona from chat history, make an AI version of someone, create a doppelgänger agent,
  or simulate a conversation with someone based on their real messages.
  Triggers: digital twin, clone friend, chat clone, persona, doppelgänger, twin agent,
  AI clone, simulate person, WhatsApp clone, chat personality, mimic friend.
  Important: Requires explicit consent from the person being cloned. Always confirm permission before proceeding.
---

# Doppel — 基于聊天记录的AI数字孪生体

通过分析用户的WhatsApp聊天记录，可以创建出逼真的AI数字孪生体。

## ⚠️ 道德与同意

**必须获得用户的明确同意。** 在创建任何人的数字孪生体之前，**必须**获得他们的明确、知情的同意。具体步骤如下：

1. **告知**用户：他们的聊天记录将被用于创建一个模仿其个性和沟通风格的AI代理。
2. **解释**数字孪生体的用途（个人使用、娱乐、测试等）。
3. **获得明确许可**——无论是口头还是书面形式。
4. **尊重用户的拒绝**。如果用户拒绝，切勿创建数字孪生体。
5. **允许用户随时撤回许可**。用户可以随时请求删除数字孪生体。

未经用户知情或同意就创建数字孪生体，属于侵犯其隐私和自主权的行为。此功能仅适用于彼此同意参与的朋友、家人或同事之间，**不得**用于模仿、欺骗、骚扰或任何可能伤害用户的行为。

**在创建数字孪生体之前，系统必须确认用户的同意。** 当用户请求创建数字孪生体时，应询问：“您是否允许我们使用这些聊天记录来创建一个AI数字孪生体？” 除非用户明确同意，否则不得继续操作。

## 工作原理

1. 用户提供WhatsApp聊天记录的导出文件（`.txt`格式）。
2. 解析脚本提取并按发送者对聊天记录进行分类。
3. 大语言模型（LLM）分析这些分类后的聊天记录，生成用户的个性档案文件。
4. 使用这些档案创建一个新的OpenClaw代理。

## 快速入门

### 第一步：获取聊天记录导出文件

请用户从WhatsApp中导出聊天记录：
- 打开聊天记录 → ⋮ → 更多 → 导出聊天记录 → 不包含媒体文件
- 将生成的`.txt`或`.zip`文件发送过来。

### 第二步：解析聊天记录

运行解析脚本以提取聊天记录：

```bash
python3 scripts/parse_chat.py <chat_export.txt> <target_name> <output_dir>
```

参数：
- `chat_export.txt` — WhatsApp聊天记录导出文件的路径
- `target_name` — 要克隆的用户的名称（在聊天记录中的显示名称）
- `output_dir` — 用于保存解析后数据的目录

解析完成后，`<output_dir>`目录下会生成`parsed_messages.json`文件，其中包含分类后的聊天记录。

### 第三步：生成数字孪生体档案

使用解析后的聊天记录，在数字孪生体的工作空间中生成以下文件：
- `SOUL.md` — 参考文档：`references/soul-guide.md`
- `EXAMPLES.md` — 参考文档：`references/examples-guide.md`
- `ANTI-EXAMPLES.md` — 参考文档：`references/anti-examples-guide.md`
- `MEMORY.md` — 参考文档：`references/memory-guide.md`

请仔细分析这些聊天记录。文件的质量取决于以下几点：
- 识别所有重复出现的短语、俚语和表达方式
- 捕捉情感模式和语气变化
- 分析与聊天对象之间的关系动态
- 提取真实的事件、人物和共同经历

### 第四步：创建AI代理

1. 创建工作空间：`~/.openclaw/workspace-<agent_id>/`
2. 创建代理目录：`~/.openclaw/agents/<agent_id>/agent/`
3. 将`SOUL.md`、`EXAMPLES.md`、`ANTI-EXAMPLES.md`、`MEMORY.md`文件放入工作空间
4. 在代理目录中创建`AGENTS.md`文件——模板参考：`references/agents-guide.md`
5. 通过`gateway config.patch`将代理注册到OpenClaw配置中。

### 第五步：测试

向数字孪生体发送消息，并验证其是否能够按照用户的性格进行回应。如有需要，可继续修改`SOUL.md`文件。

## 隐私与数据管理

- 聊天记录应仅在本地处理，绝不能传输到外部服务（除非是通过LLM API调用）。
- 解析后的数据和生成的档案存储在用户的本地OpenClaw工作空间中。
- 用户需负责保护数字孪生体的数据安全，并尊重用户的隐私。
- 如果用户请求删除数字孪生体，需删除所有相关工作空间文件、代理配置和解析后的数据。

## 提高数字孪生体质量的建议：

- **聊天记录越多，生成的数字孪生体越真实。** 建议提供50条以上的聊天记录。
- **文本消息最为重要。** 音频/图片/贴纸消息在导出过程中会丢失。
- **最新的聊天记录更合适。** 人们的沟通方式会随时间变化。
- **结合多条聊天记录**。如果可能的话，合并同一用户的多个聊天记录导出文件。
- **不断优化。** 测试数字孪生体的表现，发现不足之处并不断完善`SOUL.md`文件。