---
name: byr-cli
description: 使用 BYR CLI 进行身份验证、搜索、详细检查以及安全下载 torrent 的计划制定（这些操作均通过 JSON 格式的数据包来完成）。
metadata:
  {
    "openclaw":
      {
        "skillKey": "byr-cli",
        "homepage": "https://clawhub.ai",
        "requires": { "bins": ["byr"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "byr-pt-cli",
              "tap": "1MoreBuild/tap",
              "bins": ["byr"],
              "label": "Install byr CLI (Homebrew)",
            },
            {
              "id": "node",
              "kind": "node",
              "package": "byr-pt-cli",
              "bins": ["byr"],
              "label": "Install byr CLI (npm fallback)",
            },
          ],
      },
  }
---
# BYR CLI 技能

## 使用场景

当需要通过 CLI 执行任何 BYR 操作时，请使用此技能：

- 验证用户身份/检查身份状态
- 使用过滤器搜索种子文件
- 使用过滤器浏览最新的种子文件
- 查看种子文件的详细信息
- 规划或执行种子文件的下载
- 获取种子文件的元数据及用户信息
- 在实际操作前运行本地诊断测试

## 使用限制

- 仅通过 `byr` 二进制文件进行操作。
- 建议使用 `--json` 选项以获取机器可读的输出格式。
- 不要自动补充缺失的 ID 或路径信息，也不要在后台修改文件。
- 保持只读命令的非破坏性特性。

## 身份验证说明

- `auth import-cookie` 支持两种 cookie 格式：
  - `uid=...; pass=...`
  - `session_id=...; auth_token=...`（可选 `refresh_token=...`）
- 浏览器导入支持：
  - `chrome`（macOS 系统的导入/解密流程）
  - `safari`（尽力支持，但可能需手动处理）
- 在执行任何实际操作前，请务必使用 `byr auth status --verify --json` 命令检查身份状态。

## 命令（以 JSON 格式呈现）

**只读命令：**
- `byr check --json`
- `byr whoami --json`
- `byr doctor [--verify] --json`
- `byr browse [--limit <n>] [--category <alias|id>] [--incldead <alias|id>] [--spstate <alias|id>] [--bookmarked <alias|id>] [--page <n>] --json`
- `byr search --query "<text>" --limit <n> --json`
- `byr search --imdb <tt-id> [--category <alias|id>] [--spstate <alias|id>] --json`
- `byr get --id <torrent-id> --json`
- `byr user info --json`
- `byr meta categories --json`
- `byr meta levels --json`
- `byr auth status --verify] --json`
- `byr auth import-cookie --cookie "<cookie-header>" --json`
- `byr auth import-cookie --from-browser <chrome|safari> [--profile <name>] --json`
- `byr auth logout --json`

**写入操作：**
- 先进行模拟运行：`byr download --id <torrent-id> --output <path> --dry-run --json`
- 真正开始下载：`byr download --id <torrent-id> --output <path> --json`

## 搜索/浏览功能说明

- `search` 和 `browse` 命令会返回分页列表数据。
- JSON 数据字段包括：
  - `matchedTotal`：根据 BYR 分页范围估算的总匹配项数。
  - `returned`：当前请求返回的项数。
  - `total`：与 `returned` 具有相同含义的字段（向后兼容）。
- 如果省略 `--page` 参数，命令会自动获取后续页面，直到达到 `--limit` 限制。
- 如果提供了 `--page` 参数，仅获取指定的页面。

## 侧效应处理规则

- 在执行非模拟下载操作（`--dry-run` 除外）之前：
  - 确保 `--id` 和 `--output` 参数已明确指定。
  - 先进行模拟运行并检查 `sourceUrl` 和 `fileName` 的内容。
  - 确认输出路径的用途。

## 错误处理

- 显示错误代码 (`error.code`) 和错误信息 (`error.message`)。
- 对于 `E_ARG_*` 类型的错误，提示用户修正参数。
- 对于 `E_AUTH_*` 类型的错误，提示用户重新进行身份验证或刷新凭证。
- 对于 `E_NOT_FOUND_*` 类型的错误，提示用户重新输入查询内容或种子文件 ID。
- 对于 `E_UPSTREAM_*` 类型的错误，建议用户重试操作并记录相关命令和上下文信息。

## 响应格式

- 保持结果摘要简洁。
- 对于搜索/获取操作，包含关键字段：`id`、`title`、`size`、`seeders`、`leechers`。
- 对于列表操作，当有结果时，同时显示 `matchedTotal` 和 `returned`。
- 对于下载操作，包含关键字段：`outputPath`、`sourceUrl`、`dryRun`、`bytesWritten`。