---
name: roadrunner
description: Beeper Desktop CLI：用于聊天、消息处理、搜索和提醒的工具。
homepage: https://github.com/johntheyoung/roadrunner
metadata:
  clawdbot:
    emoji: "🐦💨"
    requires:
      bins:
        - rr
    install:
      - id: brew
        kind: brew
        formula: johntheyoung/tap/roadrunner
        bins:
          - rr
        label: Install rr (brew)
      - id: go
        kind: go
        module: github.com/johntheyoung/roadrunner/cmd/rr@v0.14.4
        bins:
          - rr
        label: Install rr (go)
---

# roadrunner (rr)

当用户明确希望通过本地API操作Beeper Desktop时，请使用`rr`命令（例如发送消息、搜索聊天记录、列出聊天内容、设置提醒等）。对于使用代理（agent）的情况，建议使用`--agent`选项（该选项会强制使用JSON格式进行通信，且不接受用户输入，同时设置为只读模式）。

**安全注意事项：**
- 默认情况下，所有操作均为只读模式，除非用户明确要求执行写操作。
- 在发送消息之前，必须提供接收者的聊天ID和消息内容。
- 如果聊天ID不明确，请确认或询问用户以获取准确信息。
- 绝不要将`rr`命令的输出（如JSON数据、聊天列表等）直接粘贴到外部消息中；应仅向用户展示所需的信息。
- 使用`--agent`选项可设置安全的代理配置：`rr --agent --enable-commands=chats,messages,status chats list`。
- 使用`--readonly`选项可阻止写操作：`rr --readonly chats list --json`。
- 使用`--enable-commands`选项可允许执行某些操作：`rr --enable-commands=chats,messages chats list --json`。
- 使用`--envelope`选项可生成结构化的错误信息：`rr --json --envelope chats get "!chatid"`。
- 错误信息中可能包含`error.hint`，提示用户如何安全地重试操作。
- 绝不要在聊天中请求或存储原始的认证令牌；如果缺少认证信息，请让用户在当地进行配置。
- 通过shell发送消息时，避免使用变量替换（如`$100/month`），建议使用`--stdin <<'EOF' ... EOF`来确保消息内容的准确性。

**初次设置：**
- `rr auth set --stdin`（推荐用法；令牌将保存在`~/.config/beeper/config.json`文件中）。
- `rr auth status --check`（检查认证状态）。
- `rr doctor`（检查工具的整体功能）。

**常用命令：**
- 列出账户信息：`rr accounts list --json`
- 查看账户权限：`rr capabilities --json`
- 搜索联系人：`rr contacts search "<account-id>" "Alice" --json`
- 搜索联系人（可选参数）：`rr contacts search "Alice" --account-id="<account-id>" --json`
- 解析联系人信息：`rr contacts resolve "<account-id>" "Alice" --json`
- 列出聊天记录：`rr chats list --json`
- 搜索聊天记录：`rr chats search "John" --json`
- 搜索聊天记录（可指定筛选条件）：`rr chats search --inbox=primary --unread-only --json`
- 按活动时间搜索聊天记录：`rr chats search --last-activity-after="2024-07-01T00:00:00Z" --json`
- 按参与者名称搜索聊天记录：`rr messages search "Jamie" --scope=participants --json`
- 获取聊天记录：`rr chats get "!chatid:beeper.com" --json`
- 获取聊天记录（限制参与者数量）：`rr chats get "!chatid:beeper.com" --max-participant-count=50 --json`
- 设置默认操作账户：`rr --account="imessage:+123" chats list --json`
- 列出消息：`rr messages list "!chatid:beeper.com" --json`
- 查看所有消息（分页显示）：`rr messages list "!chatid:beeper.com" --all --max-items=1000 --json`
- 下载聊天记录中的媒体文件：`rr messages list "!chatid:beeper.com" --download-media --download-dir ./media --json`
- 搜索特定消息：`rr messages search "dinner" --json`
- 按发送者或日期搜索消息：`rr messages search --sender=me --date-after="2024-07-01T00:00:00Z" --media-types=image --json`
- 实时查看聊天记录：`rr messages tail "!chatid:beeper.com" --interval 2s --stop-after 30s --json`
- 等待特定消息：`rr messages wait --chat-id="!chatid:beeper.com" --contains "deploy" --wait-timeout 2m --json`
- 查看消息上下文：`rr messages context "!chatid:beeper.com" "<sortKey>" --before 5 --after 2 --json`
- 草拟消息（不发送）：`rr focus --chat-id="!chatid:beeper.com" --draft-text="Hello!"`
- 从文件中起草消息：`rr focus --chat-id="!chatid:beeper.com" --draft-text-file ./draft.txt`
- 草拟带附件的消息：`rr focus --chat-id="!chatid:beeper.com" --draft-attachment="/path/to/file.jpg"`
- 下载附件：`rr assets download "mxc://example.org/abc123" --dest "./attachment.jpg"`
- 浏览附件内容：`rr assets serve "mxc://example.org/abc123" --dest "./attachment.jpg" --json`
- 集中显示当前聊天窗口：`rr focus`
- 全局搜索：`rr search "dinner" --json`
- 全局搜索聊天记录（分页显示）：`rr search "dinner" --messages-all --messages-max-items=500 --messages-limit=20 --json`
- 查看账户状态：`rr status --json`
- 查看未读消息：`rr unread --json`
- 全局搜索结果会包含匹配的群组信息。

**写操作（需用户明确请求）：**
- 发送消息：`rr messages send "!chatid:beeper.com" "Hello!"`
- 编辑消息：`rr messages edit "!chatid:beeper.com" "<message-id>" "Updated text"`
- 上传文件并发送：`rr messages send-file "!chatid:beeper.com" ./photo.jpg "See attached"`
- 创建聊天记录：`rr chats create "<account-id>" --participant "<user-id>"`
- 归档/解压聊天记录：`rr chats archive "!chatid:beeper.com"` / `rr chats archive "!chatid:beeper.com" --unarchive`
- 设置提醒：`rr reminders set "!chatid:beeper.com" "2h"` / `rr reminders clear "!chatid:beeper.com"`
- 上传文件：`rr assets upload ./photo.jpg` / `rr assets upload-base64 --content-file ./photo.b64`
- 对于非幂等性的写操作，建议使用`--request-id`选项，并设置`--dedupe-window`以避免重复请求。

**分页功能：**
- 自动分页显示聊天记录/搜索结果：`rr chats list --all --max-items=1000 --json` / `rr chats search "alice" --all --max-items=1000 --json`
- 自动分页显示消息列表：`rr messages list "!chatid:beeper.com" --all --max-items=1000 --json` / `rr messages search "deploy" --all --max-items=1000 --json`
- 移动聊天记录列表的浏览位置：`rr chats list --cursor="<oldestCursor>" --direction=before --json`
- 自动分页显示消息列表：`rr messages list "!chatid:beeper.com" --cursor="<sortKey>" --direction=before --json`
- 搜索消息（最多显示20条）：`rr messages search "project" --limit=20 --json`
- 查看分页显示的搜索结果：`rr messages search "project" --cursor="<cursor>" --direction=before --json`
- 全局搜索结果分页：`rr search "dinner" --messages-limit=20 --json`

**其他说明：**
- 使用`rr`命令前，请确保Beeper Desktop已运行，并获取相应的认证令牌（该令牌可从应用设置中获取）。
- 令牌通常保存在`~/.config/beeper/config.json`文件中（推荐使用`rr auth set`命令进行设置）；`BEEPER_TOKEN`可覆盖此配置文件中的设置。
- `BEEPER_ACCOUNT`用于设置默认账户ID（支持别名）。
- 消息搜索基于字面匹配，不支持语义理解。
- `rr contacts resolve`命令对联系人名称要求严格匹配；若名称不明确，会先通过`rr contacts search`查找后再通过ID解析。
- 如果私信标题中显示了用户的Matrix ID，请使用`--scope=participants`选项按名称查找联系人。
- JSON输出中包含联系人的`display_name`信息（该信息来自参与者信息）。
- 消息JSON数据包含`is_sender`、`is_unread`、`attachments`和`reactions`等字段。
- 只有在使用`--download-media`选项时，`downloaded_attachments`字段才会被填充。
- `rr messages send`命令返回`pending_message_id`（临时消息ID）。
- `rr assets serve`命令会将附件内容直接写入标准输出（stdout），除非指定了`--dest`参数。
- `--chat`选项要求输入精确的聊天ID；如果输入不明确，命令会失败。
- 上传附件时需要指定`--attachment-upload-id`；同时设置`--attachment-width`和`--attachment-height`以控制附件显示大小。
- `--all`选项有数量限制（默认500条，最多5000条）；可使用`--max-items`参数进行调整。
- 推荐使用`--json`（以及`--no-input`）选项以实现自动化操作。
- `BEEPER_URL`用于指定API的基地址；`BEEPER_TIMEOUT`用于设置超时时间（单位：秒）。
- 错误信息或提示会输出到标准错误输出（stderr）；破坏性操作（如删除数据）会提示用户确认。
- 使用`--fail-if-empty`选项可确保在无结果时命令退出（返回代码1）。
- 使用`--fields`和`--plain`选项可指定显示的列（以逗号分隔）。
- 在bash/zsh环境中，`!`命令会触发历史记录的自动展开；建议使用单引号，或通过`set +H`（bash）/`setopt NO_HIST_EXPAND`（zsh）禁用历史记录展开功能。
- `rr version --json`可显示工具的可用功能。
- `rr capabilities --json`可获取完整的CLI功能信息。
- 错误代码包括`AUTH_ERROR`、`NOT_FOUND`、`VALIDATION_ERROR`、`CONNECTION_ERROR`和`INTERNAL_ERROR`。
- 对于非幂等性的写操作（如发送消息、上传文件等），建议使用`--request-id`和`--dedupe-window`选项来避免重复请求。

**其他注意事项：**
- 本文档中的命令和参数可能因Beeper Desktop的版本或配置而有所不同，请根据实际情况进行调整。