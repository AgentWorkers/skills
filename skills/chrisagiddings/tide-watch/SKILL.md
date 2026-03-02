---
name: tide-watch
description: >
  OpenClaw 的主动会话容量监控与管理功能：  
  - 在可配置的阈值（75%、85%、90%、95%）达到时发出警告，以防止会话窗口卡顿；  
  - 在会话重置前自动备份会话数据；  
  - 管理会话恢复的提示机制。  
  适用于以下场景：  
  - 处理耗时较长的项目；  
  - 管理多个聊天渠道（如 Discord、Telegram、Webchat）；  
  - 防止因会话窗口完全关闭而导致工作丢失。  
  该功能提供以下工具：  
  - 命令行界面（CLI）工具，用于检查会话容量；  
  - 跨会话的仪表盘，便于实时监控会话状态；  
  - 会话存档管理功能；  
  - 会话恢复功能。  
  支持与任何模型或服务提供商配合使用。
author: Chris Giddings
homepage: https://github.com/chrisagiddings/openclaw-tide-watch
repository: https://github.com/chrisagiddings/openclaw-tide-watch
metadata: {"openclaw":{"emoji":"🌊","version":"1.3.6","disable-model-invocation":false,"capabilities":["session-monitoring","capacity-warnings","session-backup","session-resumption","multi-agent-support","auto-detection","file-operations-local"],"requires":{"bins":[],"anyBins":["node"],"config":["~/.openclaw/agents/main/sessions/"],"env":{"optional":["OPENCLAW_SESSION_ID"],"notes":"OPENCLAW_SESSION_ID is optional for auto-detection in CLI mode (v1.3.4+). Not required for Directives-Only mode."}},"install":[{"id":"npm","kind":"node","package":".","command":"npm link","bins":["tide-watch"],"label":"Install tide-watch CLI (requires Node.js 14+, optional for Directives-Only mode)"}],"credentials":{"required":false,"types":[],"notes":"No external credentials required. Operates on local OpenClaw session files only."}}}
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
- ✅ 会话重置时自动加载恢复提示  
- ✅ 所有操作均通过OpenClaw的原生工具完成  

### 模式2：使用CLI工具（可选）  
**描述：** 用于手动管理的Node.js命令行工具  
**代码执行：** **有** – 可执行的JavaScript代码  
**文件访问：** 直接读写`~/.openclaw/agents/main/sessions/`目录  
**安装：** 使用`git clone`和`npm link`（需要Node.js）  
**安全性：** 中等风险 – 安装前需检查代码  

**功能：**  
- CLI命令：`tide-watch status`、`tide-watch dashboard`等  
- 手动检查会话容量  
- 管理会话存档  
- 编辑恢复提示（⚠️ 请参阅下面的CVE-2026-001漏洞）  

### 模式比较  

| 特性 | 仅使用指令 | 使用CLI工具 |  
|---------|-----------------|-----------|  
| **是否需要Node.js？** | ❌ 否 | ✅ 是（14.0.0及以上版本） |  
| **安装方式** | 复制模板文件 | 使用`npm link` |  
| **代码执行** | 无 | ✅ JavaScript代码 |  
| **文件访问** | 通过内置工具 | 直接访问文件系统 |  
| **安全风险** | 最低 | 中等 |  
| **适用场景** | 被动监控 | 主动管理 |  

**选择仅使用指令的模式，如果：**  
你只需要容量警告和恢复提示功能。  
**选择使用CLI工具的模式，如果：**  
你需要手动管理会话、存档或查看仪表盘数据。  

### 🚨 严重安全警告：CVE-2026-001  

**漏洞描述：**  
`editResumePrompt`函数中存在Shell注入漏洞  
**受影响版本：** 仅v1.0.0  
**当前版本：** v1.0.1（已修复）  
**严重程度：** 高（CVSS 7.8）  
**状态：** 已修复  

**总结：**  
v1.0.0版本中，`editResumePrompt`命令存在Shell注入漏洞。攻击者可以通过控制`--session`参数来执行任意命令。该问题已在v1.0.1版本中通过将`execSync`替换为`spawnSync`得到修复。  

**如果你安装了v1.0.0版本：** **请立即更新到v1.0.1。**  
**详细信息：** 请参阅[SECURITY-ADVISORY-CVE-2026-001.md](./SECURITY-ADVISORY-CVE-2026-001.md)  

### 安全最佳实践  

**对于仅使用指令的模式（最安全）：**  
1. ✅ 将`AGENTS.md.template`和`HEARTBEAT.md.template`复制到工作区。  
2. ✅ 无需安装任何代码。  
3. ✅ 无需依赖npm包。  
4. ✅ 安全风险最低。  

**对于使用CLI工具的模式（如需）：**  
1. ⚠️ **确保使用v1.0.1或更高版本**（使用`tide-watch --version`确认）。  
2. ⚠️ **安装前检查代码：**  
   - 审查`lib/capacity.js`和`lib/resumption.js`文件。  
   - 确保`package.json`中没有安装脚本。  
   - 运行`npm test`测试代码功能（共113个测试用例）。  
3. ⚠️ **使用UUID作为会话ID**。  
4. ⚠️ **避免向CLI命令传递不可信的输入。**  
5. ⚠️ **检查备份文件的位置**（`~/.openclaw/agents/main/sessions/archive/`）。  

**操作类型：**  

**只读操作（安全，无修改）：**  
- `tide-watch status` – 查看当前会话数量。  
- `tide-watch check --session <id>` – 查看特定会话的容量。  
- `tide-watch check --current` – 自动检测并检查当前会话（v1.3.4及以上版本）。  
- `tide-watch dashboard` – 提供会话容量概览。  
- `tide-watch dashboard --watch` – 实时更新仪表盘数据。  
- `tide-watch dashboard --raw-size` – 显示精确的令牌数量（v1.3.2及以上版本）。  
- `tide-watch report` – 列出超过阈值的会话。  
- `tide-watch resume-prompt show --session <id>` – 查看恢复提示。  

**修改操作（可能修改文件）：**  
- `tide-watch archive --older-than <时间>` – 将会话移至存档目录（基于时间）。  
- `tide-watch archive --session <id>` – 存档特定会话（v1.3.3及以上版本）。  
- `tide-watch archive --session <id1> --session <id2>` – 同时存档多个会话（v1.3.3及以上版本）。  
- `tide-watch resume-prompt edit --session <id>` – 打开编辑器（CVE已在v1.0.1版本中修复）。  
- `tide-watch resume-prompt delete --session <id>` – 删除恢复提示文件。  

**新功能（v1.3.2及以上版本）：**  
- `--raw-size` – 显示精确的令牌数量（例如`18,713/128,000`）。  
- `--current` – 通过`OPENCLAW_SESSION_ID`环境变量自动检测当前会话（v1.3.4及以上版本）。  
- `--session` – 支持部分UUID、多个会话的存档操作（v1.3.3及以上版本）。  

**文件系统访问：**  
- 读取：`~/.openclaw/agents/main/sessions/*.jsonl`（会话数据）。  
- 写入：`~/.openclaw/agents/main/sessions/resume-prompts/*.md`（恢复提示文件）。  
- 移动：`~/.openclaw/agents/main/sessions/archive/`（存档会话）。  

**网络活动：** **无** – 所有操作均在本地文件系统内完成。  

### CLI参考  

**完整参数和选项说明：**  
- **显示选项：**  
  - `--raw-size` – 以逗号显示精确的令牌数量（v1.3.2及以上版本）  
    - 默认：人类可读格式（例如`18.7k/128k`）。  
    - 使用该参数时：显示精确数量（例如`18,713/128,000`、`20,631/1,000,000`）。  
    - 适用场景：需要精确的令牌数量时。  
    - 例：`tide-watch dashboard --raw-size`。  
  - `--json` – 以JSON格式输出（而非表格格式）。  
    - 例：`tide-watch check --session abc123 --json`。  
    - 适用于脚本编写和数据解析。  
  - `--pretty` – 以美观格式输出JSON（需要`--json`参数）。  
    - 例：`tide-watch report --json --pretty`。  
- **会话选择：**  
    - `--session <key>` – 指定目标会话（v1.3.3及以上版本）。  
    - 完整UUID：`--session 17290631-42fe-40c0-bd23-c5da511c6f7b`。  
    - 部分UUID：`--session 17290631-4`（v1.3.3及以上版本）。  
    - 标签：`--session "#navi-code-yatta"`（v1.3.3及以上版本）。  
    - 频道：`--session discord`（v1.3.3及以上版本）。  
    - 频道+标签：`--session "discord/#navi-code"`（v1.3.3及以上版本）。  
    - 多个会话：`--session abc123 --session def456`（仅用于存档）。  
  - `--current` – 通过`OPENCLAW_SESSION_ID`环境变量自动检测当前会话（v1.3.4及以上版本）。  
    - 适用场景：进行心跳监控（检查当前会话）。  
    - 如果环境变量未设置，会显示友好提示。  
- **过滤：**  
    - `--all` – 显示所有会话（不考虑容量）。  
    - `--threshold <数字>` – 过滤超过指定阈值的会话（默认：75%）。  
    - `--active <小时>` – 仅显示过去N小时内活跃的会话。  
    - `--agent <id>` – 过滤特定代理（多代理环境）。  
    - `--exclude-agent <id>` – 排除特定代理（可多次使用）。  
- **存档选项：**  
    - `--older-than <时间>` – 将超过指定时间的会话存档（例如`4d`、`2w`、`1mo`、`3months`）。  
    - 与`--session`参数互斥使用。  
    - `--dry-run` – 预览存档内容（不进行实际操作）。  
    - 例：`tide-watch archive --older-than 7d --dry-run`。  
    - `--exclude-channel <名称>` – 从存档中排除指定频道。  
    - 例：`tide-watch archive --older-than 30d --exclude-channel discord`。  
    - `--min-capacity <数字>` – 仅存档容量低于指定阈值的会话（例如`tide-watch archive --older-than 7d --min-capacity 50`）。  
- **实时监控：**  
    - `--watch` – 实时更新仪表盘数据（每10秒更新一次）。  
    - 例：`tide-watch dashboard --watch`。  
    - 按Ctrl+C退出实时监控。  
- **多代理：**  
    - `--all-agents` – 多代理发现模式（默认，自动检测代理）。  
    - `--single-agent-only` – 仅针对单个代理（仅显示该代理的会话）。  
- **配置覆盖：**  
    - `--refresh-interval <秒数>` – 仪表盘更新间隔（1-300秒）。  
    - `--gateway-interval <秒数>` – 网关状态检查间隔（5-600秒）。  
    - `--gateway-timeout <秒数>` – 网关命令超时时间（1-30秒）。  
    - `--session-dir <路径>` – 自定义会话目录。  

**使用示例：**  
```bash
# Human-readable vs full precision
tide-watch dashboard                    # 18.7k/128k (easy to scan)
tide-watch dashboard --raw-size         # 18,713/128,000 (exact)

# Auto-detect current session (v1.3.4+)
export OPENCLAW_SESSION_ID="17290631-4"
tide-watch check --current              # Check THIS session
tide-watch check --current --json       # JSON for heartbeat scripts

# Session-specific archiving (v1.3.3+)
tide-watch archive --session abc123 --dry-run    # Preview
tide-watch archive --session abc123              # Archive one
tide-watch archive --session a --session b       # Archive multiple

# Partial ID matching (v1.3.3+)
tide-watch check --session 17290631-4   # Matches 17290631-42fe-40c0-...

# Multi-agent filtering
tide-watch dashboard --agent kintaro    # Kintaro sessions only
tide-watch report --exclude-agent main  # All except main
```  

### 运行时要求：**  
**模式1（仅使用指令）：**  
- **Node.js**：不需要。  
- **npm**：不需要。  
- **依赖项：** 无。  
- **二进制文件：** 无。  
- **安装：** 将模板文件复制到工作区配置文件中。  

**模式2（使用CLI工具）：**  
- **Node.js**：需要v14.0.0或更高版本。  
- **npm**：任意最新版本。  
- **依赖项：**  
  - 开发阶段：`jest@^30.2.0`（仅用于测试）。  
  - 运行时：无依赖项（无生产环境依赖）。  
- **二进制文件：** `tide-watch`（通过`npm link`全局安装）。  

**为什么没有运行时依赖项？**  
- 仅使用Node.js内置模块（`fs`、`path`、`child_process`）。  
- 不使用外部API客户端或网络库，因此攻击面极小。  

**建议：**  
**大多数用户应选择仅使用指令的模式**。** 这种方式无需安装任何代码即可实现自动容量监控。只有在需要手动管理会话时才安装CLI工具。  

## 功能说明：**  
该工具会监控你的OpenClaw会话状态，并在会话容量达到阈值时发出警告：  
- 🟡 **75%** – 提醒你尽快结束当前任务。  
- 🟠 **85%** – 建议完成当前任务并重置会话。  
- 🔴 **90%** – 会话即将锁定，建议立即重置。  
- 🚨 **95%** – 会话即将锁定，立即保存数据！  

## 安装步骤：**  
### 第1步：在`AGENTS.md`中添加监控指令**  
将`AGENTS.md.template`中的指令模板复制到工作区的`AGENTS.md`文件中：  
```bash
# From your workspace root (~/clawd or similar)
cat skills/tide-watch/AGENTS.md.template >> AGENTS.md
```  

或者手动添加相应的监控配置。  

### 第2步：在`HEARTBEAT.md`中添加心跳任务**  
将`HEARTBEAT.md.template`中的心跳配置模板复制到工作区的`HEARTBEAT.md`文件中：  
```bash
# From your workspace root (~/clawd or similar)
cat skills/tide-watch/HEARTBEAT.md.template >> HEARTBEAT.md
```  

或者手动添加Tide Watch的相关配置。  

### 第3步：配置设置（可选）**  
默认设置适用于大多数用户，但你也可以在`AGENTS.md`中进行自定义：  
- **警告阈值**：设置警告的百分比（默认：75%、85%、90%、95%）。  
- **检查频率**：设置监控间隔（默认：每小时一次）。  
  - 选项：15分钟、30分钟、1小时、2小时或“手动”。  
- **自动备份**：启用/禁用自动备份（默认：启用）。  
  - 设置触发备份的阈值（默认：90%、95%）。  
  - 配置备份保留时间（默认：7天）。  
  - 启用压缩以节省磁盘空间（默认：关闭）。  
- **频道特定设置**：为不同频道设置不同的配置（例如Discord、Webchat、DM）。  

## 使用方法：**  
安装完成后，该工具会：  
1. **每小时检查一次会话容量**。  
2. **在达到75%、85%、90%、95%的阈值时发出警告**。  
3. **提供建议**：  
  - 将重要数据保存到内存中。  
  - 切换到使用率较低的频道。  
  - 提供会话重置命令。  
  - 生成会话恢复提示。  

### 手动检查会话状态：**  
你可以随时请求我检查会话状态：  
```
What's my current session capacity?
Check context usage
Run session_status
```  

### 会话重置（保留会话数据）：**  
当收到容量过高警告时：  
```
Help me reset this session and preserve context
```  
我会：  
1. 将当前工作内容保存到内存中。  
2. 备份会话文件（如果尚未备份）。  
3. 提供会话恢复提示。  
4. 重置会话。  

### 从备份中恢复会话：**  
如果你需要从备份中恢复会话状态：  
```
Show me available backups for this session
Load session from 90% backup
```  
我会：  
1. 列出所有可用的备份文件及其时间戳和大小。  
2. 选择要恢复的备份文件。  
3. 指导你重新连接以恢复会话。  

**备份位置：**  
备份文件位于`~/.openclaw/agents/main/sessions/backups/`。  
备份文件格式为`<session-id>-<threshold>-<timestamp>.jsonl[.gz`。  
备份保留时间为7天（可配置）。  

## 工作原理：**  
### 自动监控（心跳机制）：**  
当你配置Tide Watch后，它会：  
1. **解析配置文件`AGENTS.md`：**  
   - 设置监控频率和警告阈值。  
   - 设置备份参数（何时备份、保留时间、压缩方式）。  
   - 详细逻辑请参阅[PARSING.md]。  
2. **按计划检查会话容量**（默认：每小时一次）：  
   - 运行`session_status`获取令牌使用情况。  
   - 计算容量百分比（`（使用的令牌数 / 总令牌数）× 100`）。  
3. **与阈值比较**：  
   - 使用你设置的阈值（非固定默认值）。  
   - 确定哪些阈值被超过。  
   - 根据阈值严重程度显示警告（从低到高：🟡、🟠、🔴、🚨）。  
4. **发出警告**：  
   - 在达到新阈值时发出警告。  
   - 记录已警告的阈值。  
   - 如果容量保持不变，不再重复警告。  
5. **自动备份（如果启用）：**  
   - 检查是否超过备份阈值。  
   - 创建备份文件（`~/.openclaw/agents/main/sessions/backups/<session-id>-<threshold>-<timestamp>.jsonl`）。  
   - 验证备份完整性。  
   - 记录备份信息。  
   - 避免重复备份相同会话。  
6. **提供建议**：  
   - 将数据保存到内存中。  
   - 切换到使用率较低的频道。  
   - 提供会话重置命令。  
   - 生成会话恢复提示。  
7. **清理旧备份**：  
   - 删除超过保留时间的备份文件（默认：7天）。  
8. **返回静默模式**：  
   - 如果容量低于所有阈值，恢复到静默状态（无输出、无干扰）。  

### 手动检查：**  
你也可以随时请求我检查会话状态：  
```
What's my current session capacity?
Check context usage
Run session_status
```  

### 主要特点：**  
- **兼容性**：适用于任何聊天平台（Anthropic、OpenAI、DeepSeek等）。  
- **非侵入式**：仅在达到阈值时发出警告。  
- **可配置**：可根据需求调整阈值、监控频率和操作方式。  
- **状态记录**：记录被警告的阈值和会话重置情况。  

**为什么需要这个工具？**  
**问题：** 会话窗口会逐渐被占用，直到100%时系统会锁定，导致会话中断。**  
**解决方案：** 通过主动监控提前发现容量问题，让你有时间保存数据、切换频道或重新开始会话。  

**实际案例：**  
在2026年2月23日，Discord频道#navi-code-yatta的会话使用率达到97%，导致系统锁定。用户不得不手动重置会话，从而丢失了对话内容。  

**配置示例：**  
### 保守配置（早期警告）：**  
```markdown
Warning thresholds: 60%, 70%, 80%, 90%
Check frequency: Every 30 minutes
```  
### 积极配置（最大化使用率）：**  
```markdown
Warning thresholds: 85%, 92%, 96%, 98%
Check frequency: Every 2 hours
```  
### 针对特定频道的配置：**  
```markdown
Discord channels: 75%, 85%, 90%, 95% (default)
Webchat: 85%, 95% (lighter warnings)
DM: 90%, 95% (minimal warnings)
```  

**未来计划：**  
- 提供CLI工具以生成容量报告。  
- 在达到阈值时自动备份会话数据。  
- 提供历史容量统计。  
- 实现跨会话的容量对比。  
- 集成心跳监控功能。  
- 发送电子邮件或通知提醒。  
- 提供智能的会话切换建议。  

**系统要求：**  
- OpenClaw需支持`session_status`工具。  
- 工作区需包含`AGENTS.md`文件。  
- 代理配置文件中需包含相应的监控指令。  

**支持信息：**  
- **仓库链接**：https://github.com/chrisagiddings/openclaw-tide-watch  
- **问题反馈**：https://github.com/chrisagiddings/openclaw-tide-watch/issues  
- **社区平台**：https://clawhub.ai/chrisagiddings/tide-watch  

**许可证：** MIT许可证