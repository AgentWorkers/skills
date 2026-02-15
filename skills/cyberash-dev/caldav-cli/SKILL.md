---
name: caldav-cli
description: 通过命令行管理 CalDAV 日历（iCloud、Google、Yandex）。支持 OAuth2 和 Basic 身份验证，支持多账户管理，输出格式可为表格或 JSON。
metadata: {"clawdbot":{"emoji":"📅","os":["linux","macos"],"requires":{"bins":["caldav-cli","node"],"configs":["~/.config/caldav-cli/config.json"],"keychain":true},"install":[{"id":"npm","kind":"shell","command":"npm install -g caldav-cli","bins":["caldav-cli"],"label":"Install caldav-cli via npm"}],"source":"https://github.com/cyberash-dev/caldav-cli"}}
---

# caldav-cli

这是一个 CalDAV 命令行客户端，支持通过安全的操作系统密钥链（keychain）存储多个账户信息。它兼容 iCloud、Google（OAuth2）、Yandex 以及任何自定义的 CalDAV 服务器。

## 安装

需要 Node.js >= 18。

```bash
npm install -g caldav-cli
```

安装完成后，`caldav-cli` 命令将在系统中全局可用。

## 快速入门

```bash
caldav-cli account add          # Interactive wizard: pick provider, enter credentials
caldav-cli events list          # Show events for the next 7 days
caldav-cli events create        # Interactive wizard: create a new event
```

## 账户管理

- **添加账户**：通过交互式向导输入提供商信息、登录凭据并测试连接。
- **列出已配置的账户**：
- **删除账户**：

## 查看事件

```bash
caldav-cli events list                           # Next 7 days (default)
caldav-cli events list --from 2026-02-10 --to 2026-02-20
caldav-cli events list -a work                   # Specific account
caldav-cli events list -c "Team Calendar"        # Filter by calendar name
caldav-cli events list -a work -c Personal --from 2026-03-01 --to 2026-03-31
```

事件数据以 JSON 格式输出，便于脚本处理。

## 创建事件

- **通过交互式向导输入所有必要信息**。
- **非交互式方式（使用命令行参数）**：
- **部分参数的使用方式（向导会提示剩余的输入内容）**：

事件创建完成后，也会以 JSON 格式输出结果。

## 支持的提供商

| 提供商 | 认证方式 | 服务器地址 |
|---------|---------|-----------|
| Apple iCloud | Basic（应用特定密码） | `https://caldav.icloud.com` |
| Google 日历 | OAuth2（客户端 ID + 密钥） | `https://apidata.googleusercontent.com/caldav/v2` |
| Yandex 日历 | Basic（应用密码） | `https://caldav.yandex.ru` |
| 自定义提供商 | Basic | 用户提供服务器地址 |

## Google 日历设置

使用 caldav-cli 添加账户前，需要完成以下步骤：

1. 访问 [Google Cloud Console](https://console.cloud.google.com/)。
2. 创建项目并启用 CalDAV API。
3. 生成 OAuth 客户端 ID（适用于桌面应用程序）。
4. 记下客户端 ID 和客户端密钥。

向导会提示您输入这些信息，并引导您完成授权流程。授权所需的刷新令牌会安全地存储在操作系统的密钥链中。

## 数据存储方式

- **密码、OAuth2 刷新令牌以及 OAuth2 客户端凭据**（客户端 ID、客户端密钥、令牌地址）：存储在操作系统的密钥链中（macOS 的 Keychain、Linux 的 libsecret、Windows 的 Credential Vault）；这些数据绝不会以明文形式保存在磁盘上。
- **账户元数据**（名称、提供商 ID、用户名、服务器地址）：存储在 `~/.config/caldav-cli/config.json` 文件中（文件权限设置为 `0600`）。

所有敏感信息都不会保存在磁盘上。对于之前将 OAuth2 客户端凭据保存在 `config.json` 文件中的旧版本，系统会在首次运行时自动将其迁移到密钥链中。

## 命令行参数参考

### `events list`  
| 参数 | 缩写 | 说明 | 默认值 |
|------|-------|-----------|---------|
| `--account <名称>` | `-a` | 指定账户名称 | 使用默认账户 |
| `--from <日期>` | | 事件开始日期（格式：YYYY-MM-DD） | 当前日期 |
| `--to <日期>` | | 事件结束日期（格式：YYYY-MM-DD） | 当前日期后 7 天 |
| `--calendar <名称>` | `-c` | 按日历名称过滤事件 | 显示所有日历的事件 |
| `--json` | | 以 JSON 格式输出结果 | 不输出 |

### `events create`  
| 参数 | 缩写 | 说明 |
|------|-------|-----------|
| `--title <标题>` | `-t` | 事件标题 |
| `--start <日期时间>` | `-s` | 事件开始时间（格式：YYYY-MM-DDTHH:mm） |
| `--end <日期时间>` | `-e` | 事件结束时间（格式：YYYY-MM-DDTHH:mm） |
| `--account <名称>` | `-a` | 指定账户名称 |
| `--calendar <名称>` | `-c` | 按日历名称过滤事件 |
| `--description <描述>` | `-d` | 事件描述 |
| `--location <位置>` | `-l` | 事件地点 |
| `--json` | | 以 JSON 格式输出结果 |

所有 `events create` 命令行参数均为可选参数。如果省略这些参数，系统会使用交互式向导来收集所需信息。