---
name: tide-watch
description: >
  OpenClaw 的主动会话容量监控与管理功能：  
  - 在预设的阈值（75%、85%、90%、95%）达到时发出警告，防止会话窗口卡顿；  
  - 在会话重置前自动备份数据；  
  - 管理会话恢复的提示功能。  
  适用于处理长时间运行的项目、管理多个聊天渠道（如 Discord、Telegram、Webchat）的场景，有效避免因会话窗口完全关闭而导致的工作丢失。  
  提供命令行工具（CLI）用于容量检查、跨会话的仪表盘查看、会话存档管理以及会话恢复操作；  
  支持与任何模型或服务提供商配合使用。
author: Chris Giddings
homepage: https://github.com/chrisagiddings/openclaw-tide-watch
repository: https://github.com/chrisagiddings/openclaw-tide-watch
metadata:
  openclaw:
    emoji: "🌊"
    version: "1.0.3"
    disable-model-invocation: false
    capabilities:
      - session-monitoring
      - capacity-warnings
      - session-backup
      - session-restoration
      - file-operations-local
    requires:
      bins:
        - node
        - npm
      config:
        - "~/.openclaw/agents/main/sessions/"
      engines:
        node: ">=14.0.0"
    install:
      - type: directives
        description: "AGENTS.md/HEARTBEAT.md directives for automatic monitoring (recommended)"
        requires: []
        code-execution: false
        command: null
        files-modified:
          - "~/clawd/AGENTS.md"
          - "~/clawd/HEARTBEAT.md"
      - type: npm
        description: "Optional Node.js CLI for manual capacity checks and management"
        directory: "."
        command: "npm link"
        requires:
          - node>=14.0.0
          - npm
        code-execution: true
        dependencies:
          dev:
            - "jest@^30.2.0"
          runtime: []
        binaries:
          - name: tide-watch
            path: "./bin/tide-watch"
        files-installed:
          - "bin/tide-watch"
          - "lib/capacity.js"
          - "lib/resumption.js"
    credentials:
      required: false
      types: []
      notes: "No external credentials required. Operates on local OpenClaw session files only."
---
# Tide Watch 🌊  
OpenClaw 的主动会话容量监控工具。  

## ⚠️ 安全性与架构说明  

**Tide Watch 是一个混合型的 SKILL，具有两种运行模式：**  

### 模式 1：仅指令模式（推荐给大多数用户）  
**描述：** 仅使用 `AGENTS.md` 和 `HEARTBEAT.md` 中的指令  
**代码执行：** **无** – 仅包含指令，无可执行代码  
**文件访问：** 通过代理内置工具读取 OpenClaw 会话文件  
**安装：** 将模板指令复制到工作区配置文件中  
**安全性：** 风险最低 – 无需安装任何代码  

**功能：**  
- ✅ 通过 `session_status` 工具监控会话容量  
- ✅ 在达到阈值（75%、85%、90%、95%）时发出警告  
- ✅ 会话重置时自动显示恢复提示  
- ✅ 所有操作均通过 OpenClaw 的原生工具完成  

### 模式 2：CLI 工具模式（可选）  
**描述：** 使用 Node.js 命令行工具进行手动管理  
**代码执行：** **有** – 包含可执行的 JavaScript 代码  
**文件访问：** 直接读写 `~/.openclaw/agents/main/sessions/` 目录  
**安装：** 使用 `git clone` 和 `npm link` （需要 Node.js）  
**安全性：** 中等风险 – 安装前需检查代码  

**功能：**  
- CLI 命令：`tide-watch status`、`tide-watch dashboard` 等  
- 手动检查会话容量  
- 管理会话存档  
- 编辑恢复提示（⚠️ 请参阅下面的 CVE-2026-001）  

### 🚨 严重安全警告：CVE-2026-001  

**漏洞：** `editResumePrompt` 函数中的 Shell 注入漏洞  
**受影响版本：** 仅 v1.0.0  
**当前版本：** v1.0.1（已修复）  
**严重程度：** 高（CVSS 7.8）  
**状态：** ✅ 已修复  

**总结：** v1.0.0 版本中的 CLI `resume-prompt edit` 命令存在 Shell 注入漏洞。攻击者可以通过控制 `--session` 参数执行任意命令。**此问题已在 v1.0.1 中通过将 `execSync` 替换为 `spawnSync` 修复。**  

**如果您安装了 v1.0.0，请** **立即升级到 v1.0.1。**  
**完整信息：** 请参阅 [SECURITY-ADVISORY-CVE-2026-001.md](./SECURITY-ADVISORY-CVE-2026-001.md)  

### 安全最佳实践  

**仅指令模式（最安全）：**  
1. ✅ 将 `AGENTS.md.template` 和 `HEARTBEAT.md.template` 复制到工作区  
2. ✅ 无需安装代码  
3. ✅ 无 npm 依赖项  
4. ✅ 安全性最高  

**使用 CLI 工具模式（如需）：**  
1. ⚠️ **确认版本为 1.0.1 或更高**（`tide-watch --version`）  
2. ⚠️ **安装前检查代码：**  
   - 查看 `lib/capacity.js` 和 `lib/resumption.js`  
   - 检查 `package.json` 中的依赖项（应无依赖项）  
   - 运行 `npm test` 测试功能（共 113 个测试）  
3. ⚠️ **使用 UUID 作为会话 ID**  
4. ⚠️ **避免向 CLI 命令传递不可信的输入**  
5. ⚠️ **检查备份位置**（`~/.openclaw/agents/main/sessions/archive/`）  

**操作类型：**  

**只读操作**（✅ 安全，无修改）：  
- `tide-watch status` – 查看当前会话数量  
- `tide-watch check --session <id>` – 查看特定会话的容量  
- `tide-watch dashboard` – 查看容量概览  
- `tide-watch report` – 列出超过阈值的会话  
- `tide-watch resume-prompt show --session <id>` – 查看恢复提示  

**修改操作**（⚠️ 会修改文件）：  
- `tide-watch archive --older-than <time>` – 将会话移至存档目录  
- `tide-watch resume-prompt edit --session <id>` – 打开编辑器（CVE 已在 v1.0.1 中修复）  
- `tide-watch resume-prompt delete --session <id>` – 删除恢复提示文件  

**文件系统访问：**  
- 读取：`~/.openclaw/agents/main/sessions/*.jsonl`（会话数据）  
- 写入：`~/.openclaw/agents/main/sessions/resume-prompts/*.md`（恢复提示文件）  
- 移动：`~/.openclaw/agents/main/sessions/archive/`（存档会话）  

**网络活动：** **无** – 所有操作均在本地文件系统内完成。  

### 运行时要求**  

**模式 1（仅指令模式）：**  
- **Node.js**：无需  
- **npm**：无需  
- **依赖项：** 无  
- **二进制文件：** 无  
- **安装：** 将模板文件复制到工作区配置文件中  

**模式 2（CLI 工具模式（可选）：**  
- **Node.js：** v14.0.0 或更高版本  
- **npm：** 任意最新版本  
- **依赖项：**  
  - 开发：`jest@^30.2.0`（仅用于测试）  
  - 运行时：无依赖项  
- **二进制文件：** `tide-watch`（通过 `npm link` 全局安装）  
- **安装：** `git clone` + `npm link`  

**为何没有运行时依赖项？**  
- 仅使用 Node.js 内置模块（`fs`、`path`、`child_process`）  
- 无外部 API 客户端  
- 无网络库  
- 攻击面极小  

### 建议  

**大多数用户应使用仅指令模式。** 这种方式无需安装任何代码即可实现自动容量监控。只有在需要手动管理会话容量时才安装 CLI 工具。  

## 功能说明  

**监控您的 OpenClaw 会话状态，并在容量达到阈值时发出警告：**  
- 🟡 **75%** – 提醒您尽快结束当前会话  
- 🟠 **85%** – 建议完成当前任务并重置会话  
- 🔴 **90%** – 会话即将锁定，建议立即重置  
- 🚨 **95%** – 严重！请立即保存会话内容！  

## 安装步骤  

### 第 1 步：在 `AGENTS.md` 中添加监控指令  

从 `AGENTS.md.template` 复制指令模板，并将其添加到工作区的 `AGENTS.md` 文件中：  
```bash
# From your workspace root (~/clawd or similar)
cat skills/tide-watch/AGENTS.md.template >> AGENTS.md
```  

或者手动添加模板中的监控内容。  

**第 2 步：在 `HEARTBEAT.md` 中添加心跳任务**  

从 `HEARTBEAT.md.template` 复制心跳模板，并将其添加到工作区的 `HEARTBEAT.md` 文件中：  
```bash
# From your workspace root (~/clawd or similar)
cat skills/tide-watch/HEARTBEAT.md.template >> HEARTBEAT.md
```  

或者手动添加 Tide Watch 的心跳监控内容。  

**第 3 步：配置设置（可选）**  
默认设置适用于大多数用户，但您可以在 `AGENTS.md` 中进行自定义：  

**警告阈值**（何时发出警告）：  
- 调整百分比（默认：75%、85%、90%、95%）  
- 范围：50–99%，共 2–6 个阈值  

**检查频率**（监控间隔）：  
- 调整检查间隔（默认：每小时一次）  
- 选项：15分钟、30分钟、1小时、2小时或“手动”  
- 范围：5分钟至6小时  

**自动备份**：  
- 启用/禁用自动备份（默认：启用）  
- 设置触发备份的阈值（默认：90%、95%）  
- 配置备份保留时间（默认：7天）  
- 启用压缩以节省磁盘空间（默认：关闭）  
**频道特定设置（高级）**：  
- 不同频道（Discord、Webchat、私信）的单独配置  

## 使用方法  

安装完成后，我会：  
1. **每小时检查一次会话容量**  
2. **在达到阈值（75%、85%、90%、95%）时发出警告**  
3. **提供建议**：  
   - 将重要内容保存到内存  
   - 切换到使用率较低的频道  
   - 提供会话重置命令  
   - 生成会话恢复提示  

### 手动检查  
您可以随时要求我检查会话状态：  
```
What's my current session capacity?
Check context usage
Run session_status
```  

### 重置会话并保留会话内容  

当收到容量过高警告时：  
```
Help me reset this session and preserve context
```  
我会：  
1. 将当前工作内容保存到内存  
2. 备份会话文件（如果尚未备份）  
3. 提供会话恢复提示  
4. 重置会话  

### 从备份中恢复  
如果您需要恢复之前的会话状态：  
```
Show me available backups for this session
Restore session from 90% backup
```  
我会：  
1. 列出可用的备份文件及其时间戳和大小  
2. 恢复选定的备份  
3. 指导您重新连接以加载恢复的会话  

**备份位置：**  
- 路径：`~/.openclaw/agents/main/sessions/backups/`  
- 格式：`<session-id>-<threshold>-<timestamp>.jsonl[.gz`  
- 保留时间：可配置（默认：7天）  

## 工作原理  

### 自动监控（心跳机制）  
当您在 `HEARTBEAT.md` 中启用 Tide Watch 时，我会：  
1. **解析配置**（来自 `AGENTS.md`）：  
   - 监控频率  
   - 警告阈值  
   - 备份设置  
   - 详情请参阅 [PARSING.md](PARSING.md)  
2. **按计划检查容量**（默认：每小时一次）：  
   - 运行 `session_status` 获取令牌使用情况  
   - 计算占用百分比：`(tokens_used / tokens_max) * 100`  
3. **与阈值进行比较**：  
   - 使用您配置的阈值（非固定默认值）  
   - 确定哪些阈值被超过  
   - 根据阈值严重程度显示警告（最严重为 🚨）  
4. **发出警告**：  
   - 对于新达到的阈值发出警告  
   - 记录该会话已触发的阈值  
   - 如果容量保持不变，则不再重复警告  
5. **自动备份（如果启用）**：  
   - 检查是否达到备份阈值  
   - 创建备份文件：`~/.openclaw/agents/main/sessions/backups/<session-id>-<threshold>-<timestamp>.jsonl`  
   - 验证备份完整性  
   - 记录备份完成情况  
   - 记录备份的阈值  
6. **提供建议**：  
   - 将内容保存到内存  
   - 切换到使用率较低的频道  
   - 提供会话重置命令  
   - 生成会话恢复提示  
7. **清理旧备份**：  
   - 删除超过保留时间的备份文件（默认：7天）  
8. **恢复静默模式**：  
   - 如果容量低于所有阈值，返回 `HEARTBEAT_OK`  
   - 无输出，不中断系统  

### 手动检查  
您也可以随时要求我进行检查：  
```
What's my current session capacity?
Check context usage
Run session_status
```  

### 主要特点：  
- **兼容性高**：适用于任何提供者（Anthropic、OpenAI、DeepSeek 等）  
- **非侵入式**：仅在达到阈值时发出警告  
- **可配置**：根据工作流程调整阈值、频率和操作  
- **状态记录**：记录被触发的阈值及会话重置情况  

## 为何需要这个工具？  
**问题：** 会话窗口会逐渐占用资源。一旦达到 100%，会话会锁定并停止响应，导致数据丢失。**  
**解决方案：** 主动监控可以提前发现容量问题，让您有时间保存工作、切换频道或重新开始会话。  

**实际案例**：  
在 Discord #navi-code-yatta 中，系统在 2026-02-23 日达到 97% 的使用率并锁定，导致会话中断，不得不手动重置，导致对话内容丢失。  

## 配置示例：  
### 保守配置（提前预警）  
```markdown
Warning thresholds: 60%, 70%, 80%, 90%
Check frequency: Every 30 minutes
```  
### 积极配置（最大化使用率）  
```markdown
Warning thresholds: 85%, 92%, 96%, 98%
Check frequency: Every 2 hours
```  
### 针对不同频道的配置  
```markdown
Discord channels: 75%, 85%, 90%, 95% (default)
Webchat: 85%, 95% (lighter warnings)
DM: 90%, 95% (minimal warnings)
```  

**未来计划：**  
- 提供 CLI 工具以生成容量报告  
- 在达到阈值时自动备份会话  
- 提供历史容量记录  
- 实现跨会话的容量监控  
- 集成心跳监控功能  
- 发送电子邮件/通知警告  
- 提供智能的会话切换建议  

**系统要求：**  
- OpenClaw 支持 `session_status` 工具  
- 工作区包含 `AGENTS.md` 文件  
- 代理指令中包含主动监控配置  

## 支持信息：  
- **仓库：** https://github.com/chrisagiddings/openclaw-tide-watch  
- **问题报告：** https://github.com/chrisagiddings/openclaw-tide-watch/issues  
- **ClawHub：** https://clawhub.ai/chrisagiddings/tide-watch  

**许可证：** MIT