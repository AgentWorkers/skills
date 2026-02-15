---
name: skill-sharer
description: 将某项技能公开分享到 Enterprise-Crew-skills GitHub 仓库中。在此过程中，需要删除所有个人信息/安全相关的数据，自动生成一个 README 文件，并更新仓库的索引。
---

# Skill Sharer

该脚本用于将本地技能文件发布到 GitHub 的 `henrino3/Enterprise-Crew-skills` 仓库中。

## 功能说明

1. 将技能文件复制到一个经过清理处理的文件夹中。
2. 删除文件中的个人信息、密码、IP 地址、路径以及认证信息。
3. 为该技能文件生成一个独立的 `README.md` 文件。
4. 更新仓库根目录下的 `README.md` 文件，添加新的技能条目。
5. 提交并推送更改到 GitHub。

## 使用方法

```bash
# Share a skill (interactive — reviews sanitization before pushing)
~/clawd/skills/skill-sharer/scripts/share-skill.sh <skill-folder-path> [--description "Short description"]
```

### 示例

```bash
# Share session-cleaner
~/clawd/skills/skill-sharer/scripts/share-skill.sh ~/clawd/scripts/session-cleaner/ --description "Converts session JSONL to clean markdown"

# Share a skill from the skills directory
~/clawd/skills/skill-sharer/scripts/share-skill.sh ~/clawd/skills/weather/ --description "Get weather forecasts with no API key"
```

## 清理规则

该脚本会删除以下内容：
- **IP 地址**：Tailscale 的 IP 地址、公共 IP 地址、本地 IP 地址（替换为 `<REDACTED_IP>`）
- **包含用户名的路径**：例如 `/home/henrymascot/`、`/home/jamify/` 等，这些路径会被替换为通用路径。
- **API 密钥和令牌**：任何与 “key”/“token”/“secret” 相关的内容都会被删除。
- **电子邮件地址**：真实的电子邮件地址会被替换为 `user@example.com`。
- **SSH 连接字符串**：例如 `ssh user@host` 会被替换为 `ssh user@<your-host>`。
- **包含真实主机名的服务器 URL**：内部 URL 会被替换为占位符。
- **秘密文件引用**：例如 `~/clawd/secrets/*` 会被替换为 `<YOUR_SECRET_FILE>`。
- **Tailscale 服务器的名称**：服务器名称会被替换为占位符。
- **环境变量值**：环境变量的实际值会被删除，仅保留变量名。

## 代理工作流程

当 Henry 请求分享某个技能时，系统会执行以下步骤：
1. **确定** 需要分享的技能文件所在的路径。
2. **运行** `share-skill.sh <path> --description "..."` 命令。
3. **查看** 经过清理处理后的文件内容（脚本会暂停等待用户审核）。
4. **确认** 是否要推送文件到 GitHub。
5. **将** GitHub 的仓库地址告知 Henry。

## 仓库结构

```
Enterprise-Crew-skills/
├── README.md              ← Root index (auto-updated)
├── session-cleaner/
│   ├── README.md
│   └── ...
├── new-skill/
│   ├── README.md
│   └── ...
```