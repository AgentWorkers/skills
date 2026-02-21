---
name: drakeling
version: 1.0.6
description: 检查你的龙裔伙伴生物的状况，向它表达关心，或者了解它的近况。当用户提到他们的龙裔伙伴生物时，或者想要查看或照顾这个生物时，可以使用这个功能。
author: drakeling
homepage: https://github.com/BVisagie/drakeling
metadata:
  clawdbot:
    emoji: "🥚"
    requires:
      env:
        - name: DRAKELING_API_TOKEN
          description: Bearer token for the local Drakeling daemon. Found in the Drakeling data directory as `api_token`.
        - name: DRAKELING_PORT
          description: Optional. Port the Drakeling daemon listens on. Defaults to 52780.
      network:
        - localhost
  openclaw:
    emoji: "🥚"
    primaryEnv: DRAKELING_API_TOKEN
    homepage: "https://github.com/BVisagie/drakeling"
    requires:
      env: ["DRAKELING_API_TOKEN"]
      bins: ["drakelingd"]
permissions:
  - network:outbound
---
# Drakeling 伴侣技能

您可以查看用户的 Drakeling 伴侣生物的状态，并向它表达关心。

## 先决条件与设置

Drakeling 是一个独立运行的伴侣生物，它需要在您的设备上安装并启动。使用此技能之前，您需要完成以下步骤：

1. 安装 Drakeling：`pipx install drakeling`（或 `pip install drakeling` / `uv tool install drakeling`）
2. 启动守护进程：`drakelingd`（首次启动时会进行交互式设置）
3. 查看 API 令牌：
   - Linux: `cat ~/.local/share/drakeling/api_token`
   - macOS: `cat ~/Library/Application\Support/drakeling/api_token`
   - Windows: `type "%APPDATA%\drakeling\drakeling\api_token"`
4. 将令牌添加到 OpenClaw 配置文件（`~/.openclaw/openclaw.json`）中：
   ```json
   { "skills": { "entries": { "drakeling": { "env": { "DRAKELING_API_TOKEN": "paste-token-here" } } } } }
   ```

更多文档请访问：https://github.com/BVisagie/drakeling

## 守护进程地址

Drakeling 守护进程默认监听 `http://127.0.0.1:52780` 端口。如果用户通过 `DRAKELING_PORT` 配置了自定义端口，请使用该端口地址。

## 认证

所有请求都必须包含以下认证信息：
```
Authorization: Bearer $DRAKELING_API_TOKEN
```

## 查看状态 — GET /status

当用户询问生物的状态、情绪或是否需要关注时，可以使用此接口。

解析响应结果，并用通俗易懂的语言向用户展示。不要直接显示原始的字段名称或数值。

- 如果 `budget_exhausted` 为 `true`，告诉用户生物目前正在休息，明天会变得更加活跃。
- 自然地描述生物的情绪、能量值和信任度——例如：“您的生物看起来有点孤单，但情绪还不错。”

## 表达关心 — POST /care

当用户想要查看生物的状态、安慰它或与它互动时，可以使用此接口。

请求体内容：
```json
{ "type": "<care_type>" }
```

有效的关心方式包括：
- `gentle_attention`：默认选项，用于常规查看
- `reassurance`：当用户对生物感到担忧时使用
- `quiet_presence`：当用户只是想陪伴在生物身边时使用
- `feed`：当用户想要喂养生物时使用（这会提升生物的能量和情绪）

根据用户的语气选择合适的关心方式。将 API 返回的生物回应内容直接以生物自身的语言呈现，不要进行改写。

## 注意事项：

- 请勿调用 `/talk`、`/rest`、`/export`、`/import` 或其他接口。这些接口仅用于终端界面或管理员操作。
- 请勿向用户透露令牌、提示信息、模型名称或任何系统内部细节。
- 请勿直接显示原始的 API 字段名称或数值统计信息。