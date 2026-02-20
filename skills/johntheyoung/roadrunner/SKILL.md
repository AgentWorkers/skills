---
name: roadrunner
description: Beeper Desktop CLI（命令行界面）支持聊天、消息、联系人管理、连接信息查看、WebSocket事件处理、搜索以及提醒功能。
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
        module: github.com/johntheyoung/roadrunner/cmd/rr@v0.16.2
        bins:
          - rr
        label: Install rr (go)
---
# roadrunner (rr)

当用户明确希望通过本地API操作Beeper Desktop时（发送消息、搜索聊天记录/消息、列出聊天记录/消息、设置提醒、聚焦聊天等），请使用`rr`命令。  
若需以代理模式使用`rr`，请使用`--agent`选项（该模式强制使用JSON格式进行通信，不接受用户输入，且仅支持读取操作）。

**安全性注意事项：**  
- 除非用户明确要求执行修改操作，否则默认只支持读取操作。  
- 在发送消息前，必须提供接收者（聊天ID）和消息内容。  
- 如果聊天ID不明确，系统会提示用户确认或提供更多信息。  
- 绝不要将`rr`命令的输出（如JSON数据、聊天列表等）直接粘贴到外部消息中；应仅向用户展示所需的信息。  
- 使用`--agent`选项可设置安全的代理行为示例：`rr --agent --enable-commands=chats,messages,status chats list`  
- 使用`--readonly`选项可阻止写入操作：`rr --readonly chats list --json`  
- 使用`--enable-commands`选项可允许某些操作：`rr --enable-commands=chats,messages chats list --json`  
- 使用`--envelope`选项可生成结构化的错误信息：`rr --json --envelope chats get "!chatid"`  
- 错误信息中可能包含`error.hint`，提示用户如何安全地重试操作。  
- 绝不要在聊天中请求或存储原始的认证令牌；如果缺少认证信息，请让用户在当地进行配置。  
- 通过shell发送消息时，避免使用变量替换（如`$100/month`）；建议使用`--stdin <<'EOF' ... EOF`来确保内容的安全性。

**设置（只需执行一次）：**  
- `rr auth set --stdin`（推荐；令牌会保存在`~/.config/beeper/config.json`文件中）  
- `rr auth status --check`  
- `rr doctor`  

**常用命令：**  
- 列出账户：`rr accounts list --json`  
- 查看功能：`rr capabilities --json`  
- 连接元数据：`rr connect info --json`  
- 监听实时WebSocket事件（实验性功能）：`rr events tail --all --stop-after 30s --json`  
- 列出联系人：`rr contacts list "<account-id>" --json`  
- 搜索联系人：`rr contacts search "<account-id>" "Alice" --json`  
- 解析联系人信息：`rr contacts resolve "<account-id>" "Alice" --json`  
- 列出聊天记录：`rr chats list --json`  
- 搜索聊天记录：`rr chats search "John" --json`  
- 搜索聊天记录（可指定筛选条件）：`rr chats search --inbox=primary --unread-only --json`  
- 按活动时间搜索聊天记录：`rr messages search --last-activity-after="2024-07-01T00:00:00Z" --json`  
- 按参与者名称搜索聊天记录：`rr messages search "Jamie" --scope=participants --json`  
- 获取聊天记录内容：`rr chats get "!chatid:beeper.com" --json`  
- 获取聊天记录内容（限制参与者数量）：`rr chats get "!chatid:beeper.com" --max-participant-count=50 --json`  
- 根据联系人信息创建/恢复私信：`rr chats start "<account-id>" --email "alice@example.com" --full-name "Alice" --json`  
- 设置默认操作账户：`rr --account="imessage:+123" chats list --json`  
- 列出消息：`rr messages list "!chatid:beeper.com" --json`  
- 查看所有消息（分页显示）：`rr messages list "!chatid:beeper.com" --all --max-items=1000 --json`  
- 下载消息附件：`rr messages list "!chatid:beeper.com" --download-media --download-dir ./media --json`  
- 搜索消息：`rr messages search "dinner" --json`  
- 添加/删除消息反应：`rr messages react "!chatid:beeper.com" "<message-id>" "👍" --json` / `rr messages unreact "!chatid:beeper.com" "<message-id>" "👍"`  
- 实时查看消息：`rr messages tail "!chatid:beeper.com" --interval 2s --stop-after 30s --json`  
- 等待特定消息：`rr messages wait --chat-id="!chatid:beeper.com" --contains "deploy" --wait-timeout 2m --json`  
- 查看消息上下文：`rr messages context "!chatid:beeper.com" "<sortKey>" --before 5 --after 2 --json`  
- 草拟消息（不发送）：`rr focus --chat-id="!chatid:beeper.com" --draft-text="Hello!"`  
- 从文件起草消息：`rr focus --chat-id="!chatid:beeper.com" --draft-text-file ./draft.txt`  
- 添加附件到消息：`rr focus --chat-id="!chatid:beeper.com" --draft-attachment="/path/to/file.jpg"`  
- 下载附件：`rr assets download "mxc://example.org/abc123" --dest "./attachment.jpg"`  
- 流式传输附件内容：`rr assets serve "mxc://example.org/abc123" --dest "./attachment.jpg" --json`  
- 聚焦当前应用：`rr focus`  
- 全局搜索：`rr search "dinner" --json`  
- 全局搜索消息（分页显示）：`rr search "dinner" --messages-all --messages-max-items=500 --messages-limit=20 --json`  
- 查看账户状态：`rr status --json`  
- 查看未读消息：`rr unread --json`  
- 全局搜索结果包含匹配的群组信息。

**修改操作（仅限用户明确请求）：**  
- 发送消息：`rr messages send "!chatid:beeper.com" "Hello!"`  
- 编辑消息：`rr messages edit "!chatid:beeper.com" "<message-id>" "Updated text"`  
- 对消息添加/删除反应：`rr messages react "!chatid:beeper.com" "<message-id>" "👍"` / `rr messages unreact "!chatid:beeper.com" "<message-id>" "👍"`  
- 上传并发送文件：`rr messages send-file "!chatid:beeper.com" ./photo.jpg "See attached"`  
- 创建聊天记录：`rr chats create "<account-id>" --participant "<user-id>"`  
- 根据联系人信息开始聊天：`rr chats start "<account-id>" --email "alice@example.com" --full-name "Alice"`  
- 归档/解压聊天记录：`rr chats archive "!chatid:beeper.com"` / `rr chats archive "!chatid:beeper.com" --unarchive`  
- 设置提醒：`rr reminders set "!chatid:beeper.com" "2h"` / `rr reminders clear "!chatid:beeper.com"`  
- 上传文件：`rr assets upload ./photo.jpg` / `rr assets upload-base64 --content-file ./photo.b64`  
- 对于非幂等性的写入操作，使用`--request-id`选项，并设置`--dedupe-window`以避免重复请求。

**分页功能：**  
- 自动分页显示聊天记录/消息列表：`rr chats list --all --max-items=1000 --json` / `rr messages search "alice" --all --max-items=1000 --json`  
- 自动分页显示消息列表：`rr messages list "!chatid:beeper.com" --all --max-items=1000 --json`  
- 移动聊天记录列表的查看位置：`rr chats list --cursor="<oldestCursor>" --direction=before --json`  
- 自动分页显示消息列表：`rr messages list "!chatid:beeper.com" --cursor="<sortKey>" --direction=before --json`  
- 搜索消息（最多显示20条）：`rr messages search "project" --limit=20 --json`  
- 分页显示搜索结果：`rr search "dinner" --messages-limit=20 --json`  

**其他说明：**  
- 使用`rr`命令前，确保Beeper Desktop已启动；令牌信息存储在`~/.config/beeper/config.json`文件中（建议使用`rr auth set`命令进行设置）。`BEEPER_TOKEN`可覆盖配置文件中的设置。  
- `BEEPER_ACCOUNT`用于设置默认账户ID（支持别名）。  
- 当支持OAuth认证时，`rr auth status --check`会优先使用`/oauth/introspect`方法；在旧版本中则使用账户列表验证。  
- 消息搜索基于字面匹配，不支持语义搜索。  
- `rr contacts resolve`命令对联系人名称要求严格；若名称不明确，会先通过`contacts search`查找后再通过ID解析。  
- 如果私信标题中显示了用户的Matrix ID，请使用`--scope=participants`选项按名称查找联系人。  
- JSON输出中包含单条聊天的`display_name`信息（从参与者信息中获取）。  
- 消息JSON格式包含`message_type`、`linked_message_id`、`is_sender`、`is_unread`、`attachments`和`reactions`等字段。  
- 仅在使用`--download-media`选项时，`downloaded_attachments`字段才会被填充。  
- `rr messages send`命令返回`pending_message_id`（临时消息ID）。  
- 在较新的API版本中，`account network`字段可能不存在；在这种情况下，输出中会显示`"unknown"`。  
- `rr assets serve`命令会将附件内容直接写入标准输出（stdout）；若未指定`--dest`参数，则会默认输出。  
- `--chat`选项执行精确匹配；若匹配结果不明确，命令会失败。  
- 上传附件时需要指定`--attachment-upload-id`；同时设置`--attachment-width`和`--attachment-height`参数。  
- `--all`选项有数量限制（默认500条，最大5000条）；可使用`--max-items`参数进行调整。  
- 推荐使用`--json`（及`--no-input`）选项以实现自动化操作。  
- `BEEPER_URL`用于指定API的基地址；`BEEPER_TIMEOUT`用于设置请求超时时间（单位：秒）。  
- 错误信息或提示会输出到标准错误流（stderr）。  
- 破坏性操作（如删除数据）在执行前会提示用户确认；`--no-input`或`BEEPER_NO_INPUT`选项会阻止这些操作的执行。  
- 对于列表/搜索命令，使用`--fail-if-empty`选项可确保在无结果时返回错误代码1。  
- 使用`--fields`和`--plain`选项可指定显示的列（以逗号分隔）。  
- 在bash/zsh环境中，`!`命令会触发历史记录的展开；建议使用单引号，或通过`set +H`（bash）/`setopt NO_HIST_EXPAND`（zsh）禁用历史记录展开功能。  
- `rr version --json`可显示工具支持的API功能。  
- `rr capabilities --json`可获取完整的CLI功能元数据。  
- `rr events tail`依赖于Beeper Desktop中的`/v1/ws`接口；若该接口不可用，会切换到`rr messages tail`。  
- 错误代码包括`AUTH_ERROR`、`NOT_FOUND`、`VALIDATION_ERROR`、`CONNECTION_ERROR`、`INTERNAL_ERROR`。  
- 对于非幂等性操作（如发送消息、上传文件等），建议使用`--request-id`和`--dedupe-window`选项来避免重复请求。  
- 可使用`make test-agent-smoke`命令进行本地测试。