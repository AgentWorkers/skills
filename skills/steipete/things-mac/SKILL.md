---
name: things-mac
description: 在 macOS 上，可以通过 `things` CLI 来管理 Things 3：通过 URL 方式添加/更新项目及待办事项；从本地 Things 数据库中读取、搜索或列出相关内容。当用户要求 Clawdbot 向 Things 中添加任务、列出收件箱中的任务、今日待办的任务或即将进行的任务、搜索任务，或者查看项目、区域或标签的相关信息时，可以使用该 CLI。
homepage: https://github.com/ossianhempel/things3-cli
metadata: {"clawdbot":{"emoji":"✅","os":["darwin"],"requires":{"bins":["things"]},"install":[{"id":"go","kind":"go","module":"github.com/ossianhempel/things3-cli/cmd/things@latest","bins":["things"],"label":"Install things3-cli (go)"}]}}
---

# Things 3 CLI

使用 `things` 命令可以读取您本地的 Things 数据库（包括收件箱、今日待办事项、搜索结果、项目、区域和标签），并通过 Things 的 URL 方案来添加或更新待办事项。

## 设置
- **推荐安装（适用于 Apple Silicon 系统）：**  
  ```
  GOBIN=/opt/homebrew/bin go install github.com/ossianhempel/things3-cli/cmd/things@latest
  ```
- 如果在读取数据库时遇到错误，请为调用该命令的应用程序授予 **完全磁盘访问权限**（手动运行时在终端中执行；通过 `Clawdbot.app` 运行时则需要授权）。
- **可选：** 设置 `THINGSDB` 变量（或使用 `--db` 参数）来指定您的 `ThingsData-*` 文件夹路径。
- **可选：** 设置 `THINGS_AUTH_TOKEN` 变量，以避免在更新操作时需要手动输入 `--auth-token` 参数。

## 仅读操作（针对数据库）
- `things inbox --limit 50` ：查看收件箱中的所有待办事项
- `things today`：查看今日的待办事项
- `things upcoming`：查看即将到期的待办事项
- `things search "query"`：根据指定条件搜索待办事项
- `things projects`：查看所有项目中的待办事项
- `things areas`：查看特定区域中的待办事项
- `things tags`：查看所有待办事项的标签信息

## 写入操作（通过 URL 方案）
- **建议先进行安全预览：**  
  ```
  things --dry-run add "Title"
  ```
- **添加新待办事项：**  
  ```
  things add "Title" --notes "..." --when today --deadline 2026-01-02
  ```
- **将待办事项置前显示：**  
  ```
  things --foreground add "Title"
  ```

**示例：**
- **添加待办事项：**
  - **基本用法：**  
    ```
  things add "Buy milk"
  ```
  - **带备注：**  
    ```
  things add "Buy milk" --notes "2% off + bananas"
  ```
  - **添加到特定项目/区域：**  
  ```
  things add "Book flights" --list "Travel"
  ```
  - **添加到项目标题下：**  
  ```
  things add "Pack charger" --list "Travel" --heading "Before"
  ```
  - **添加标签：**  
  ```
  things add "Call dentist" --tags "health,phone"
  ```
  - **创建清单：**  
  ```
  things add "Trip prep" --checklist-item "Passport" --checklist-item "Tickets"
  ```
  - **从标准输入添加待办事项（多行输入）：**  
    ```
  cat <<'EOF' | things add -
  ```
    ```
    - 第一行：待办事项标题
    - 第二行：备注
    - EOF
  ```

**示例：**（需要 `THINGS_AUTH_TOKEN` 来执行修改操作）
- **首先获取待办事项的 ID（UUID）：**  
  ```
  things search "milk" --limit 5
  ```
- **设置认证信息：**  
  ```
  THINGS_AUTH_TOKEN = <your_token>
  ```
  或者：
  ```
  things search "milk" --limit 5 --auth-token <your_token>
  ```
- **修改待办事项的标题：**  
  ```
  things update --id <UUID> --auth-token <your_token> "New title"
  ```
- **修改备注：**  
  ```
  things update --id <UUID> --auth-token <your_token> --notes "New notes"
  ```
- **追加/前置备注：**  
  ```
  things update --id <UUID> --auth-token <your_token> --append-notes "..." / --prepend-notes "..."
  ```
- **调整待办事项所属的项目/区域：**  
  ```
  things update --id <UUID> --auth-token <your_token> --list "Travel" --heading "Before"
  ```
- **修改/添加标签：**  
  ```
  things update --id <UUID> --auth-token <your_token> --tags "a,b"
  ```
- **完成/取消待办事项（类似软删除操作）：**  
  ```
  things update --id <UUID> --auth-token <your_token> --completed
  ```
  ```
  ```
  ```
  things update --id <UUID> --auth-token <your_token> --canceled
  ```
- **安全预览：**  
  ```
  things --dry-run update --id <UUID> --auth-token <your_token> --completed
  ```
  ```

**删除待办事项：**
- `things3-cli` 目前不支持直接删除待办事项的功能（没有 `delete` 或 `move-to-trash` 命令）；`things trash` 命令仅用于查看已删除的待办事项列表。
- **建议使用 Things 的用户界面来删除待办事项**，或者通过 `--completed`/`--canceled` 参数将其标记为已完成或已取消。

**注意事项：**
- 该工具仅适用于 macOS 系统。
- `--dry-run` 选项会打印出操作所需的 URL，但不会实际执行操作。