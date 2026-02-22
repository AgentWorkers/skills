---
name: claw-guru
description: OpenClaw专家——适用于任何与OpenClaw相关的问题或故障，包括：配置错误、网关崩溃、网关无法启动、斜杠命令（slash commands）的使用、通道路由（channel routing）、多代理设置（multi-agent setup）、心跳机制（heartbeat）、定时任务（cron jobs）、通道配置（channel setup）、与Discord/Telegram/Slack/iMessage的集成、设备配对（pairing）、身份验证（auth）、节点管理（nodes）、版本升级（version upgrades）、技能功能（skills）、沙箱环境（sandboxing）、模型提供者（model providers）、Webhook的使用、其他相关问题（如“OpenClaw无法正常工作”、“网关崩溃”、“命令未找到”等），以及会话相关问题（session issues）、内存问题（memory issues）、浏览器工具（browser tool）的使用、命令行界面（CLI）的操作、安装流程（installation）、权限设置（permissions）、远程访问（remote access）等。
---
# Claw Guru — OpenClaw 实时支持

OpenClaw 是一个 AI 代理网关，用于将大型语言模型（LLMs）连接到聊天渠道、工具和设备。**切勿依赖记忆中的配置值——务必始终从实时数据源进行验证。**

## 实时数据源（在运行时获取）

| 数据源 | URL |
|--------|-----|
| 文档首页 | `https://docs.openclaw.ai` |
| 文档索引（机器可读格式） | `https://docs.openclaw.ai/llms.txt` |
| 配置参考 | `https://docs.openclaw.ai/gateway/configuration-reference.md` |
| 网关故障排除 | `https://docs.openclaw.ai/gateway/troubleshooting.md` |
| 通用故障排除 | `https://docs.openclaw.ai/help/troubleshooting.md` |
| 常见问题解答 | `https://docs.openclaw.ai/help/faq.md` |
| Doctor 文档 | `https://docs.openclaw.ai/gateway/doctor.md` |
| GitHub 仓库 | `https://github.com/openclaw/openclaw` |
| GitHub 问题报告 | `https://github.com/openclaw/openclaw/issues` |
| 新版本/变更日志 | `https://github.com/openclaw/openclaw/releases` |
| 社区 Discord 频道 | `https://discord.gg/clawd` |
| ClawHub（技能管理） | `https://clawhub.ai` |

对于任何主题，都可以从 `llms.txt` 文件开始查找相应的文档页面。

## 代理工作流程

### 1. 首先收集诊断信息
```bash
openclaw doctor
openclaw gateway status
tail -50 ~/.openclaw/logs/gateway.log
```

### 2. 在提供建议之前先获取相关文档
在 `llms.txt` 中搜索相关主题的关键词 → 获取对应的文档页面 → 以此作为回答的依据。

### 3. 在 GitHub 问题报告中查找具体的错误信息
在 `https://github.com/openclaw/openclaw/issues?q=ERROR_STRING` 中搜索已知的问题及其解决方案。

### 4. 根据安装的版本验证配置信息——切勿仅依赖记忆
```bash
DIST=$(find $(npm root -g)/openclaw/dist ~/.npm*/openclaw/dist 2>/dev/null | head -1)
# Look up any config key:
grep -o 'KEY_NAME.\{0,200\}' "$DIST"/config-*.js | head -10
# Or check the live config reference doc:
# https://docs.openclaw.ai/gateway/configuration-reference.md
```

### 5. 安全的配置修改流程
1. **备份**：`cp ~/.openclaw/openclaw.json ~/.openclaw.json.bak`
2. **修改配置文件**
3. **验证 JSON 格式**：`cat ~/.openclaw/openclaw.json | python3 -m json.tool > /dev/null`
4. **重启服务**：`openclaw gateway restart`
5. **查看日志**：`tail -30 ~/.openclaw/logs/gateway.log`

**重要规则**：
**切勿仅凭记忆提供配置值、默认设置或字段名称**。务必始终根据本地配置文件的结构或实时配置参考文档进行验证。OpenClaw 会频繁发布新版本——过时的建议可能会导致问题。