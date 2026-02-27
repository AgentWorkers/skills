---
name: openclaw-guardian
description: 这是一个为 OpenClaw 开发的安全层插件，它通过两层正则表达式黑名单规则以及基于大型语言模型 (LLM) 的意图验证机制来拦截危险的操作（如执行命令、写入数据或修改文件）。对于关键操作，需要三个大型语言模型的一致性投票才能通过；对于警告级别的操作，则只需要一个大型语言模型的确认即可。99% 的常规操作可以即时完成，且不会产生任何性能开销。该插件还具备绕过攻击/管道攻击的检测功能、路径规范化处理能力、SHA-256 哈希链审计日志记录功能，并能自动从您现有的提供商配置中选择合适的模型进行使用。
---
# OpenClaw Guardian

> 为AI代理提供缺失的安全防护层。

## 为什么需要它？

OpenClaw允许代理直接访问shell、文件、电子邮件、浏览器等资源。其中99%的操作都是无害的，但剩余的1%操作可能包含风险。Guardian能够识别这些风险操作，且不会影响代理的其他正常功能。

## 工作原理

```
Tool Call → Blacklist Matcher (regex rules, 0ms)
              ↓
   No match     → Pass instantly (99% of calls)
   Warning hit  → 1 LLM vote ("did the user ask for this?")
   Critical hit → 3 LLM votes (all must confirm user intent)
```

### 两个级别的黑名单

| 级别 | LLM投票数 | 延迟时间 | 示例操作 |
|-------|-----------|---------|---------|
| 无匹配 | 0 | 约0毫秒 | 读取文件、执行git操作、常规操作 |
| 警告 | 1 | 约1-2秒 | `rm -rf /tmp/cache`、`chmod 777`、`sudo apt` |
| 严重 | 3（一致同意） | 约2-4秒 | `rm -rf ~/`、`mkfs`、`dd of=/dev/`、`shutdown` |

### 检查的内容

系统仅检查三种类型的操作：

- `exec`：命令字符串与黑名单进行匹配；
- `write`/`edit`：文件路径经过规范化处理后与黑名单进行匹配；
- 其他所有操作会立即通过检查。

### LLM意图验证

当黑名单规则被触发时，Guardian会询问一个轻量级的LLM：“用户是否明确请求了这些操作？”系统会读取最近的对话记录以防止误判：

- 警告级别：调用一次LLM进行确认；
- 严重级别：同时调用三次LLM进行确认；如果三次都返回“否”，则阻止操作。

Guardian会自动从您现有的OpenClaw配置中选择一款性能良好且成本较低的模型（推荐使用Haiku模型），无需额外的API密钥。

### LLM备用方案

- 如果LLM无法正常工作，系统会采取安全措施进行阻止；
- 如果LLM无法工作但仅处于警告级别，系统会请求用户手动确认操作。

## 黑名单规则

### 严重级别（exec操作）
- 在系统路径上执行`rm -rf`命令（`/tmp/`和工作区路径除外）；
- 执行`mkfs`或`dd`命令以修改设备；
- 将数据写入`/etc/passwd`、`/etc/shadow`、`/etc/sudoers`文件；
- 执行`shutdown`或`reboot`命令；
- 尝试绕过安全限制（如使用`eval`命令、绝对路径执行命令、通过解释器执行脚本，例如`python -c`或`node -e`）；
- 攻击方式包括管道攻击（`curl | sh`、`wget | bash`、`base64 -d | sh`）和链式攻击（先下载文件再执行`chmod +x`）。

### 警告级别（exec操作）
- 在安全路径上执行`rm -rf`命令；
- 使用`sudo`权限；
- 修改文件权限（`chmod 777`）；
- 更改文件所有者（`chown root`）；
- 安装或卸载软件包；
- 管理系统服务；
- 修改Crontab配置；
- 使用SSH/SCP进行文件传输；
- 执行`kill`或`killall`命令。

### 路径规则（write/edit操作）
- 严重级别：修改系统认证文件（如`/etc/passwd`、`/etc/shadow`）和systemd配置文件；
- 警告级别：修改`.env`文件和SSH密钥文件。

## 审计日志

所有被黑名单拦截的操作都会被记录到`~/.openclaw/guardian-audit.jsonl`文件中，并附有SHA-256哈希值。这种日志记录方式可以防止篡改，每个日志条目都包含了操作内容及其之前的哈希值。

## 安装方法

```bash
openclaw plugins install openclaw-guardian
```

或者也可以手动安装：

```bash
cd ~/.openclaw/workspace
git clone https://github.com/fatcatMaoFei/openclaw-guardian.git
```

## 成本计算

| 操作类型 | 占操作总数的百分比 | 额外成本（以令牌计） |
|----------|----------|------------|
| 无匹配 | 约99% | 0 |
| 警告 | 约0.5-1% | 约500令牌 |
| 严重 | 小于0.5% | 约1500令牌 |

系统优先选择性能较低但成本较低的LLM模型（如Haiku、GPT-4o-mini、Gemini Flash）。

## 文件结构

```
extensions/guardian/
├── index.ts                # Entry — registers before_tool_call hook
├── src/
│   ├── blacklist.ts        # Two-tier regex rules (critical/warning)
│   ├── llm-voter.ts        # LLM intent verification
│   └── audit-log.ts        # SHA-256 hash-chain audit logger
├── test/
│   └── blacklist.test.ts   # Blacklist rule tests
├── openclaw.plugin.json    # Plugin manifest
└── default-policies.json   # Enable/disable toggle
```

## 许可证

MIT许可证