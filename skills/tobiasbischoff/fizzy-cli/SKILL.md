---
name: fizzy-cli
description: 使用 `fizzy-cli` 工具，可以从命令行对 Fizzy 的看板（kanban boards）、卡片（cards）、注释（comments）、标签（tags）、列（columns）、用户（users）以及通知（notifications）进行身份验证和管理。当您需要列出、创建、更新或删除 Fizzy 资源，或者需要编写 Fizzy 工作流程的脚本时，请使用此工具。
metadata:
  author: tobiasbischoff
  version: "1.0"
---

# Fizzy CLI 技能

使用此技能可以通过 `fizzy-cli` 命令来操作 Fizzy 卡板（kanban）系统。它涵盖了身份验证、配置以及常见的 CRUD（创建、读取、更新、删除）操作。

## 快速入门

1) **身份验证**
- **使用令牌：**
  ```
  fizzy-cli auth login --token $FIZZY_TOKEN
  ```
- **使用邮箱：**
  ```
  fizzy-cli auth login --email user@example.com
  ```
  - 如果是非交互式操作，可以使用 `--code ABC123` 作为密码。

2) **设置默认值**
- **仅设置账户信息：**
  ```
  fizzy-cli account set 897362094
  ```
- **设置基础 URL 和账户信息：**
  ```
  fizzy-cli config set --base-url https://app.fizzy.do --account 897362094
  ```

3) **验证访问权限：**
  ```
  fizzy-cli auth status
  ```
  ```
  fizzy-cli account list
  ```

## 常见任务

### 卡板（Boards）
- **列出所有卡片：**
  ```
  fizzy-cli board list
  ```
- **创建新卡片：**
  ```
  fizzy-cli board create --name "Roadmap"
  ```
- **更新卡片信息：**
  ```
  fizzy-cli board update <board-id> --name "New name"
  ```
- **删除卡片：**
  ```
  fizzy-cli board delete <board-id>
  ```

### 卡片（Cards）
- **列出指定卡板的卡片：**
  ```
  fizzy-cli card list --board-id <board-id>
  ```
- **创建新卡片：**
  ```
  fizzy-cli card create --board-id <board-id> --title "Add dark mode" --description "Switch theme"
  ```
- **上传图片：**
  ```
  fizzy-cli card create --board-id <board-id> --title "Add hero" --image ./hero.png
  ```
- **更新卡片信息：**
  ```
  fizzy-cli card update <card-number> --title "Updated" --tag-id <tag-id>
  ```
- **将卡片状态改为“Not Now”：**
  ```
  fizzy-cli card not-now <card-number>
  ```
- **关闭/重新打开卡片：**
  ```
  fizzy-cli card close <card-number>
  fizzy-cli card reopen <card-number>
  ```
- **对卡片进行分类/取消分类：**
  ```
  fizzy-cli card triage <card-number> --column-id <column-id>
  fizzy-cli card untriage <card-number>
  ```

### 评论（Comments）
- **列出所有评论：**
  ```
  fizzy-cli comment list <card-number>
  ```
- **创建新评论：**
  ```
  fizzy-cli comment create <card-number> --body "Looks good"
  ```

### 标签（Tags）、列（Columns）、用户（Users）和通知（Notifications）
- **列出所有标签：**
  ```
  fizzy-cli tag list
  ```
- **列出指定卡板的列：**
  ```
  fizzy-cli column list --board-id <board-id>
  ```
- **列出所有用户：**
  ```
  fizzy-cli user list
  ```
- **列出未读通知：**
  ```
  fizzy-cli notification list --unread
  ```

## 输出格式
- **默认格式：** 人类可读的表格形式。
- **机器可读格式：**
  - `--json`：获取原始的 API JSON 数据。
  - `--plain`：以纯文本形式输出。

## 配置与身份验证注意事项
- **配置文件：** `~/.config/fizzy/config.json`
- **环境变量：** `FIZZY_BASE_URL`, `FIZZY_TOKEN`, `FIZZY_ACCOUNT`, `FIZZY_CONFIG`
- **优先级：** 命令行参数 > 环境变量 > 配置文件 > 默认值。

## 故障排除
- 如果身份验证失败，请运行 `fizzy-cli auth status` 并重新登录。
- 如果账户信息缺失，可以使用 `fizzy-cli account set <slug>` 或 `fizzy-cli config set --account <slug>` 进行设置。
- 使用 `fizzy-cli --help` 或 `fizzy-cli help <command>` 查看完整的使用说明。