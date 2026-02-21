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
        package: "@andreasnlarsen/whoop-cli@0.3.1"
        bins:
          - whoop
        label: Install whoop-cli from npm
---

# whoop-cli

请使用已安装的 `whoop` 命令。

## 安全性及凭证处理（强制要求）

- 绝不要要求用户在聊天中输入客户端密钥或令牌。
- 对于首次登录的用户，应让其在本地的 shell 中自行完成登录操作。
- 在代理流程中，优先使用只读操作命令（如 `summary`、`day-brief`、`health`、`trend`、`sync pull`）。
- 除非用户明确请求帮助进行登录，否则不要执行 `whoop auth login` 命令。
- 令牌由 CLI 保存在本地文件 `~/.whoop-cli/profiles/<profile>.json` 中。

## 安装/启动

如果 `whoop` 未安装：

```bash
npm install -g @andreasnlarsen/whoop-cli@0.3.1
```

（可选：通过包管理器安装 OpenClaw 插件）

```bash
whoop openclaw install-skill --force
```

## 核心检查

1. `whoop auth status --json`：检查认证状态。
2. 如果用户未认证，提示其执行本地登录：
   - `whoop auth login --client-id ... --client-secret ... --redirect-uri ...`
3. 验证用户信息：
   - `whoop day-brief --json --pretty`

## 有用的命令

- 日常查询：
  - `whoop summary --json --pretty`
  - `whoop day-brief --json --pretty`
  - `whoop strain-plan --json --pretty`
  - `whoop health flags --days 7 --json --pretty`
- 活动分析：
  - `whoop activity list --days 30 --json --pretty`
  - `whoop activity trend --days 30 --json --pretty`
  - `whoop activity types --days 30 --json --pretty`
  - 仅用于训练数据分析：`whoop activity trend --days 30 --labeled-only --json --pretty`

### 活动解读规则（重要）

- WHOOP 系统中的通用活动记录（通常 `sport_id=-1`）可能是自动检测到的，可能表示非刻意进行的运动（如家务或偶然活动），而非训练行为。
- 默认情况下，不要将这些通用活动记录视为有效的训练数据。
- 在提供训练建议时，建议使用 `--labeled-only` 选项，同时显示总记录数和过滤后的记录数。

### 代理数据过滤方式（兼容jq工具）

- 数据来源：`whoop activity list --json`
- 首先推荐使用内置的过滤选项（`--labeled-only`、`--generic-only`、`--sport-id`、`--sport-name`）。
- 如果需要自定义过滤，可以使用 `jq` 在 shell 中对原始 JSON 数据进行处理（示例代码见下文）：

```bash
whoop activity list --days 30 --json | jq '.data.records | map(select(.sport_id != -1))'
```

- 数据导出：
  - `whoop sync pull --start YYYY-MM-DD --end YYYY-MM-DD --out ./whoop.jsonl --json --pretty`

## 实验管理（仅限代理使用）

- 实验数据存储在 `~/.whoop-cli/experiments.json` 文件中。
- 创建实验时需指定详细信息：
  - `whoop experiment plan --name ... --behavior ... --start-date YYYY-MM-DD --end-date YYYY-MM-DD --description ... --why ... --hypothesis ... --success-criteria ... --protocol ... --json --pretty`
- 更新实验信息时避免创建重复记录：
  - `whoop experiment context --id ... --description ... --why ... --hypothesis ... --success-criteria ... --protocol ...] --json --pretty`
- 查看实验状态：
  - `whoop experiment status [--status planned|running|completed] --id ... --json --pretty`
- 评估实验结果：
  - `whoop experiment report --id ... --json --pretty`
- 默认情况下，实验数据仅针对特定用户或团队可见（需使用 `--profile` 选项）。
- 除非用户特别要求，否则建议使用 `--all-profiles` 选项以查看所有用户的实验数据。
- 推荐使用 `sourceOfTruth` 输出字段（指向实验数据的原始文件路径）；`experimentsFile` 仅作为兼容性保留。
- 除非用户明确要求，否则不要将实验数据复制到其他文件中。

## 安全注意事项

- 绝不要打印客户端密钥或原始令牌。
- 确保 API 错误信息简洁明了且易于处理。
- 请注意：此工具为非官方开发，与 OpenClaw 无直接关联。