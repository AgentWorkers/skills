---
name: remnote
description: 默认情况下，可以通过 `remnote-cli` 读取/搜索 RemNote 内容；在创建、更新或记录内容之前，需要先确认是否要执行写入操作（即需要用户输入确认信息）。
homepage: https://github.com/robert7/remnote-cli
metadata:
  {
    "openclaw":
      {
        "emoji": "🌀",
        "requires": { "bins": ["remnote-cli"] },
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "remnote-cli",
              "bins": ["remnote-cli"],
              "label": "Install remnote-cli (npm)",
            },
          ],
      },
  }
---
# 通过 `remnote-cli` 使用 RemNote 功能

当用户希望通过命令行（`remnote-cli`）来读取或管理 RemNote 的内容时，可以使用此技能。

如果用户需要在整个知识库中进行导航（例如：“这个主题在我的笔记中位于哪里？”、“从顶级笔记树开始浏览”或“查看主要的笔记组”），并且 `remnote-kb-navigation` 插件可用且已针对当前用户进行了定制，建议优先使用该插件。如果 `remnote-kb-navigation` 不可用（或仍处于模板/未配置状态），则继续使用此技能，并在需要时请求插件定制。

## 示例对话触发场景：
- “检查 RemNote 桥接是否已连接。”
- “在我的 RemNote 中搜索 sprint 相关的笔记。”
- “查找标记为 ‘weekly-review’ 的笔记。”
- “根据 ID `<rem-id>` 读取对应的 RemNote 内容。”
- “查看我的整个 RemNote 知识库的顶层结构。”
- “创建一个标题为 ‘X’ 的新笔记，并输入相应内容。”（需要用户确认是否要写入）
- “将此内容添加到我的 RemNote 日志中。”（需要用户确认是否要写入）

## 必备前提条件：
1. RemNote 中已安装了 RemNote Automation Bridge 插件。
2. 插件安装路径符合以下指南之一：
   - 通过市场places 安装：`https://github.com/robert7/remnote-mcp-bridge/blob/main/docs/guides/install-plugin-via-marketplace-beginner.md`
   - 本地开发环境安装：`https://github.com/robert7/remnote-mcp-bridge/blob/main/docs/guides/development-run-plugin-locally.md`
3. `remnote-cli` 已安装在运行 OpenClaw 的同一台机器上（推荐安装方式：`npm install -g remnote-cli`）。
4. RemNote 已在浏览器或应用程序中打开（访问地址：`https://www.remnote.com/`）。
5. `remnote-cli` 守护进程正在运行（使用命令：`remnote-cli daemon start`）。
6. RemNote 的右侧边栏中已打开插件面板，并显示连接状态。

如果缺少任何前提条件，请先停止操作并完成相应的设置。

## 安全策略（仅限读取操作）：
- 默认情况下，所有操作均为只读模式：`status`、`search`、`search-tag`、`read`、`daemon status`。
- 严禁执行任何会修改数据的命令。
- 对于写入操作（`create`、`update`、`journal`），必须用户明确输入 “confirm write” 的指令。
- 如果未收到确认信息，切勿执行写入操作。

## 命令使用规则（非常重要）：
- 每次执行只能运行一个 `remnote-cli` 命令。
- 直接调用 `remnote-cli`，禁止链式调用其他 shell 命令。
- 禁止使用 `&&`、`|`、`;`、子shell（`(...)`、命令替换（`$()`）、`xargs` 或 `echo` 等操作。
- 错误示例：`remnote-cli daemon status --text && echo '---' && remnote-cli status --text`  
  正确示例：`remnote-cli daemon status --text`  
  原因：命令链式调用可能导致执行流程中断或自动化失败。

## 在实际操作前的兼容性检查：
1. 确认守护进程和桥接服务的连接状态：`remnote-cli daemon status --text`
2. 确认插件面板已打开并且处于连接状态。
3. 通过 `remnote-cli status --text` 查看以下信息：
   - 活动中的插件版本
   - `remnote-cli` 的版本信息
   - 是否存在版本警告（`version_warning`）
4. 遵循版本要求：`remnote-cli` 和桥接插件必须属于同一版本系列（例如 `0.x` 系列，优先选择完全匹配的版本）。
   - 如果版本不匹配：
   - 安装匹配的 `remnote-cli` 版本：`npm install -g remnote-cli@<plugin-version>`
   - 如果无法找到精确匹配的版本，可以安装相同的小版本号（例如 `0.<minor>.x`）。
   - 重新运行 `remnote-cli --version`；如果 `remnote-cli daemon restart` 不可用，执行以下操作：
     - `remnote-cli daemon stop`
     - `remnote-cli daemon start`
     - 再次运行 `remnote-cli status --text`

## 核心命令：
### 健康状态与连接检查：
- `remnote-cli daemon start`
- `remnote-cli daemon status --text`
- `remnote-cli status --text`

### 只读操作（默认）：
- 搜索笔记：`remnote-cli search "query"`
- 按标签搜索：`remnote-cli search-tag "tag"`
- 根据 Rem ID 读取笔记：`remnote-cli read <rem-id>`
- 可选参数 `--text`：用于指定以文本格式显示笔记内容。

## 输出格式与遍历方式：
- 默认输出格式为 JSON，适用于导航、多步骤数据检索以及需要后续操作的场景。
- 当仅需要简单查看单个笔记内容时，使用 `--text` 参数。
- 对于结构化数据的遍历，建议从浅层读取开始，并设置 `--child-limit` 限制（例如：`remnote-cli read <rem-id> --depth 1 --child-limit 500`）。

### `--include-content` 参数：
- `--include-content markdown`：返回可阅读的子节点内容（以 Markdown 格式），适合总结或展示用途。但这种方式无法获取用于进一步导航的子节点 ID。
- `--include-content structured`：返回包含子节点 ID 的结构化数据，适用于需要精确遍历笔记结构的场景。

### 修改操作（仅允许在用户确认写入后执行）：
- 创建新笔记：`remnote-cli create "Title" --content "Body" --text`
- 更新笔记内容：`remnote-cli update <rem-id> --title "New Title" --append "More text" --text`
- 记录日志：`remnote-cli journal "Entry text" --text`

## 错误处理：
- 如果守护进程无法访问（退出代码为 2），请重启守护进程并重试。
- 如果桥接服务未连接，请打开 RemNote 应用程序，检查插件面板的状态并重新尝试连接。
- 如果版本不匹配，请将 `remnote-cli` 的版本更新为与插件匹配的版本（`0.x` 系列），然后重启守护进程。

## 操作注意事项：
- JSON 格式是自动化操作的默认和推荐格式。
- `--text` 参数适用于快速的人工查看。
- 如有疑问，请参考官方文档：`https://github.com/robert7/remnote-cli/blob/main/docs/guides/command-reference.md`