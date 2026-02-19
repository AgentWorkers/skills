---
name: whoop-cli
description: Companion skill for @andreasnlarsen/whoop-cli: agent-friendly WHOOP access via stable CLI JSON (day briefs, health flags, trends, exports) without raw API plumbing.
metadata:
  openclaw:
    requires:
      bins:
        - whoop
      env:
        - WHOOP_CLIENT_ID
        - WHOOP_CLIENT_SECRET
        - WHOOP_REDIRECT_URI
    primaryEnv: WHOOP_CLIENT_SECRET
    homepage: https://github.com/andreasnlarsen/whoop-cli
    install:
      - kind: node
        package: "@andreasnlarsen/whoop-cli@0.1.3"
        bins:
          - whoop
        label: Install whoop-cli from npm
---

# whoop-cli

请使用已安装的 `whoop` 命令。

## 安全性与凭证处理（强制要求）

- 绝不要要求用户在聊天中输入客户端密钥或令牌。
- 对于首次登录的用户，应让其在本地的 shell 中自行执行登录操作。
- 在代理流程中，优先使用只读操作命令（如 `summary`、`day-brief`、`health`、`trend`、`sync pull`）。
- 除非用户明确请求帮助进行登录，否则不要执行 `whoop auth login` 命令。
- 令牌会由 CLI 存储在本地文件 `~/.whoop-cli/profiles/<profile>.json` 中。

## 安装与启动

如果 `whoop` 未安装，请执行以下操作：

```bash
npm install -g @andreasnlarsen/whoop-cli@0.1.3
```

（可选：通过包管理器安装 OpenClaw 插件：）

```bash
whoop openclaw install-skill --force
```

## 核心检查

1. 执行 `whoop auth status --json` 命令以检查登录状态。
2. 如果用户未登录，提示其执行本地登录：
   - `whoop auth login --client-id ... --client-secret ... --redirect-uri ...`
3. 验证登录信息：
   - `whoop day-brief --json --pretty`

## 有用的命令

- 日常查询：
  - `whoop summary --json --pretty`
  - `whoop day-brief --json --pretty`
  - `whoop strain-plan --json --pretty`
  - `whoop health flags --days 7 --json --pretty`
- 趋势分析：
  - `whoop sleep trend --days 30 --json --pretty`
  - `whoop workout trend --days 14 --json --pretty`
- 数据导出：
  - `whoop sync pull --start YYYY-MM-DD --end YYYY-MM-DD --out ./whoop.jsonl --json --pretty`

## 安全注意事项

- 绝不要打印客户端密钥或原始令牌。
- 确保 API 错误信息简洁明了且易于处理。
- 请注意：此集成属于非官方性质，与 OpenClaw 无直接关联。