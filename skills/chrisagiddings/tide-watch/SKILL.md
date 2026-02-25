---
name: tide-watch
description: >
  OpenClaw 的主动会话容量监控与管理功能：  
  - 在可配置的阈值（75%、85%、90%、95%）达到时发出警告，以防止会话窗口卡死；  
  - 在会话重置前自动备份会话数据；  
  - 管理会话恢复的提示功能。  
  适用于以下场景：  
  - 处理耗时较长的项目；  
  - 管理多个聊天渠道（如 Discord、Telegram、Webchat）；  
  - 防止因会话窗口关闭而导致工作丢失。  
  该功能包含以下工具：  
  - 命令行界面（CLI）工具，用于检查会话容量；  
  - 跨会话的仪表盘，用于实时监控会话状态；  
  - 档案管理工具，用于存储和检索会话数据；  
  - 会话恢复功能，方便用户继续未完成的工作。  
  支持与任何模型或服务提供商配合使用。
author: Chris Giddings
homepage: https://github.com/chrisagiddings/openclaw-tide-watch
repository: https://github.com/chrisagiddings/openclaw-tide-watch
metadata:
  openclaw:
    emoji: "🌊"
    version: "1.0.2"
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
    install:
      type: hybrid
      modes:
        - name: directives-only
          description: "AGENTS.md/HEARTBEAT.md directives for automatic monitoring"
          requires: []
          code-execution: false
          files-modified: 
            - "~/clawd/AGENTS.md"
            - "~/clawd/HEARTBEAT.md"
        - name: cli-tools
          description: "Optional Node.js CLI for manual capacity checks and management"
          requires: 
            - node
            - npm
          code-execution: true
          install-command: "npm link"
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
OpenClaw的主动会话容量监控工具。  

## ⚠️ 安全性与架构说明  

**Tide Watch是一个混合型的SKILL插件，具有两种运行模式：**  

### 模式1：仅指令模式（推荐给大多数用户）  
**描述：** 仅使用`AGENTS.md`和`HEARTBEAT.md`中的指令  
**代码执行：** **无**——纯指令，不包含可执行代码  
**文件访问：** 通过代理内置工具读取OpenClaw会话文件  
**安装方式：** 将模板指令复制到工作区配置文件中  
**安全性：** 风险最低——无需安装任何代码  

**功能：**  
- ✅ 通过`session_status`工具监控会话容量  
- ✅ 在容量达到75%、85%、90%、95%的阈值时发出警告  
- ✅ 会话重置时自动显示恢复提示  
- ✅ 所有操作均通过OpenClaw的原生工具完成  

### 模式2：CLI工具模式（可选）  
**描述：** 使用Node.js命令行工具进行手动管理  
**代码执行：** **有**——包含可执行的JavaScript代码  
**文件访问：** 直接读写`~/.openclaw/agents/main/sessions/`目录  
**安装方式：** 使用`git clone`和`npm link`（需要Node.js环境）  
**安全性：** 中等风险——安装前需检查代码  

**功能：**  
- CLI命令：`tide-watch status`、`tide-watch dashboard`等  
- 手动检查会话容量  
- 管理会话存档  
- 编辑恢复提示（⚠️ 请参阅下面的CVE-2026-001漏洞）  

### 🚨 严重安全警告：CVE-2026-001  
**漏洞描述：** `editResumePrompt`函数存在shell注入漏洞  
**受影响版本：** 仅v1.0.0  
**当前版本：** v1.0.1（已修复）  
**严重程度：** 高（CVSS 7.8）  
**状态：** ✅ 已修复  

**总结：** v1.0.0版本中的CLI `resume-prompt edit`命令存在shell注入漏洞，攻击者可通过`--session`参数执行任意命令。该问题已在v1.0.1版本中通过将`execSync`替换为`spawnSync`得到修复。  
**如果您安装了v1.0.0，请立即升级至v1.0.1。**  
**详细信息：** 请参阅[SECURITY-ADVISORY-CVE-2026-001.md](./SECURITY-ADVISORY-CVE-2026-001.md)  

### 安全最佳实践  

**仅指令模式（最安全）：**  
1. ✅ 将`AGENTS.md.template`和`HEARTBEAT.md.template`复制到工作区  
2. ✅ 无需安装任何代码  
3. ✅ 无npm依赖  
4. ✅ 安全性最高  

**使用CLI工具模式（如需）：**  
1. ⚠️ **确认版本为1.0.1或更高**（使用`tide-watch --version`命令）  
2. ⚠️ **安装前检查代码：**  
   - 查看`lib/capacity.js`和`lib/resumption.js`  
   - 确认`package.json`中无安装钩子  
   - 运行`npm test`测试功能（包含113个测试用例）  
3. ⚠️ 使用`--session`参数时仅使用UUID格式的会话ID  
4. ⚠️ 避免向CLI命令传递不可信的输入  
5. ⚠️ 确认备份文件的位置（`~/.openclaw/agents/main/sessions/archive/`）  

**操作类型：**  

**只读操作（安全，无修改）：**  
- `tide-watch status`——查看当前会话数量  
- `tide-watch check --session <id>`——查看特定会话的容量  
- `tide-watch dashboard`——查看容量概览  
- `tide-watch report`——列出超出阈值的会话  
- `tide-watch resume-prompt show --session <id>`——查看恢复提示  

**修改操作（可能修改文件）：**  
- `tide-watch archive --older-than <time>`——将会话移至存档目录  
- `tide-watch resume-prompt edit --session <id>`——编辑恢复提示（v1.0.1版本已修复漏洞）  
- `tide-watch resume-prompt delete --session <id>`——删除恢复提示文件  

**文件系统访问权限：**  
- 读取：`~/.openclaw/agents/main/sessions/*.jsonl`（会话数据）  
- 写入：`~/.openclaw/agents/main/sessions/resume-prompts/*.md`（恢复提示文件）  
- 移动：`~/.openclaw/agents/main/sessions/archive/`（存档会话）  

**网络活动：** **无**——所有操作仅限于本地文件系统。  

### 建议：**  
**大多数用户应使用仅指令模式**，无需安装任何代码即可实现自动容量监控。只有在需要手动管理会话容量时才安装CLI工具。  

## 功能说明：**  
该插件会监控您的OpenClaw会话状态，并在容量达到阈值时发出警告：  
- 🟡 **75%**——提醒您尽快结束当前任务  
- 🟠 **85%**——建议完成当前任务并重置会话  
- 🔴 **90%**——会话即将锁定，请立即保存数据  
- 🚨 **95%**——紧急！立即保存会话数据！  

## 安装步骤：**  

### 第1步：在`AGENTS.md`中添加监控指令  
从`AGENTS.md.template`复制指令模板，并将其添加到工作区的`AGENTS.md`文件中：  
```bash
# From your workspace root (~/clawd or similar)
cat skills/tide-watch/AGENTS.md.template >> AGENTS.md
```  

### 第2步：在`HEARTBEAT.md`中添加心跳检测功能  
从`HEARTBEAT.md.template`复制心跳检测模板，并将其添加到工作区的`HEARTBEAT.md`文件中：  
```bash
# From your workspace root (~/clawd or similar)
cat skills/tide-watch/HEARTBEAT.md.template >> HEARTBEAT.md
```  

### 第3步：配置设置（可选）**  
默认设置适用于大多数用户，您也可以在`AGENTS.md`中进行自定义：  
- **警告阈值**：设置警告的百分比（默认：75%、85%、90%、95%）  
- **检查频率**：设置监控间隔（默认：每小时一次）  
  - 选项：15分钟、30分钟、1小时、2小时或“手动”  
- **自动备份**：启用/禁用自动备份（默认：启用）  
  - 设置触发备份的阈值（默认：90%、95%）  
  - 配置备份保留时间（默认：7天）  
  - 启用压缩以节省磁盘空间（默认：关闭）  
- **频道特定设置**：为不同频道（Discord、Webchat、私信）设置不同配置  

## 使用方法：**  
安装完成后，该插件将：  
1. **每小时检查一次会话容量**  
2. **在达到75%、85%、90%、95%的阈值时发出警告**  
3. **提供相应建议**：  
  - 将重要数据保存到内存  
  - 切换到使用率较低的频道  
  - 提供会话重置命令  
  - 生成会话恢复提示  

### 手动检查：**  
您可以随时请求我检查会话状态：  
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
1. 将当前工作内容保存到内存  
2. 备份会话文件（如果尚未备份）  
3. 提供会话恢复提示  
4. 重置会话  

### 从备份中恢复：**  
如果您需要恢复之前的会话状态：  
```
Show me available backups for this session
Restore session from 90% backup
```  
我会：  
1. 列出可用的备份文件（包含时间戳和文件大小）  
2. 恢复选定的备份  
3. 指导您重新连接以加载恢复的会话  

**备份位置：**  
- 路径：`~/.openclaw/agents/main/sessions/backups/`  
- 格式：`<session-id>-<threshold>-<timestamp>.jsonl[.gz`  
- 保留时间：可配置（默认：7天）  

## 工作原理：**  
### 自动监控（心跳检测）：**  
当您在`HEARTBEAT.md`中启用Tide Watch后，插件会：  
1. **解析配置文件（`AGENTS.md`）**  
  - 监控频率  
  - 警告阈值  
  - 备份设置  
  - 详细解析逻辑请参阅[PARSING.md]  
2. **按计划检查会话容量**（默认：每小时一次）  
  - 运行`session_status`获取令牌使用情况  
  - 计算容量百分比  
3. **与阈值比较**  
  - 使用您设置的阈值（非固定默认值）  
  - 确定是否超过阈值  
  - 根据阈值严重程度显示警告（首次超过为🟡，再次超过为🚨）  
4. **发出警告**  
  - 在达到新阈值时发出警告  
  - 记录已警告的阈值  
  - 如果容量保持不变，则不再重复警告  
5. **自动备份（如果启用）**  
  - 检查是否超过备份触发阈值  
  - 创建备份文件（`~/.openclaw/agents/main/sessions/backups/<session-id>-<threshold>-<timestamp>.jsonl`）  
  - 验证备份完整性  
  - 记录备份信息  
  - 避免重复备份同一阈值  
6. **提供建议**  
  - 将数据保存到内存  
  - 切换到使用率较低的频道  
  - 提供会话重置命令  
  - 生成会话恢复提示  
7. **清理旧备份**  
  - 删除超过保留时间的备份文件（默认：7天）  
8. **恢复静默模式**  
  - 如果容量低于所有阈值，恢复到静默状态（无输出，不中断系统）  

### 手动检查：**  
您也可以随时请求我进行检查：  
```
What's my current session capacity?
Check context usage
Run session_status
```  

### 主要特点：**  
- **兼容性强**：适用于任何提供者（Anthropic、OpenAI、DeepSeek等）  
- **非侵入式**：仅在达到阈值时发出警告  
- **可配置**：可根据工作流程调整阈值、频率和操作  
- **状态记录**：记录被警告的阈值和会话重置情况  

## 使用理由：**  
**问题：** 会话窗口会逐渐占用系统资源。当资源使用率达到100%时，会话会锁定并停止响应，导致数据丢失。  
**解决方案：** 通过主动监控提前发现容量问题，让您有时间保存数据、切换频道或重新开始会话。  

**实际案例：**  
在2026年2月23日，Discord上的#navi-code-yatta频道因资源使用率达到97%而锁定，导致会话中断，用户不得不手动重置会话，导致对话内容丢失。  

## 配置示例：**  
- **保守配置（提前预警）**  
```markdown
Warning thresholds: 60%, 70%, 80%, 90%
Check frequency: Every 30 minutes
```  
- **激进配置（最大化资源利用）**  
```markdown
Warning thresholds: 85%, 92%, 96%, 98%
Check frequency: Every 2 hours
```  
- **频道特定配置**  
```markdown
Discord channels: 75%, 85%, 90%, 95% (default)
Webchat: 85%, 95% (lighter warnings)
DM: 90%, 95% (minimal warnings)
```  

**未来计划：**  
- 提供CLI工具以生成容量报告  
- 在达到阈值时自动备份会话  
- 追踪历史容量使用情况  
- 提供跨会话的容量报告  
- 与心跳检测功能集成  
- 发送电子邮件/通知警告  
- 提供智能的会话切换建议  

## 硬件要求：**  
- 支持`session_status`工具的OpenClaw  
- 工作区中包含`AGENTS.md`文件  
- 代理指令中包含激活的监控配置  

## 技术支持：**  
- 仓库：https://github.com/chrisagiddings/openclaw-tide-watch  
- 问题反馈：https://github.com/chrisagiddings/openclaw-tide-watch/issues  
- 更多信息：https://clawhub.ai/chrisagiddings/tide-watch  

## 许可证：**  
MIT许可证