# clawd-migrate

用于将机器人系统从 **moltbot** 或 **clawdbot** 迁移到 **openclaw**。该工具能够安全地保留配置文件、内存数据以及 **clawdbook**（Moltbook）中的信息，适用于任何操作系统。

## 功能概述

- **检测** 系统中现有的机器人相关资源（内存文件、配置文件以及 **clawdbook/Moltbook** 的认证信息）。
- **在开始迁移之前，将所有数据备份到一个带有时间戳的文件夹中**。
- **将文件按照 **openclaw** 的文件结构进行迁移**（分别存储到 `memory/`、`.config/openclaw/` 和 `.config/clawdbook/` 目录中）。
- **验证** 所有源文件是否已成功复制到目标位置（包括文件是否存在以及文件大小是否一致）。
- **重新安装 **openclaw**（使用命令 `npm i -g openclaw`），并自动执行 `openclaw onboard` 命令以完成初始化。

## 快速入门

通过交互式菜单引导您完成以下步骤：发现现有资源 → 备份数据 → 迁移系统 → 验证迁移结果 → 重新安装 openclaw。

## 命令行接口（CLI）命令

（具体 CLI 命令请参见下方代码块）

## 系统要求

- Node.js 14 及以上版本
- Python 3.x

## 被迁移的数据包括：

- **内存/身份信息**：`SOUL.md`、`USER.md`、`TOOLS.md`、`IDENTITY.md`、`AGENTS.md`、`MEMORY.md`
- **配置文件**：`.config/moltbook/`、`.config/moltbot/`
- **clawdbook/Moltbook** 相关数据**：存储在 `.config/clawdbook/` 目录下（包括认证信息、API 密钥等）
- **可选数据**：`projects/` 目录（如果存在的话）

## 相关标签

migration、openclaw、moltbot、clawdbot、clawdbook、moltbook、backup、verify