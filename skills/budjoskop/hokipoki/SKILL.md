---
name: hokipoki
description: "使用 HokiPoki CLI，无需切换标签页即可切换 AI 模型。当某个 AI 模型无法解决问题时，可以快速在 Claude、Codex 和 Gemini 之间切换。该工具适用于用户希望向不同的 AI 模型求助、获取其他模型的建议、与其他团队成员共享 AI 订阅服务，或管理 HokiPoki 的提供者/监听者模式。触发命令包括：`use codex/gemini for this`、`hop to another model`、`ask another AI`、`get a second opinion`、`switch models`、`hokipoki`、`listen for requests`。"
---

# HokiPoki 技能

通过 HokiPoki P2P 网络将任务路由到不同的 AI CLI（Claude、Codex、Gemini）。API 密钥始终保留在提供者的机器上；仅交换加密后的请求和结果。

## 先决条件

必须安装并登录 HokiPoki CLI：

```bash
npm install -g @next-halo/hokipoki-cli
hokipoki login
```

使用 `hokipoki whoami` 命令进行验证。如果未安装，请指导用户完成安装过程。

## 向其他 AI 请求帮助

向远程 AI 模型发送任务。始终使用 `--json` 选项以确保输出结果可被解析：

```bash
# Specific files
hokipoki request --tool claude --task "Fix the auth bug" --files src/auth.ts --json

# Entire directory
hokipoki request --tool codex --task "Add error handling" --dir src/services/ --json

# Whole project (respects .gitignore)
hokipoki request --tool gemini --task "Review for security issues" --all --json

# Route to a team workspace
hokipoki request --tool claude --task "Optimize queries" --files src/db.ts --workspace my-team --json

# Skip auto-apply (just save the patch)
hokipoki request --tool codex --task "Refactor module" --dir src/ --no-auto-apply --json
```

工具选择：如果用户未指定工具，可以询问用户希望使用哪个模型，或者省略 `--tool` 选项，让 HokiPoki 自动选择。

### 自动应用补丁

当目标目录是一个包含已提交文件的 Git 仓库时，系统会自动应用补丁。如果自动应用失败，应通知用户并建议用户采取相应措施：

```bash
git init && git add . && git commit -m "initial"
```

## 提供者模式（共享你的 AI 资源）

注册并监听来自其他用户的请求：

```bash
# Register as a provider (one-time)
hokipoki register --as-provider --tools claude codex gemini

# Start listening
hokipoki listen --tools claude codex
```

任务在隔离的 Docker 容器中执行（容器具有只读文件系统、临时文件空间（tmpfs）以及自动清理功能）。确保 Docker 已经运行。

## 状态与账户

```bash
hokipoki whoami      # Current user info
hokipoki status      # Account, workspaces, history
hokipoki dashboard   # Open web dashboard in browser
```

## 何时建议切换使用其他 AI 模型

- 用户在多次尝试后仍然无法解决问题
- 用户请求采用不同的方法或新的视角
- 任务涉及某个其他模型更擅长的领域（例如，使用 Codex 处理重复性任务，使用 Gemini 进行复杂场景分析）
- 用户明确要求尝试其他 AI 模型

## 完整命令参考

有关所有 CLI 选项、认证令牌的位置以及高级用法，请参阅 [references/commands.md](references/commands.md)。