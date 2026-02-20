---
name: abaddon
description: OpenClaw的“红队安全模式”（Red Team Security Mode）可根据需求或夜间自动运行对抗性审计。该模式会检查系统中的暴露端口、凭证泄露情况、文件权限设置、可疑进程以及OpenClaw自身的配置安全状况，并给出相应的评分（以字母等级表示）。该功能专为macOS环境设计。
---
# Abaddon ⚔️

大多数安全审计都是防御性的——它们检查你已经采取了哪些防护措施。而Abaddon的运作方式则截然不同：它以攻击者的视角来思考问题，寻找对手可能会发现的问题，而不仅仅是那些你记得需要检查的内容。

你可以根据需要随时运行Abaddon，或者设置它在每晚3:45 AM自动执行。每次运行后，系统都会得到一个评分（用字母等级表示）。

## Abaddon的检查内容

**网络与暴露风险**
- 监听端口：任何绑定到0.0.0.0的端口都会被标记为风险点。
- 网关绑定：应仅允许本地连接（loopback）。
- SSH远程登录状态。
- 活动的隧道（如ngrok、cloudflared）以及未经授权的远程访问。
- 防火墙设置及隐藏模式（stealth mode）的使用情况。

**系统完整性**
- SIP协议、FileVault加密机制、Gatekeeper安全组件的状态。
- macOS的系统版本及待更新的软件。
- XProtect/MRT（Malware Removal Tool）的定义文件是否过时。

**OpenClaw配置**
- 执行安全模式（full、allowlist、deny）的设置。
- 网关身份验证是否启用？
- 是否存在异常的cron任务？
- 是否安装了未经授权的插件？

**文件权限**
- `SOUL.md`和`AGENTS.md`文件必须由root用户拥有，并且权限设置为444。
- `MEMORY.md`、`USER.md`、`AGENT_PROMPT.md`、`openclaw.json`、`cron/jobs.json`以及`LaunchAgent`相关文件应设置为权限600。
- 确保敏感路径上的文件权限不会被设置为644或更宽松的权限。
- 对工作区内的所有文件进行明文密钥扫描。

**API密钥管理**
- API密钥是存储在Keychain中还是普通文件中？
- 是否有密钥通过环境变量泄露？
- 代码历史记录中是否包含敏感信息？
- `.zshrc`文件中是否存在硬编码的API密钥？

**代理行为**
- 检查是否存在内存注入行为（例如：尝试在内存文件中注入命令）。
- 代理的权限设置是否异常。
- 是否存在未经授权的子代理（sub-agent）。

**依赖项**
- 如果使用了Homebrew，需要检查`openclaw`、`ollama`、`node`等依赖包是否过时。

## 评分标准**

| 评分 | 检查项目 |
|------|--------|
| A    | 0个严重漏洞（CRITICAL），0个高风险漏洞（HIGH） |
| B    | 0个严重漏洞，1–2个高风险漏洞（HIGH） |
| C    | 1个严重漏洞或3个以上高风险漏洞（HIGH） |
| D    | 2个以上严重漏洞（HIGH） |
| F    | 存在明显的系统被入侵的迹象（ACTIVE COMPROMISE） |

## 安装步骤

### 第一步：将Abaddon的命令行提示添加到你的代理程序中

如果你使用了Gideon（OpenClaw的监控代理），请添加相应的代码段：
```bash
cat skills/abaddon/templates/abaddon-prompt.md >> ~/.openclaw/workspace/agents/observer/AGENT_PROMPT.md
```

如果你没有使用Gideon，可以使用独立的代理程序命令：
```bash
cp skills/abaddon/templates/abaddon-prompt.md ~/.openclaw/workspace/agents/abaddon/AGENT_PROMPT.md
```

### 第二步：添加夜间定时任务

在`~/.openclaw/cron/jobs.json`文件中添加一个定时任务，使其在每晚3:45 AM（CST时间）执行。如果配置了，结果会发送到Telegram的安全主题中。

### 第三步：保护代理程序的命令行提示文件

你的检测脚本必须设置为只有授权用户才能访问。

## 使用方法

**手动触发**：
- 可以输入以下命令来运行Abaddon：
  - `run red team`
  - `run Abaddon`
  - `run full assessment`
  - `Abaddon report`

**自动执行**：
- Abaddon会在每晚3:45 AM（CST时间）自动执行，此时系统已经完成了标准的防御性审计。

## 执行结果

每次运行Abaddon后，会生成两份报告：
1. **技术报告**：保存在`memory/audits/abaddon-YYYY-MM-DD.md`文件中，包含完整的命令执行记录、发现的问题及相应的修复建议。
2. **总结报告**：以字母等级的形式发布到Telegram的安全主题中。

**特别说明**：
- 严重漏洞（CRITICAL）会立即触发私信提醒。

**注意事项**：
- Abaddon专为macOS（Darwin arm64架构）设计。大多数检查功能在Linux系统上也可以使用，但可能需要调整路径相关设置。
- 假设OpenClaw网关是在本地运行的；如果是在远程环境中部署，可能需要调整端口绑定相关的检查规则。
- Abaddon可以与`enoch-tuning`工具配合使用：安装完成后运行`lock-identity.sh`命令，以一次性设置所有文件的权限基准。