---
name: remnote
description: 通过 `remnote-cli` 搜索、阅读和编写 RemNote 笔记以及个人知识库中的内容。该工具可用于笔记记录、日志记录、添加标签以及浏览知识库；在创建、更新或记录内容之前需要先进行“确认写入”操作。
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
# 通过 `remnote-cli` 操作 RemNote

当用户希望通过命令行使用 `remnote-cli` 来读取或管理 RemNote 内容时，可以使用此技能。

如果用户需要在整个知识库中进行导航（例如：“这个主题在我的笔记中位于哪里？”、“从顶级笔记树开始”、“映射主要的笔记组”），并且 `remnote-kb-navigation` 已经可用并且针对当前用户进行了定制，那么请优先使用 `remnote-kb-navigation`；否则请返回此技能以获取通用的命令规则和配置信息。如果 `remnote-kb-navigation` 不可用（或仍处于模板/未配置状态），则继续单独使用此技能，并在需要时请求技能定制。

## 示例对话触发语句：
- “检查 RemNote 桥接是否已连接。”
- “在我的 RemNote 中搜索冲刺相关的笔记。”
- “查找标记为 ‘weekly-review’ 的笔记。”
- “根据 ID `<rem-id>` 读取这篇 RemNote。”
- “映射我的整个 RemNote 知识库的顶层结构。”
- “创建一篇标题为 ‘X’ 的 RemNote 笔记。”（需要 `confirm write`）
- “将此内容添加到我的 RemNote 日志中。”（需要 `confirm write`）

## 必备前提条件：
1. RemNote 中已安装了 RemNote 自动化桥接插件。
2. 插件安装路径如下：
   - 通过市场安装的指南：
     `https://github.com/robert7/remnote-mcp-bridge/blob/main/docs/guides/install-plugin-via-marketplace-beginner.md`
   - 本地开发安装的指南：
     `https://github.com/robert7/remnote-mcp-bridge/blob/main/docs/guides/development-run-plugin-locally.md`
3. `remnote-cli` 已安装在运行 OpenClaw 的同一台机器上（推荐安装方式：`npm install -g remnote-cli`）。
4. RemNote 已在浏览器或应用程序中打开（网址：`https://www.remnote.com/`）。
5. `remnote-cli` 守护进程正在运行（使用命令：`remnote-cli daemon start`）。
6. RemNote 的右侧边栏中已打开插件面板，并显示连接状态。

如果缺少任何前提条件，请先停止并完成设置。

## 阅读权限的安全策略：
- 默认操作为只读操作：`status`、`search`、`search-tag`、`read`、`daemon status`。
- 默认情况下，不允许执行修改数据的命令。
- 对于写入操作（`create`、`update`、`journal`），需要用户在同一命令中明确输入 `confirm write`。
- 如果没有输入 `confirm write`，则请求用户确认后才能执行写入操作。

## 命令调用规则（非常重要）：
- 每次执行只能运行一个 `remnote-cli` 命令。
- 直接调用 `remnote-cli`，不要链式调用其他 shell 命令。
- 不要使用 `&&`、`|`、`;`、子shell（`(...)`、命令替换（`$()`）、`xargs` 或 `echo` 等管道操作。
- 错误的用法示例：`remnote-cli daemon status --text && echo '---' && remnote-cli status --text`
- 正确的用法：`remnote-cli daemon status --text`
- 原因：命令链式调用可能会触发执行审批流程，从而破坏自动化流程。

## 写入数据的规则（符合 OpenClaw 的安全策略）：
- 对于写入操作，建议使用基于文件的参数格式：
  - `--content-file <path|->` 用于 `create` 或 `journal`
  - `--append-file <path|->` 或 `--replace-file <path|->` 用于 `update`
- 保持执行的命令字符串简短且易于 OpenClaw 的安全策略识别。
- 不建议直接使用 `--content` 或 `--append` 以及 `journal [content]` 的参数形式，除非是处理非常简短的文本。
- 虽然支持标准输入（`-`，但在 OpenClaw 的使用场景中不推荐，因为这样会导致命令上下文不明确。

## 在实际操作前的兼容性检查：
1. 检查守护进程和桥接的连接状态：
   - `remnote-cli daemon status --text`
2. 确认插件面板已打开并且处于连接状态。
3. 从 `remnote-cli status --text` 中读取以下信息：
   - 活动中的插件版本
   - CLI 版本
   - `version_warning`（如果存在）
   - 写入操作相关的配置选项：`acceptWriteOperations`、`acceptReplaceOperation`
4. 确保插件版本和 `remnote-cli` 的版本相同（建议完全匹配，例如 `0.x` 系列）。
   - 如果版本不匹配：
     - 安装匹配的 CLI 版本：
       - `npm install -g remnote-cli@<plugin-version>`
     - 或者使用相同的小版本号（例如 `0.<minor>.x`）
     - 重新运行 `remnote-cli --version`；如果 `remnote-cli daemon restart` 不可用，则执行以下操作：
       - `remnote-cli daemon stop`
       - `remnote-cli daemon start`
       - `remnote-cli status --text`

## 核心命令：
### 健康状态与连接检查：
- `remnote-cli daemon start`
- `remnote-cli daemon status --text`
- `remnote-cli status --text`

### 只读操作（默认）：
- 搜索笔记：`remnote-cli search "query"`
- 按标签搜索：`remnote-cli search-tag "tag"`
- 根据 Rem ID 读取笔记：`remnote-cli read <rem-id>`
- 可选参数：`--text`（用于以文本形式显示笔记内容）

## 输出格式与遍历策略：
- 默认使用 JSON 格式输出，便于导航、多步数据检索以及需要后续操作的场景。
- 当只需要简单查看单个笔记内容时，可以使用 `--text` 参数。
- 对于结构遍历，建议从浅层读取开始，并设置较低的子节点数量限制：
  - `remnote-cli read <rem-id> --depth 1 --child-limit 500`

### `--include-content` 参数选项：
- `--include-content markdown`：
  - 返回可读的子节点内容（已渲染的形式）。
  - 适用于总结或展示用途。
  - 但这种格式不包含用于进一步导航的子节点 ID。
- `--include-content structured`：
  - 返回包含子节点 ID 的层次化数据结构。
  - 适用于需要明确遍历节点 ID 的场景。

### 修改数据操作（仅在用户确认后执行）：
- 创建新笔记：`remnote-cli create "Title" --content-file /tmp/body.md --text`
- 更新笔记内容：`remnote-cli update <rem-id> --title "New Title" --append-file /tmp/append.md --text`
- 替换笔记内容（具有破坏性，需用户明确授权）：
  - `remnote-cli update <rem-id> --replace-file /tmp/replacement.md --text`
  - `remnote-cli update <rem-id> --replace "" --text`（清除所有直接子节点）
- 记录日志：`remnote-cli journal --content-file /tmp/entry.md --text`
- 不推荐的做法：直接使用参数 `journal [content]`，仅适用于处理非常简短的文本。
- 安全提示：
  - 不要在同一个命令中同时使用 `append` 和 `replace` 参数。
- 只有在 `acceptWriteOperations` 和 `acceptReplaceOperation` 都设置为 `true` 时才能执行替换操作。
- 替换操作具有破坏性，用户必须明确表示同意替换操作。

## 错误处理：
- 如果无法连接到守护进程（退出代码为 `2`），则重新启动守护进程。
- 如果桥接未连接，打开 RemNote 并检查插件面板的状态，然后重新尝试连接。
- 如果版本不匹配，将 `remnote-cli` 的版本更新为与插件匹配的 `0.x` 系列，然后重新启动守护进程。

## 操作注意事项：
- JSON 格式是自动化流程的首选输出格式。
- `--text` 参数适用于快速的人工检查。
- 如有疑问，请参考官方命令文档：`https://github.com/robert7/remnote-cli/blob/main/docs/guides/command-reference.md`