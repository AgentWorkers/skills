---
name: tg-cli
description: 通过 MTProto 实现的仅限读取功能的 Telegram 命令行接口（CLI）。该接口可以列出聊天记录、获取消息、下载媒体文件，并管理本地账户/会话信息。但该接口不支持发送消息或修改 Telegram 数据。适用于用户需要读取聊天记录、获取消息、下载媒体文件或自动化提取 Telegram 数据的场景。
required_binaries:
  - name: tg
    package: tg-mtproto-cli
    install: npm install -g tg-mtproto-cli
    registry: https://www.npmjs.com/package/tg-mtproto-cli
    source: https://github.com/cyberash-dev/tg-mtproto-cli
  - name: jq
    optional: true
    install: brew install jq
credentials:
  - name: Telegram API credentials
    fields: [api_id, api_hash]
    obtain: https://my.telegram.org/apps
    storage: system keychain (macOS Keychain / Windows Credential Vault / Linux Secret Service)
    input: interactive prompt via `tg auth`
  - name: Phone number + OTP
    storage: not persisted
    input: interactive prompt via `tg auth` (one-time, creates session)
runtime_permissions:
  network: outbound TCP to Telegram DC servers (MTProto protocol)
  filesystem:
    - read/write: ~/.tg-mtproto-cli/sessions/*.session (SQLite auth sessions)
    - write: media files to --out dir or cwd (tg download only)
  keychain: read/write account metadata and API credentials
  shell: false
  browser: false
---
# tg — 通过 MTProto 协议使用的 Telegram 命令行工具

这是一个用于直接通过 MTProto 协议读取 Telegram 数据的命令行工具。无需使用 Bot API，也没有使用限制。

## 所需的二进制文件

| 二进制文件 | 安装方式 | 用途 |
|---|---|---|
| `tg` | `npm install -g tg-mtproto-cli` | 核心命令行工具 |
| `jq`（可选） | `brew install jq` 或 `apt install jq` | 用于工作流示例中的 JSON 过滤 |

源代码及开发信息：
- npm: [npmjs.com/package/tg-mtproto-cli](https://www.npmjs.com/package/tg-mtproto-cli)
- GitHub: [github.com/cyberash-dev/tg-mtproto-cli](https://github.com/cyberash-dev/tg-mtproto-cli)

安装完成后请进行验证：

```bash
tg --version
npm ls -g tg-mtproto-cli
```

## 所需的凭证

| 凭证 | 获取方式 | 存储位置 |
|---|---|---|
| Telegram 的 `api_id` 和 `api_hash` | [my.telegram.org/apps](https://my.telegram.org/apps) | 系统密钥链（macOS Keychain / Windows Credential Vault / Linux Secret Service） |
| 手机号码 + OTP 代码 | 在执行 `tg auth` 时输入 | 仅用于会话创建，使用一次后会被销毁 |

凭证需要通过 `tg auth` 交互式输入。无需使用环境变量。

## 运行时资源

| 资源 | 访问方式 | 详细信息 |
|---|---|---|
| 网络 | 发往 Telegram 数据中心的 TCP 连接 | 所有命令均需使用 MTProto 协议 |
| 会话文件 | 读写 `~/.tg-mtproto-cli/sessions/*.session` | 存储认证信息的 SQLite 数据库；由 `tg auth` 创建 |
| 系统密钥链 | 读写 | 存储 `api_id`、`api_hash`、账户元数据及默认账户信息 |
| 文件系统 | 写入（仅限 `tg download` 命令） | 将媒体文件保存到 `--out` 目录或当前目录 |

## 使用限制

- 该命令行工具仅具有 **读取** 功能，无法发送消息、创建聊天、修改群组或对 Telegram 进行任何写入操作。唯一的写入目标为本地文件（会话文件和下载的媒体文件）。
- `tg download` 命令仅将文件保存到明确指定的 `--out` 目录或当前工作目录。
- 会话文件包含敏感的认证信息，请勿读取、复制或公开 `~/.tg-mtproto-cli/sessions/` 目录的内容。
- 请勿记录或显示 `api_id` 和 `api_hash` 的值。
- 如果需要使用 `tg auth`，请告知用户，因为它需要交互式输入（手机验证码），无法自动化完成。

## 聊天识别方式

聊天可以通过以下方式引用：
- **用户名**：`@username` 或 `username`
- **数字 ID**：`-1001234567890`（群组/超级群的 ID 为负数）
- **电话号码**：`+1234567890`（私人聊天的 ID）

要查找聊天的数字 ID，可以使用 `tg chats --json | jq '.[] | {id, title}'`。

## 命令参考

### 列出聊天记录

```bash
tg chats [--type private|group|supergroup|channel] [--limit 50] [--offset 0]
```

### 读取消息

```bash
tg messages <chat> [-n 100] [--all] [--topic <id>] [--after <datetime>]
```

| 标志 | 说明 |
|---|---|
| `-n <数量>` | 显示的消息数量（默认：100 条） |
| `--all` | 显示全部聊天记录 |
| `--topic <ID>` | 显示指定主题的聊天记录（ID 可通过 `tg topics <聊天名称>` 获取） |
| `--after <日期>` | 仅显示指定日期之后的消息 |

`--after` 的格式示例：`2026-02-22`、`2026-02-22T10:00`、`10:00`（今天）。

当 `--after` 与 `-n` 同时使用时，会先按日期过滤，再显示前 N 条消息。

### 列出聊天主题

```bash
tg topics <chat>
```

返回 `--topic` 标志所需的主题 ID。

### 下载媒体文件

```bash
tg download <chat> <messageId> [--out <dir>]
```

从特定消息中下载媒体附件。消息 ID 可从 `tg messages` 的输出结果中获取（显示为 `#<ID>`）。

### 账户管理

```bash
tg auth                          # authenticate (interactive)
tg logout [alias]                # remove session
tg accounts                      # list accounts
tg accounts rename <old> <new>   # rename alias
tg default <alias>               # set default
```

## 全局标志

| 标志 | 功能 |
|---|---|
| `--account <别名>` | 使用指定账户而不是默认账户 |
| `--json` | 以 JSON 格式输出（适用于脚本编写/管道传输） |

## JSON 输出格式

所有命令都支持 `--json` 选项，以结构化格式输出结果。日期格式遵循 ISO 8601 标准。

```bash
tg chats --json
tg messages @chat -n 10 --json
tg download @chat 42 --json
```

### 消息的 JSON 结构

当没有附件时，`media` 字段值为 `null`。`media.type` 的可能值包括：`photo`（照片）、`video`（视频）、`document`（文档）、`audio`（音频）、`voice`（语音）和 `sticker`（贴纸）。

## 常见工作流程

### 从指定日期起提取聊天中的文本

```bash
tg messages @channel --after 2026-02-01 --json | jq -r '.[].text // empty'
```

### 查找包含照片的消息

```bash
tg messages @chat -n 500 --json | jq '[.[] | select(.media.type == "photo")]'
```

### 下载最近消息中的所有照片

```bash
for id in $(tg messages @chat -n 50 --json | jq -r '.[] | select(.media.type == "photo") | .id'); do
  tg download @chat "$id" --out ./photos
done
```

### 读取聊天主题的内容

```bash
tg topics -1001234567890          # find topic ID
tg messages -1001234567890 --topic 42 -n 20
```

### 多账户使用

```bash
tg chats --account work
tg messages @chat -n 10 --account personal
```

## 错误代码

| 代码 | 含义 |
|---|---|
| 0 | 操作成功 |
| 1 | 运行时错误（参数无效、聊天未找到） |
| 2 | 需要认证（没有账户或会话已过期）——请运行 `tg auth` 进行重新认证 |

## 故障排除

- 如果出现 “没有默认账户” 的错误，请运行 `tg auth` 或使用 `--account <别名>` |
- 如果提示 “会话已过期”，请运行 `tg auth` 重新认证 |
- 如果找不到聊天记录，请使用 `tg chats --json` 命令获取聊天的数字 ID |
- 如果没有显示消息，请检查聊天 ID 的格式（群组的 ID 为负数）