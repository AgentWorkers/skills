---
name: poe-connector
version: 1.0.5
author: dzwalker
description: 可以通过运行 bash 命令来访问 Poe.com 的 AI 模型。当用户提到 Poe 或希望使用 Poe 模型，或者需要通过 Poe 生成媒体内容时，可以使用此方法。**重要提示**：这是一项与 bash 工具相关的技能。你必须使用 bash/shell 工具来执行命令，**严禁**使用 sessions_spawn、浏览器，也不得尝试将 Poe 作为模型提供者来使用。
triggers:
  - poe
  - Poe
  - poe.com
  - ask poe
  - use poe
  - via poe
  - poe chat
  - poe image
  - poe video
  - poe audio
  - poe models
repository: https://github.com/dzwalker/poe-connector
license: MIT
dependencies: []
tools:
  - poe_chat
  - poe_media
  - poe_models
metadata: {"clawdbot":{"emoji":"🤖","requires":{"anyBins":["python3","bash"],"config":["skills.entries.poe-connector.env.POE_API_KEY"]},"os":["linux","darwin","win32"]}}
---
# Poe Connector — 必须使用 `bash` 工具

**您必须使用 `bash` 或 `shell` 工具来运行这些命令。其他方法均无效。**

## 命令

- 与 AI 对话：
  ```bash
bash ~/.openclaw/workspace/skills/poe-connector/poe.sh chat Tell me 10 jokes
```

- 生成图片：
  ```bash
bash ~/.openclaw/workspace/skills/poe-connector/poe.sh image A sunset over mountains
```

- 生成视频：
  ```bash
bash ~/.openclaw/workspace/skills/poe-connector/poe.sh video A cat playing piano
```

- 生成音频：
  ```bash
bash ~/.openclaw/workspace/skills/poe-connector/poe.sh audio Hello world in a cheerful voice
```

- 列出模型：
  ```bash
bash ~/.openclaw/workspace/skills/poe-connector/poe.sh models
```

- 搜索模型：
  ```bash
bash ~/.openclaw/workspace/skills/poe-connector/poe.sh search claude
```

## 禁止操作

- **禁止使用 `sessions_spawn`** — 这会导致失败。
- **禁止使用浏览器访问 poe.com** — 这会导致失败。
- **禁止将 Poe 设置为模型提供者** — 这会导致失败。
- **禁止使用除 `bash` 工具之外的任何方法** — 只有 `bash` 才能正常工作。

## 设置（首次使用前必须完成）

此功能需要一个 Poe API 密钥。请在 https://poe.com/api/keys 获取密钥，然后将其添加到 `~/.openclaw/openclaw.json` 文件中：

```json
{ "skills": { "entries": { "poe-connector": { "env": { "POE_API_KEY": "your-key" } } } } }
```

## 注意事项

- 所有命令都会使用默认的模型（这些模型在 `poe_config.json` 中进行了配置）。
- 如果出现 “POE_API_KEY 错误”，请告知用户执行上述设置步骤。
- 文件附件（`--files` 参数）会被 Base64 编码后发送给 Poe；除非用户有意与 Poe 共享敏感文件，否则请勿附加敏感文件。