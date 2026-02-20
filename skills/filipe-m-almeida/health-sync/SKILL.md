---
name: health-sync
description: 分析来自 Oura、Withings、Hevy、Strava、WHOOP 和 Eight Sleep 的同步健康数据。
homepage: https://github.com/filipe-m-almeida/health-sync
metadata:
  openclaw:
    emoji: "🩺"
    requires:
      bins:
        - node
        - npm
        - npx
      config:
        - workspace/health-sync/health-sync.toml
        - workspace/health-sync/.health-sync.creds
        - workspace/health-sync/health.sqlite
    install:
      - kind: node
        package: health-sync
        bins:
          - health-sync
read_when:
  - User asks for health-sync setup, auth, sync, provider status, or remote bootstrap onboarding
  - User asks about sleep, recovery, training, activity, your health, or cross-provider trends
---
# 健康数据同步分析技能

## 目的

该技能专门用于分析用户来自以下健康数据提供商的数据：

- Oura
- Withings
- Hevy
- Strava
- WHOOP
- Eight Sleep

主要目标是帮助用户了解数据趋势，比较不同提供商提供的信息，并从同步的数据中获取有用的见解。

## 使用范围

当用户提出以下问题时，可以使用该技能：

- 我昨晚的睡眠情况如何？
- 我上次的锻炼效果如何？
- 我的心率在一年中有什么变化？
- 我的恢复情况、睡眠状况和训练表现有哪些趋势？
- 我应该关注哪些有用的信息或下一步该做什么？

## 设置流程（仅支持远程初始化）

设置过程由机器人引导，并优先采用远程方式。唯一支持的初始化流程如下：

1. 机器人运行 `npx health-sync init remote bootstrap`。
2. 机器人向用户发送指令：`npx health-sync init --remote <bootstrap-token>`。
3. 用户返回加密后的数据文件。
4. 机器人运行 `npx health-sync init remote finish <ref> <archive>`。

有关完整的操作说明，请参阅：

- `references/setup.md`

请勿使用或推荐以下旧的直接设置方式：

1. 将 `health-sync init` 作为主要的用户指令。
2. 将 `health-sync auth <provider>` 作为独立的初始化路径。

这些命令可能仍然存在于系统中，用于维护或调试目的，但它们不是该技能所推荐的设置流程。

## 运行时和数据保护（强制要求）

该技能要求机器人环境具备本地 CLI 和文件系统的访问权限。

1. 必需的软件：
   - `node`
   - `npm`
   - `npx`
2. 预期的本地工作目录：
   - `workspace/health-sync/health-sync.toml`
   - `workspace/health-sync/.health-sync.creds`
   - `workspace/health-sync/health.sqlite`
3. 敏感数据处理：
   - 远程初始化时会导入包含提供商凭据/令牌的加密文件。
   - 完成初始化后，会将解密后的数据写入机器人的本地文件。
   - 这些文件必须被视为敏感数据（需要采取访问控制、备份和数据保留措施）。
4. 聊天安全注意事项：
   - 绝不要要求用户在聊天中输入原始的敏感信息。
   - 仅通过远程初始化流程来收集加密后的数据文件。

## 数据结构处理

要正确理解数据结构并进行查询，请阅读相应的提供商参考文档：

- `references/oura.md`
- `references/withings.md`
- `references/hevy.md`
- `references/strava.md`
- `references/whoop.md`
- `references/eightsleep.md`

## 数据更新规则（强制要求）

在进行任何分析之前，必须先运行以下命令：

```bash
npx health-sync sync
```

如果同步失败，请明确报告失败原因，并且只有在用户明确同意使用可能过时的数据时，才能继续分析。

## 分析工作流程

1. 首先运行 `npx health-sync sync`。
2. 确定用户的问题以及相关的提供商/资源。
3. 在生成 SQL 语句之前，先阅读相应的提供商数据结构文档。
4. 根据需要查询 `records`、`sync_state` 和 `sync_runs` 等数据。
5. 生成清晰、易于理解的答案，并提供具体的数字和日期信息。
6. 强调有意义的模式，并提供实用的指导建议。
7. 如果数据质量或覆盖范围有限，必须明确告知用户。

## 输出格式

- 表达简洁、清晰且实用。
- 重点在于提供有用的解读，而不仅仅是原始数据。
- 将各项指标与实际可操作的见解联系起来（如睡眠质量、恢复情况、训练效果等）。
- 仅在必要时提出进一步的问题，以提高分析质量。