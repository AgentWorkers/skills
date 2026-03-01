---
name: tide-watch
description: >
  OpenClaw 的主动会话容量监控与管理功能：  
  - 在可配置的阈值（75%、85%、90%、95%）达到时发出警告，防止会话窗口卡顿；  
  - 在会话重置前自动备份数据；  
  - 管理会话恢复的提示功能。  
  适用于处理长时间运行的项目、管理多个聊天渠道（如 Discord、Telegram、Webchat）的场景，以及避免因会话窗口完全关闭而导致工作丢失的情况。  
  提供 CLI 工具用于容量检查、跨会话的仪表盘展示、会话存档管理以及会话恢复操作。  
  支持任何模型或聊天服务提供商。
author: Chris Giddings
homepage: https://github.com/chrisagiddings/openclaw-tide-watch
repository: https://github.com/chrisagiddings/openclaw-tide-watch
metadata: {"openclaw":{"emoji":"🌊","version":"1.3.3","disable-model-invocation":false,"capabilities":["session-monitoring","capacity-warnings","session-backup","session-restoration","file-operations-local"],"requires":{"bins":[],"anyBins":["node"],"config":["~/.openclaw/agents/main/sessions/"]},"install":[{"id":"npm","kind":"node","package":".","command":"npm link","bins":["tide-watch"],"label":"Install tide-watch CLI (requires Node.js 14+, optional for Directives-Only mode)"}],"credentials":{"required":false,"types":[],"notes":"No external credentials required. Operates on local OpenClaw session files only."}}}
---
# Tide Watch 🌊  
OpenClaw的主动会话容量监控工具。  

## ⚠️ 安全性与架构说明  

**Tide Watch是一个混合型工具，具有两种运行模式：**  

### 模式1：仅使用指令（推荐给大多数用户）  
**描述：** 仅使用`AGENTS.md`和`HEARTBEAT.md`中的指令  
**代码执行：** **无** – 仅使用OpenClaw内置工具（无需安装CLI）  
**文件访问：** 通过代理内置工具读取OpenClaw会话文件  
**安装：** 将模板指令复制到工作区配置文件中  
**安全性：** 风险最低 – 无需安装或执行任何代码  

**功能：**  
- ✅ 通过`session_status`工具监控会话容量  
- ✅ 在达到75%、85%、90%、95%的阈值时发出警告  
- ✅ 会话重置时自动显示恢复提示  
- ✅ 所有操作均通过OpenClaw的原生工具完成  

### 模式2：使用CLI工具（可选）  
**描述：** 用于手动管理的Node.js命令行工具  
**代码执行：** **是** – 可执行JavaScript代码  
**文件访问：** 直接读写`~/.openclaw/agents/main/sessions/`目录  
**安装：** 使用`git clone`和`npm link`（需要Node.js）  
**安全性：** 中等风险 – 安装前需检查代码  

**功能：**  
- CLI命令：`tide-watch status`、`tide-watch dashboard`等  
- 手动检查会话容量  
- 管理会话存档  
- 编辑恢复提示（⚠️ 请参阅下面的CVE-2026-001）  

### 模式对比  

| 特性 | 仅使用指令 | 使用CLI工具 |  
|---------|-----------------|-----------|  
| **是否需要Node.js？** | ❌ 否 | ✅ 是（版本1.4及以上） |  
| **安装方式** | 复制模板文件 | 使用`npm link` |  
| **代码执行** | ❌ 无 | ✅ JavaScript代码 |  
| **文件访问** | 通过内置工具 | 直接访问文件系统 |  
| **安全风险** | 最低 | 中等 |  
| **适用场景** | 被动监控 | 主动管理 |  

**选择仅使用指令的模式，如果：**  
- 你只需要容量警告和恢复提示功能。  
**选择使用CLI工具的模式，如果：**  
- 你需要手动管理会话、存档或查看仪表板。  

### 🚨 严重安全警告：CVE-2026-001  

**漏洞描述：**  
`editResumePrompt`函数中存在Shell注入漏洞  
**受影响版本：** 仅v1.0.0  
**当前版本：** v1.0.1（已修复）  
**严重程度：** 高（CVSS 7.8）  
**状态：** 已修复  

**总结：** v1.0.0版本中的CLI `resume-prompt edit`命令存在Shell注入漏洞。攻击者可以通过控制`--session`参数执行任意命令。该问题已在v1.0.1版本中通过将`execSync`替换为`spawnSync`得到修复。  

**如果你安装了v1.0.0版本，请立即** 升级到v1.0.1。  
**详细信息：** 查看[SECURITY-ADVISORY-CVE-2026-001.md](./SECURITY-ADVISORY-CVE-2026-001.md)  

### 安全最佳实践  

**对于仅使用指令的模式（最安全）：**  
1. ✅ 将`AGENTS.md.template`和`HEARTBEAT.md.template`复制到工作区  
2. ✅ 无需安装任何代码  
3. ✅ 无npm依赖项  
4. ✅ 安全风险最低  

**对于使用CLI工具的模式（如需使用）：**  
1. ⚠️ **确保使用v1.0.1或更高版本**（`tide-watch --version`）  
2. ⚠️ **安装前检查代码：**  
   - 审查`lib/capacity.js`和`lib/resumption.js`  
   - 确保`package.json`中没有安装钩子  
   - 运行`npm test`测试代码（包含113个测试用例）  
3. ⚠️ **使用UUID作为会话ID**  
4. ⚠️ **避免向CLI命令传递不可信的输入**  
5. ⚠️ **检查备份位置**（`~/.openclaw/agents/main/sessions/archive/`）  

**操作类型：**  

**只读操作（安全，无修改）：**  
- `tide-watch status` – 查看当前会话数量  
- `tide-watch check --session <id>` – 查看特定会话的容量  
- `tide-watch dashboard` – 查看容量概览  
- `tide-watch report` – 列出超过阈值的会话  
- `tide-watch resume-prompt show --session <id>` – 查看恢复提示  

**修改操作（可能修改文件）：**  
- `tide-watch archive --older-than <time>` – 将会话移至存档目录  
- `tide-watch resume-prompt edit --session <id>` – 打开编辑器（v1.0.1版本已修复CVE）  
- `tide-watch resume-prompt delete --session <id>` – 删除恢复提示文件  

**文件系统访问：**  
- 读取：`~/.openclaw/agents/main/sessions/*.jsonl`（会话数据）  
- 写入：`~/.openclaw/agents/main/sessions/resume-prompts/*.md`（恢复提示文件）  
- 移动：`~/.openclaw/agents/main/sessions/archive/`（存档会话）  

**网络活动：** **无** – 所有操作均在本地文件系统内完成。  

### 运行时要求：**  

**模式1（仅使用指令）：**  
- **Node.js**：无需  
- **npm**：无需  
- **依赖项：** 无  
- **二进制文件：** 无  
- **安装：** 将模板文件复制到工作区配置文件  

**模式2（使用CLI工具）：**  
- **Node.js：** v14.0.0或更高版本  
- **npm：** 任意最新版本  
- **依赖项：**  
  - 开发：`jest@^30.2.0`（仅用于测试）  
  - 运行时：无依赖项  
- **二进制文件：** `tide-watch`（通过`npm link`全局安装）  

**为什么没有运行时依赖项？**  
- 仅使用Node.js内置模块（`fs`、`path`、`child_process`）  
- 无需外部API客户端  
- 无网络库  
- 攻击面极小  

**建议：**  
**大多数用户应选择仅使用指令的模式**。这种方式无需安装任何代码即可实现自动容量监控。只有在需要手动管理会话功能时才安装CLI工具。  

## 功能说明：**  
该工具会监控你的OpenClaw会话状态，并在会话容量达到阈值时发出警告：  
- 🟡 **75%** – 提醒你尽快结束当前任务  
- 🟠 **85%** – 建议完成当前任务并重置会话  
- 🔴 **90%** – 会话即将锁定，请立即保存数据  
- 🚨 **95%** – 临界状态！立即保存数据！  

## 安装步骤：**  

### 第1步：在`AGENTS.md`中添加监控指令  
从`AGENTS.md.template`复制指令模板，并将其添加到工作区的`AGENTS.md`文件中：  
```bash
# From your workspace root (~/clawd or similar)
cat skills/tide-watch/AGENTS.md.template >> AGENTS.md
```  

### 第2步：在`HEARTBEAT.md`中添加心跳任务  
从`HEARTBEAT.md.template`复制心跳模板，并将其添加到工作区的`HEARTBEAT.md`文件中：  
```bash
# From your workspace root (~/clawd or similar)
cat skills/tide-watch/HEARTBEAT.md.template >> HEARTBEAT.md
```  

### 第3步：配置设置（可选）  
默认设置适用于大多数用户，但你也可以在`AGENTS.md`中进行自定义：  

- **警告阈值**（何时发出警告）：  
  - 调整百分比（默认：75%、85%、90%、95%）  
  - 范围：50-99%，共2-6个阈值  

- **检查频率**（监控间隔）：  
  - 调整时间间隔（默认：每小时一次）  
  - 选项：15分钟、30分钟、1小时、2小时或“手动”  
  - 范围：5分钟到6小时  

- **自动备份**：  
  - 启用/禁用自动备份（默认：启用）  
  - 设置触发备份的阈值（默认：90%、95%）  
  - 配置备份保留时间（默认：7天）  
  - 启用压缩以节省磁盘空间（默认：关闭）  

- **频道特定设置**（高级选项）：  
  - 为不同频道设置不同的配置（Discord、Webchat、私信）  

## 使用方法：**  
安装完成后，该工具将：  
1. **每小时检查一次会话容量**  
2. **在达到阈值时发出警告**（75%、85%、90%、95%）  
3. **提供建议**：  
  - 将重要数据保存到内存  
  - 切换到使用率较低的频道  
  - 提供会话重置命令  
  - 生成会话恢复提示  

### 手动检查：**  
你可以随时请求我检查会话状态：  
```
What's my current session capacity?
Check context usage
Run session_status
```  

### 重置会话并保留数据：**  
当收到容量过高警告时：  
```
Help me reset this session and preserve context
```  
- 我会：  
  - 将当前工作保存到内存  
  - 备份会话文件（如果尚未备份）  
  - 提供会话恢复提示  
  - 重置会话  

### 从备份中恢复：**  
如果需要恢复之前的会话状态：  
```
Show me available backups for this session
Restore session from 90% backup
```  
- 我会：  
  - 列出可用的备份文件及其时间戳  
  - 恢复选定的备份  
  - 指导你重新连接以加载恢复的会话  

**备份位置：**  
- 路径：`~/.openclaw/agents/main/sessions/backups/`  
- 格式：`<session-id>-<threshold>-<timestamp>.jsonl[.gz`  
- 保留时间：可配置（默认：7天）  

## 工作原理：**  

### 自动监控（心跳机制）：**  
当你将Tide Watch添加到`HEARTBEAT.md`中后，它会自动：  
1. **解析配置**（来自`AGENTS.md`）：  
  - 监控频率  
  - 警告阈值  
  - 备份设置  
  - 查看[PARSING.md]以了解详细的解析逻辑  

2. **按计划检查容量**（默认：每小时一次）：  
  - 运行`session_status`获取令牌使用情况  
  - 计算使用率：`(tokens_used / tokens_max) * 100`  

3. **与阈值比较**：  
  - 使用你配置的阈值（非硬编码默认值）  
  - 确定是否超过阈值  
  - 根据阈值严重程度显示警告（首次警告为🟡，最高为🚨）  

4. **发出警告**：  
  - 对于新达到的阈值发出警告  
  - 记录该会话已收到的警告次数  
  - 如果容量保持不变，则不再重复警告  

5. **自动备份（如果启用）：**  
  - 检查是否超过备份阈值  
  - 创建备份文件：`~/.openclaw/agents/main/sessions/backups/<session-id>-<threshold>-<timestamp>.jsonl`  
  - 验证备份完整性  
  - 记录备份完成情况  
  - 记录备份的阈值  

6. **提供建议**：  
  - 将数据保存到内存  
  - 切换到使用率较低的频道  
  - 提供会话重置命令  
  - 生成会话恢复提示  

7. **清理旧备份**：  
  - 删除超过保留时间的备份文件（默认：7天）  
8. **恢复静默模式**：  
  - 如果容量低于所有阈值，则返回`HEARTBEAT_OK`，不产生任何输出，不打断正常操作  

### 手动检查：**  
你也可以随时请求我进行检查：  
```
What's my current session capacity?
Check context usage
Run session_status
```  

### 主要特点：**  
- **兼容性高**：适用于任何聊天平台（Anthropic、OpenAI、DeepSeek等）  
- **非侵入式**：仅在工作达到阈值时发出警告  
- **可配置**：可根据需求调整阈值、检查和操作方式  
- **状态记录**：记录每次警告的阈值和会话重置情况  

**为什么需要这个工具？**  
**问题：** 会话窗口会逐渐填满，但用户可能毫无察觉。一旦达到100%，会话会锁定并停止响应，导致数据丢失。**  
**解决方案：** 通过主动监控提前发现容量问题，让你有时间保存数据、切换频道或重新开始会话。  

**实际案例：**  
在2026年2月23日，Discord上的#navi-code-yatta频道达到97%的容量上限并锁定，导致会话中断，用户不得不手动重置会话，从而丢失了对话内容。  

## 配置示例：**  
- **保守配置（提前警告）：**  
```markdown
Warning thresholds: 60%, 70%, 80%, 90%
Check frequency: Every 30 minutes
```  
- **激进配置（最大化使用率）：**  
```markdown
Warning thresholds: 85%, 92%, 96%, 98%
Check frequency: Every 2 hours
```  
- **频道特定配置：**  
```markdown
Discord channels: 75%, 85%, 90%, 95% (default)
Webchat: 85%, 95% (lighter warnings)
DM: 90%, 95% (minimal warnings)
```  

**未来功能：**  
- 提供CLI工具以生成容量报告  
- 在达到阈值时自动备份会话  
- 追踪历史容量使用情况  
- 跨会话的容量报告  
- 与心跳监控集成  
- 通过电子邮件/通知发送警告  
- 提供智能的会话切换建议  

**系统要求：**  
- OpenClaw需支持`session_status`工具  
- 工作区需包含`AGENTS.md`文件  
- 代理指令中需包含主动监控配置  

**支持信息：**  
- **仓库：** https://github.com/chrisagiddings/openclaw-tide-watch  
- **问题报告：** https://github.com/chrisagiddings/openclaw-tide-watch/issues  
- **ClawHub：** https://clawhub.ai/chrisagiddings/tide-watch  

**许可证：** MIT