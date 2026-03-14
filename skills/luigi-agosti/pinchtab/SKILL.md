---
name: pinchtab
description: "当需要使用 PinchTab 进行浏览器自动化操作时，请使用此技能：打开网站、检查交互式元素、点击页面元素、填写表单、抓取页面文本、使用持久化的用户资料登录网站、导出截图或 PDF 文件、管理多个浏览器实例；或者在 CLI 不可用时，切换到 HTTP API 进行操作。建议在依赖稳定可访问性规范（如 `e5` 和 `e12`）的场景中优先使用此技能，因为它能够更高效地处理浏览器相关任务。"
---
# 使用 PinchTab 进行浏览器自动化操作

PinchTab 为自动化代理提供了一个浏览器工具，支持稳定的可访问性操作、低成本的文本提取功能，以及持久化的配置文件或实例管理。请将其视为一个以命令行界面（CLI）为主导的浏览器操作工具；仅在 CLI 不可用或需要 CLI 中尚未提供的配置管理功能时，才使用其 HTTP API。

**推荐使用方式：**
- 首先使用 `pinchtab` CLI 命令。
- 对于配置文件管理或非 Shell/API 的操作，可以使用 `curl`。
- 当需要从 JSON 响应中提取结构化数据时，可以使用 `jq`。

## 安全默认设置
- 默认目标地址为 `http://localhost`。只有在用户明确提供远程 PinchTab 服务器地址及相应令牌的情况下，才使用远程服务器。
- 建议优先使用只读操作，如 `text`、`snap -i -c`、`snap -d`、`find`、`click`、`fill`、`type`、`press`、`select`、`hover`、`scroll`。
- 除非有更简单的 PinchTab 命令能够完成操作，否则不要执行任意 JavaScript 代码。
- 除非用户指定了上传文件，并且目标操作确实需要上传文件，否则不要上传本地文件。
- 不要将截图、PDF 文件或下载内容保存到任意路径。应使用用户指定的路径或安全的临时工作区路径。
- 绝不要使用 PinchTab 来查看与当前任务无关的本地文件、浏览器设置、存储的凭据或系统配置。

## 核心工作流程
所有 PinchTab 自动化操作都遵循以下步骤：
1. 确保任务所需的服务器、配置文件或实例已准备好。
2. 使用 `pinchtab nav <url>` 或 `pinchtab instance navigate <instance-id> <url>` 进行导航。
3. 使用 `pinchtab snap -i -c`、`pinchtab snap --text` 或 `pinchtab text` 来观察当前页面内容，并获取相关引用（如 `e5`）。
4. 使用 `click`、`fill`、`type`、`press`、`select`、`hover`、`scroll` 等命令与这些引用进行交互。
5. 在页面发生任何变化（如导航、提交、弹出窗口打开、折叠栏展开等导致 DOM 变更后），重新获取页面内容。

**注意事项：**
- 页面内容发生变化后，切勿继续使用过时的引用。
- 如果需要获取页面内容，建议使用 `pinchtab text`；如果需要获取可操作的元素，建议使用 `pinchtab snap -i -c`。
- 仅将截图用于视觉验证、用户界面差异对比或调试目的。
- 在开始多站点或多任务操作前，先选择正确的配置文件或实例。

## 命令链
仅在不需要在决定下一步操作前查看中间结果时，才使用 `&&` 连接多个命令。

**示例：**
- 当需要先读取快照结果时，应分别执行各个命令。

## 认证与状态管理
在开始与网站交互之前，请选择以下五种模式之一：
### 1. 一次性公共浏览
- 对于公共页面、数据抓取或不需要登录持久化的任务，使用临时实例。

### 2. 重用已存在的配置文件
- 对于需要重复访问同一已认证网站的任务，可以使用现有的配置文件。

### 3. 通过 HTTP 创建新的认证配置文件
- 当需要一个持久化的认证配置文件且该配置文件还不存在时，使用此方法。

### 4. 人工辅助的登录流程，随后由代理重复使用该配置文件
- 适用于需要验证码、多因素认证（MFA）或首次设置的情况。

### 5. 通过远程代理或非 Shell 环境使用带令牌的 HTTP API
- 当代理无法直接调用 CLI 时，使用此方法。

### 6. 会话存储后重复使用同一配置文件
- 会话信息存储后，后续任务可重复使用相同的配置文件。

## 常用命令
- **服务器与目标设置：** [命令示例](```bash
pinchtab server
pinchtab daemon
pinchtab health
pinchtab instances
pinchtab profiles
PINCHTAB_URL=http://localhost:9868 pinchtab snap -i -c
```)
- **导航与标签页管理：** [命令示例](```bash
pinchtab nav <url>
pinchtab nav <url> --new-tab
pinchtab nav <url> --tab <tab-id>
pinchtab nav <url> --block-images
pinchtab nav <url> --block-ads
pinchtab tab
pinchtab tab new <url>
pinchtab tab close <tab-id>
pinchtab instance navigate <instance-id> <url>
```)
- **页面内容观察：** [命令示例](```bash
pinchtab snap
pinchtab snap -i
pinchtab snap -i -c
pinchtab snap -d
pinchtab snap --selector <css>
pinchtab snap --max-tokens <n>
pinchtab snap --text
pinchtab text
pinchtab text --raw
pinchtab find <query>
pinchtab find --ref-only <query>
```)

**使用建议：**
- `snap -i -c` 用于查找可操作的页面元素。
- `snap -d` 用于多步骤操作中的页面快照获取。
- `text` 用于阅读文章、仪表板内容或确认信息。
- `find --ref-only` 适用于页面内容较多且已知目标位置的情况。

**交互操作：**
- 对于需要精确输入数据的表单，建议使用 `fill`。
- 仅当网站依赖按键事件时，才使用 `type`。
- 如果点击操作会导致页面导航，建议使用 `click --wait-nav`。
- 在执行点击、按 Enter 键、选择或滚动操作后，如果页面内容可能发生变化，应立即重新获取页面快照。

**高级操作（需明确授权）：**
- 仅在任务确实需要这些功能且更安全的命令无法满足需求时，才使用以下命令：
  - `eval` 用于仅用于读取数据的 DOM 检查。
  - `download` 应优先选择安全的临时路径或工作区路径，而非任意文件系统位置。
  - `upload` 需要用户明确提供的文件路径，或经任务批准使用的路径。

## HTTP API 备用方案
- 当代理无法通过 Shell 进行操作时，或需要创建/修改配置文件，或需要特定实例或标签页相关的功能时，使用 API。

## 常见操作模式
- **打开页面并检查内容：** [命令示例](```bash
pinchtab nav https://pinchtab.com && pinchtab snap -i -c
```)
- **填写并提交表单：** [命令示例](```bash
pinchtab nav https://example.com/login
pinchtab snap -i -c
pinchtab fill e3 "user@example.com"
pinchtab fill e4 "correct horse battery staple"
pinchtab click --wait-nav e5
pinchtab text
```)
- **搜索后快速提取结果页面内容：** [命令示例](```bash
pinchtab nav https://example.com
pinchtab snap -i -c
pinchtab fill e2 "quarterly report"
pinchtab press Enter
pinchtab text
```)
- **在多步骤操作中使用差异快照：** [命令示例](```bash
pinchtab nav https://example.com/checkout
pinchtab snap -i -c
pinchtab click e8
pinchtab snap -d -i -c
```)
- **初始化已认证的配置文件：** [命令示例](```bash
pinchtab profiles
pinchtab instance start --profile work --mode headed
# Human signs in once.
PINCHTAB_URL=http://localhost:9868 pinchtab text
```)
- **为不同网站创建独立实例：** [命令示例](```bash
pinchtab instance start --profile work --mode headless
pinchtab instance start --profile staging --mode headless
pinchtab instances
```)
- 确保每个命令指向相应的 `PINCHTAB_URL`。

## 安全性与令牌管理
- 使用专用的自动化配置文件，而非日常浏览用的配置文件。
- 如果 PinchTab 可通过外部网络访问，必须要求用户提供令牌，并谨慎使用令牌。
- 在使用截图、PDF 文件、执行代码评估或上传文件之前，优先选择 `text`、`snap -i -c`、`snap -d`。
- 对于主要依赖文本内容且不需要视觉资源的操作，使用 `--block-images` 选项。
- 在切换不同账户或环境时，应停止或隔离相关实例。

## 差异检测与验证
- 在长时间运行的操作中，每次状态发生变化后，使用 `pinchtab snap -d` 获取新页面内容。
- 使用 `pinchtab text` 确认操作结果、表格更新或导航结果。
- 仅在需要验证视觉效果、验证码或特定布局变化时，使用 `pinchtab screenshot`。
- 如果某个引用在操作后消失，视为正常现象，应重新获取最新数据。

**参考资料：**
- 命令参考：[commands.md](../../docs/commands.md)
- CLI 使用指南：[cli.md](../../docs/reference/cli.md)
- 配置文件管理：[profiles.md](../../docs/reference/profiles.md)
- 实例管理：[instances.md](../../docs/reference/instances.md)
- 完整 API 文档：[api.md](./references/api.md)
- 环境变量配置：[env.md](./references/env.md)
- 安全策略：[TRUST.md](./TRUST.md)