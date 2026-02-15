---
name: instapaper
description: "在操作 instapaper-cli（ip）工具或进行故障排除时，以下功能会用到：身份验证、列出/导出/导入书签、批量修改书签、文件夹/高亮内容/文本、选择输出格式（ndjson/json/plain）、基于光标的同步，以及解析 stderr 和 JSON 文件中的退出代码以实现自动化操作。"
---

# Instapaper CLI

## 概述

使用此工具可以通过 `ip` CLI（必须已安装并添加到 `PATH` 环境变量中）来执行 Instapaper 相关操作，特别是在需要可靠的自动化处理、结构化输出或故障排除指导时。

## 安装 CLI

- 使用 Go 安装：`go install github.com/vburojevic/instapaper-cli/cmd/ip@latest`
- 使用 Homebrew 安装：`brew tap vburojevic/tap && brew install instapaper-cli`
- 从源代码编译安装：`go build ./cmd/ip`（之后可以通过 `./ip` 命令使用）

## 工作流程（快速入门）

1. **验证设置**：
   - 确保 `INSTAPAPER_CONSUMER_KEY` 和 `INSTAPAPER_CONSUMER_SECRET` 已设置或在登录时提供。
   - 推荐使用 `--password-stdin` 进行身份验证；切勿将密码存储在本地。
   - 在执行长时间运行的任务之前，先运行 `ip doctor --json`（或 `ip auth status`）以检查配置是否正确。

2. **选择输出格式**：
   - 默认格式为 `--ndjson`（以流式方式输出，每行一个对象）。
  - 使用 `--json` 时，输出为单个对象或紧凑的数组格式。
  - 使用 `--plain` 时，输出为稳定的、基于文本的格式。
  - 使用 `--stderr-json` 可以获取结构化的错误信息；`--progress-json` 适用于长时间运行的任务。

3. **确定性地读取数据**：
   - 使用 `list` 或 `export` 命令，并结合 `--cursor`/`--cursor-dir` 或 `--since/--until` 参数来指定数据范围。
  - 使用 `--updated-since` 可以实现增量同步。
  - 如果 API 不支持客户端过滤功能，可以使用 `--select` 进行过滤。

4. **安全地修改数据**：
   - 尽可能使用 `--dry-run` 或 `--idempotent` 来避免数据冲突。
  - 对于批量操作，可以使用 `--ids` 或 `--stdin`，并考虑使用 `--batch` 选项。
   - 删除操作需要明确的确认提示。

5. **其他功能**：
   - 查看文章的 HTML 内容：`ip text`
   - 管理高亮标记：`ip highlights list/add/delete`
   - 管理文件夹：`ip folders list/add/delete/order`

6. **故障排除**：
  - 使用 `--debug` 查看请求的发送时间和状态。
  - 通过 `--stderr-json` 获取错误信息，并根据返回的 `exit_code` 采取相应的处理措施。

## 命令参考

如需了解具体的命令参数、格式说明或使用示例，请参考以下文档：
- `references/commands.md`：包含身份验证、列表/导出/导入、数据修改、文件夹管理、高亮标记和文本显示等功能的详细命令说明。
- `references/output-and-sync.md`：介绍输出格式、进度显示、参数使用规则以及过滤方法。
- `references/errors.md`：解释了各种错误代码及其含义。

## 注意事项：
- **避免使用 `--format table`**：该格式仅适用于人类阅读，不适合数据解析。
- **处理大量数据时**：使用 `--output` 或 `--output-dir` 以避免对标准输出（stdout）造成压力。
- **在 Windows 上**：建议使用 `--password-stdin` 以避免密码被显示在屏幕上。