---
name: notebooklm
description: NotebookLM CLI封装工具通过 `node {baseDir}/scripts/notebooklm.mjs` 提供。该工具可用于身份验证、创建笔记本、进行聊天、管理代码源、记录笔记、实现内容共享以及生成/下载相关成果文件。
---

# NotebookLM CLI Wrapper

## 必需参数
- `node` 和 `notebooklm` 必须已在系统的 PATH 环境变量中。
- NotebookLM CLI 需要经过身份验证（如需要，请运行 `login` 命令）。

## 快速入门
- 包装脚本：`scripts/notebooklm.mjs`（用于调用 NotebookLM CLI）。
- 请从技能（skill）目录中运行该脚本，或使用绝对路径 `{baseDir}`。

```bash
node {baseDir}/scripts/notebooklm.mjs status
node {baseDir}/scripts/notebooklm.mjs login
node {baseDir}/scripts/notebooklm.mjs list
node {baseDir}/scripts/notebooklm.mjs use <notebook_id>
node {baseDir}/scripts/notebooklm.mjs ask "Summarize the key takeaways" --notebook <notebook_id>
```

## 请求与输出
- 命令格式：`node {baseDir}/scripts/notebooklm.mjs <command> [args...]`
- 建议使用 `--json` 选项以获得机器可读的输出格式。
- 对于长时间运行的任务，请使用 `--exec-timeout <seconds>`；`--timeout` 选项用于等待或轮询操作。

## 参考资料
- `references/cli-commands.md`

## 所需资源
- 无额外资源（无文件或库需要下载）。