---
name: tg-channel-manager
description: >
  这是一个通用的、基于配置的内容处理引擎，适用于任何 Telegram 频道：
  - 通过 SearXNG 进行新闻搜索；
  - 支持草稿功能；
  - 支持定时发布内容；
  - 具备去重功能。
  所有频道相关的设置都通过配置文件进行定义——一个配置文件即可适用于所有频道。
metadata:
  openclaw:
    emoji: "📡"
    requires:
      bins: ["python3", "curl"]
      env: ["SEARXNG_URL"]
    primaryEnv: "SEARXNG_URL"
---
# TG频道管理器

工作流程：**扫描 → 草稿 → 人工审核 → 发布**

## 执行

您的环境中已安装`python3`和`curl`（在`requires.bins`文件中声明）。请使用`exec`/`bash`工具自行执行所有命令。切勿让用户为您运行命令。

## 启动

加载此技能后，请先运行预检查：

```bash
python3 {baseDir}/scripts/tgcm.py --workspace {workspace} check
```

**检查结果处理方式：**
- 如果所有结果均为`[ok]`，则默默地继续用户的任务。
- 如果出现`[fail] Bot token`错误，请求用户提供机器人令牌，并将其保存：`tgcm.py config set bot-token <token>`。不要询问令牌的来源或提供其他选项。
- 如果出现`[warn] SEARXNG_URL`错误，请求用户提供SearXNG的URL，并将其保存：`tgcm.py config set searxng-url <url>`。即使没有该URL，也可以继续执行其他命令，但扫描功能将无法使用。
- 如果出现`[fail] Channel`错误，请报告具体的频道问题及原因，并参考输出中的解决方法。
- 如果显示`[warn] No channels`，请告知用户这一情况，用户可能需要创建一个新的频道。

通过`config set`保存的设置会持久保存在`tgcm/.config.json`文件中，并被后续所有命令使用。

切勿对检查结果提出额外的问题。只需报告错误内容及相应的解决方法即可。
如果用户未指定任何任务，只需报告检查结果即可。

## 命令行参考（完整列表，无其他命令）

所有命令的格式为：`python3 {baseDir}/scripts/tgcm.py --workspace {workspace} <cmd>`

| 命令 | 功能 |
|---------|-------------|
| `init <name>` | 创建一个频道 |
| `list` | 显示所有频道 |
| `bind <name> --channel-id ID` | 将频道绑定到Telegram |
| `info <name> [--chat] [--subscribers] [--permissions] [--admins] [--all]` | 查看频道信息 |
| `get-id <@username\|ID>` | 根据@username或ID获取频道详细信息（id、类型、标题） |
| `check` | 预检查：验证机器人令牌、频道及环境变量 |
| `config set <key> <value>` | 本地保存设置（例如：bot-token、searxng-url） |
| `config get <key>` | 读取已保存的设置 |
| `config list` | 显示所有保存的设置 |
| `fetch-posts <name> [--limit N] [--dry-run]` | 从频道公开页面（t.me/s/）获取帖子并添加到去重索引中（需要频道具有@username权限） |
| `connect --channel-id ID --channel-title T` | 处理#tgcm的连接事件 |

机器人令牌会自动解析：`--bot-token`参数会从环境变量`$BOT_TOKEN`、`openclaw.json`文件以及`tgcm/.config.json`文件中自动获取。只需调用`tgcm.py get-id @username`即可（无需`--bot-token`参数）。如果自动解析失败，请使用`tgcm.py config set bot-token <token>`进行手动设置。

频道名称的格式要求为：`^[a-z0-9][a-z0-9_-]{0,62}$`。

## 快速参考

| 用户操作 | 对应操作 |
|-----------|---------|
| 「узнай/определи channel-id」 | `tgcm.py get-id @username` |
| 「подключи канал」 | 连接频道（详见下文） |
| 「какие каналы / список」 | `tgcm.py list` |
| 「статус канала X」 | `tgcm.py info X` |
| 「что в очереди」 | `cat tgcm/<name>/content-queue.md` |
| 「загрузи посты / rebuild index」 | `tgcm.py fetch-posts <name>` |

## 常用操作

### 查找频道ID

`python3 {baseDir}/scripts/tgcm.py get-id @username`

该命令会自动获取机器人令牌，并返回频道的ID、类型和标题。

### 连接频道

1. 获取频道ID：`python3 {baseDir}/scripts/tgcm.py get-id @username`
2. `python3 {baseDir}/scripts/tgcm.py --workspace {workspace} init <name>`
3. `python3 {baseDir}/scripts/tgcm.py --workspace {workspace} bind <name> --channel-id <id>`
4. 在`openclaw.json`文件中配置`skills.entries["tg-channel-manager"]`的相关设置。
5. 设置定时任务（详见`{baseDir}/references/cron-setup.md`）。

### 加载频道帖子（重建去重索引）

`python3 {baseDir}/scripts/tgcm.py --workspace {workspace} fetch-posts <name>`

该命令会从频道的公开页面（t.me/s/）获取帖子，并将其添加到`content-index.json`文件中。
选项说明：
- `--limit N`：限制获取的帖子数量（默认为5条）。
- `--dry-run`：仅预览操作。

### 查看频道信息/状态

- `tgcm.py list`
- `tgcm.py info <name>`
- 队列状态：`cat tgcm/<name>/content-queue.md`

## 注意事项：

- 请勿自行创建新的命令（上述命令即为全部可用命令）。
- 请勿直接发布帖子——仅由定时任务负责发布。
- 请勿在草稿状态跳过去重检查。
- 请勿让用户运行命令——环境中已安装`python3`和`curl`，请使用`exec`/`bash`自行执行命令。
- 请勿要求用户提供机器人令牌或环境变量——令牌会自动解析；`check`命令会显示错误信息。
- 请勿在检查后向用户询问额外问题——只需报告错误及相应的解决方法。
- 请勿询问频道类型（`get-id`命令会返回频道的类型信息，此技能仅适用于频道）。

## 数据结构

当`channelId`被设置且`status`为`"connected"`时，表示频道已成功绑定。

## 配置参数

配置参数来自`openclaw.json`文件中的`skills.entries["tg-channel-manager"]`：

### Telegram相关参数

| 参数 | 类型 | 说明 |
|-----------|------|-------------|
| `config.channelId` | 字符串 | 用于发布的Telegram频道ID |
| `config.chatId` | 字符串 | 频道社区聊天ID（可选） |

### 限制与调度参数

| 参数 | 类型 | 说明 |
|-----------|------|-------------|
| `config.maxPostsPerDay` | 数字 | 每天的最大帖子数量 |
| `config.maxDraftsPerRun` | 数字 | 每次扫描的最大草稿数量 |
| `config.timezone` | 字符串 | 时间区（IANA格式） |
| `config.language` | 字符串 | 帖子语言（如：ru、en等） |
| `config.cronScoutTimes` | 字符串数组 | 扫描任务的调度时间（cron格式） |
| `config.cronPublisherTimes` | 字符串数组 | 发布任务的调度时间（cron格式） |

### 内容相关参数

| 参数 | 类型 | 说明 |
|-----------|------|-------------|
| `config.rubrics` | 数组 | 评分规则（格式：`[{id, emoji, name}, ...]`） |
| `config.searchQueries` | 字符串数组 | SearXNG的搜索查询条件 |
| `config.searchInclude` | 字符串 | 需要包含的内容（过滤条件） |
| `config.searchExclude` | 字符串 | 需要排除的内容（过滤条件） |
| `config.evergreen` | 字符串数组 | 无新闻时的文章主题 |

### 帖子样式相关参数

| 参数 | 类型 | 说明 |
|-----------|------|-------------|
| `config.postStyle.minChars` | 数字 | 帖子的最小字符数 |
| `config.postStyle.maxChars` | 数字 | 帖子的最大字符数 |
| `config.postStyle.emojiTitle` | 布尔值 | 标题前是否显示emoji |
| `config.postStyle.boldTitle` | 布尔值 | 标题是否加粗 |
| `config.postStyle.signature` | 字符串 | 帖子的签名 |
| `config.postStyle.newsFooter` | 字符串 | 新闻帖子的额外文本（默认为空） |
| `config.postStyle.articleFooter` | 字符串 | 文章的额外文本（默认为空） |

### 环境参数

| 参数 | 类型 | 说明 |
| `env.SEARXNG_URL` | 字符串 | SearXNG实例的URL |

### 路径解析规则

- `{workspace}`：当前工作目录。可以使用`pwd`命令或`--workspace .`来获取当前工作目录。
- `{baseDir}`：`{workspace}/skills/tg-channel-manager`的路径。

在沙箱模式下（`workspaceAccess: "none"`），工作目录位于`~/.openclaw/sandboxes`，而非`~/.openclaw/workspace`。请始终使用相对路径。

关于定时任务的设置，请参考`{baseDir}/references/cron-setup.md`。

## 队列文件格式

`content-queue.md`文件中的条目格式如下：

```markdown
### <number>
- **Status:** draft | pending
- **Rubric:** <emoji> <name> (from config.rubrics)
- **Topic:** <topic>
- **Source:** <url> (for news)
- **Text:**

<post text>
```

状态说明：
- **draft**：等待审核
- **pending**：已审核，准备发布

发布后，相关条目将从`content-queue.md`文件中删除。

## 去重机制

**每次生成草稿前**：必须进行去重检查：

```bash
python3 {baseDir}/scripts/dedup-check.py --base-dir <workspace> --topic "topic" --links "url1" "url2"
```

**发布后**：将条目添加到索引中：

```bash
python3 {baseDir}/scripts/dedup-check.py --base-dir <workspace> --add <msgId> --topic "topic" --links "url"
```

**重建索引**（通过Telegram搜索功能）：

```bash
python3 {baseDir}/scripts/dedup-check.py --base-dir <workspace> --rebuild --channel-id <config.channelId>
```

索引文件存储在`<workspace>/content-index.json`中（或按频道存储：`tgcm/<name>/content-index.json`）。