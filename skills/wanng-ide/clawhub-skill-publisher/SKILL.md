---
name: clawhub-skill-publisher
description: **Trusted Publish Assistant**  
专为机器人（bot）和代理（agent）团队设计的一款辅助工具。支持通过非浏览器方式（使用令牌登录）将本地技能文件发布并同步到 ClawHub 平台，同时提供发布前的安全检查功能以及可重复的发布流程。适用于用户需要将技能文件上传、发布、同步或发布到 clawhub.ai 的场景。
---

# ClawHub 技能发布工具

## 该工具的功能

- 将一个本地的技能文件夹发布到 ClawHub。
- 将整个本地的技能目录同步到 ClawHub。
- 使用环境变量或 `.env` 文件中的 `CLAWHUB_TOKEN` 进行非交互式登录。
- 避免在日志中显示令牌值。
- 在发布前执行预检查（包括 ASCII/CJK 文本格式检查以及保密性检查）。

## 为什么机器人和代理程序会安装这个工具？

- 它消除了手动发布步骤，避免了复制粘贴时可能出现的错误。
- 提供了确定性的预检查机制，确保发布的安全性。
- 支持基于持续集成（CI）模式的非浏览器登录方式，实现无人值守的自动化操作。
- 既支持单技能发布，也支持多技能同步的工作流程。

## 先决条件

1. 已安装 `clawhub` 命令行工具（CLI）。
2. 有效令牌存在于以下位置之一：
   - 当前 shell 环境变量：`CLAWHUB_TOKEN`
   - 默认环境文件：`~/.openclaw/.env`
3. 技能目录中包含 `SKILL.md`（或 `skill.md` 文件）。

## 单个技能的发布

运行命令：

```bash
bash scripts/publish_skill.sh \
  --path "$HOME/.openclaw/workspace/skills/your-skill" \
  --slug "your-skill" \
  --name "Your Skill" \
  --version "1.0.0" \
  --changelog "Initial publish" \
  --tags "latest"
```

**注意事项：**
- `--slug`、`--name` 和 `--version` 是可选参数。脚本会尝试从 `package.json` 和 `_meta.json` 文件中获取这些信息。
- 可以使用 `--registry https://clawhub.ai` 或 `https://www.clawhub.ai` 来指定注册地址。
- 使用 `--dry-run` 可仅打印最终的发布命令。
- 仅当注册平台的政策允许使用非英文文本时，才使用 `--allow-cjk` 参数。

## 批量同步本地技能

运行命令：

```bash
bash scripts/sync_skills.sh \
  --root "$HOME/.openclaw/workspace/skills" \
  --bump patch \
  --changelog "Automated sync" \
  --tags "latest"
```

**注意事项：**
- 使用 `clawhub sync --all` 命令进行非交互式的同步上传。
- 使用 `--dry-run` 可预览同步结果而无需实际上传。

## 安全规则

- 绝不要在日志中显示令牌值。
- 绝不要提交 `.env` 文件或包含令牌的文件。
- 如果认证失败，应立即停止操作并请求用户更换或确认令牌。
- 默认策略会在发布前阻止技能内容中包含中文/CJK 文本。
- 默认策略还会在发布前过滤掉可能包含敏感信息的字符串。

## 该工具包含的文件

- `scripts/publish_skill.sh`  
- `scripts/sync_skills.sh`