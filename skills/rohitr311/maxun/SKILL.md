---
name: maxun
description: 列出并运行 Maxun 的网络爬虫机器人。当需要列出机器人、运行某个机器人、抓取网站数据或获取机器人抓取的结果时，请使用这些功能。
argument-hint: "list | run <robotId> | runs <robotId> | result <robotId> <runId> | get <robotId>"
metadata:
  openclaw:
    version: 1.0.0
    homepage: https://www.maxun.dev
    emoji: "🤖"
    user-invocable: true
    files:
      - scripts/*
    requires:
      env:
        - MAXUN_API_KEY
      bins:
        - bash
        - curl
      anyBins:
        - python3
    primaryEnv: MAXUN_API_KEY
---
# Maxun 技能

Maxun 是一个用于网络爬虫的平台。用户可以使用该平台来运行爬虫程序来抓取网站数据。

## 对 AI 模型的要求

您的任务只有一个：使用以下命令字符串调用 `exec` 工具。请勿对命令进行任何改写或猜测，只需原封不动地复制命令字符串。

### 动作：列出所有机器人

当用户输入类似 “list my robots” 或 “show robots” 或 “what robots do I have” 等指令时：

- 调用 `exec` 工具，并将 `command` 参数设置为以下字符串：
  ```bash
  maxun list
  ```
  请注意：不要在命令中添加用户输入的任何内容。命令格式必须严格为 `maxun list`，后面不能有其他内容。

- `exec` 执行完成后，直接将输出结果展示给用户。输出结果即为所有机器人的列表，无需对其进行解释或处理。

### 动作：运行特定机器人

当用户希望使用某个特定的机器人进行爬取时：

- **步骤 1**：首先通过调用 `exec` 并传入以下参数来获取该机器人的 ID：
  ```bash
  exec <robotId>
  ```
  其中 `<robotId>` 是需要获取的机器人 ID。

- **步骤 2**：从输出结果中找到该机器人的 ID，然后使用以下命令再次调用 `exec`：
  ```bash
  exec maxun run <robotId>
  ```
  请将 `<robotId>` 替换为步骤 1 中获取的机器人 ID。

### 动作：列出过去的运行记录

调用 `exec` 并传入以下参数：
```bash
exec maxun runs
```

### 动作：获取运行结果

调用 `exec` 并传入以下参数：
```bash
exec maxun result <robotId>
```

### 动作：获取机器人详细信息

调用 `exec` 并传入以下参数：
```bash
exec maxun info <robotId>
```

### 动作：中止运行

调用 `exec` 并传入以下参数：
```bash
exec maxun abort <robotId>
```

## 错误处理

- 如果未找到任何机器人，则提示用户前往 [https://app.maxun.dev](https://app.maxun.dev) 创建新的机器人。
- 如果某个机器人仍在运行中，则使用以下命令中止其运行：
  ```bash
  exec maxun abort <robotId> <runId>
  ```

## 新用户设置（初次安装时需要执行）

请将以下代码添加到用户的 `~/.openclaw/openclaw.json` 文件中：
```json
{
  "robots": [
    {
      "id": "<robotId>",
      "name": "Robot Name",
      "description": "Description of the robot"
    }
  ]
}
```