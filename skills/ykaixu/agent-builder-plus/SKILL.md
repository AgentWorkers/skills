---
name: agent-builder-plus
description: 构建高性能的 OpenClaw 代理，具备全面的安全特性。当您需要设计新的代理（包括代理角色、操作规则）并生成相应的 OpenClaw 工作空间文件（SOUL.md、IDENTITY.md、AGENTS.md、USER.md、HEARTBEAT.md，可选的 MEMORY.md 和 MEMORY/YYYY-MM-DD.md）时，可以使用此工具。该工具支持以下功能：防死锁保护、超时处理、错误恢复、循环中断机制、消息过载保护、令牌限制保护、重试机制、健康检查、降级模式、监控与日志记录、配置验证以及通道冲突预防。此外，它还适用于对现有代理的行为、安全防护机制、自主性模型、心跳计划和技能列表进行迭代优化。
---
# Agent Builder Plus (OpenClaw)

该工具用于设计和生成一个完整的**OpenClaw代理工作空间**，提供丰富的默认设置以及针对高级用户的详细询问流程。

## 快速入门

```bash
# 1. Read skill documentation
Read SKILL.md and references/openclaw-workspace.md

# 2. Answer interview questions
Provide answers for: job statement, surfaces, autonomy level, prohibitions, memory, tone, tool posture

# 3. Generate workspace files
The skill will create: IDENTITY.md, SOUL.md, AGENTS.md, USER.md, HEARTBEAT.md

# 4. Verify and test
Run acceptance tests to validate behavior
```

## 参考资料

- 工作空间布局与心跳规则：请参阅 `references/openclaw-workspace.md`
- 文件模板/代码片段：请参阅 `references/templates.md`
- 代理架构概述（可选）：请参阅 `references/architecture.md`

## 从零开始构建代理的流程

### 第1阶段 - 询问详细信息

仅询问您需要的信息，避免冗长。建议分多轮进行询问，而非一次性提交大量问题。

**高级用户所需的最小问题集：**

1) **任务描述**：用一句话概括代理的主要任务是什么？
2) **沟通渠道**：支持哪些渠道（Telegram/WhatsApp/Discord/iMessage/Feishu）？支持私信还是群组聊天？
3) **自主性级别**：
   - 顾问模式（仅提供建议）
   - 操作员模式（允许非破坏性操作；在执行破坏性操作或使用外部资源前需用户确认）
   - 自动驾驶模式（具有较高自主权；风险也相应增加）
4) **禁止的行为**：代理绝对不能执行哪些操作？
5) **数据存储**：是否需要记录在 `MEMORY.md` 文件中？哪些类别的数据需要被记录？
6) **沟通风格**：简洁还是详细？语气应如何？是否允许在群组中使用粗俗语言？在群组中是否应使用“非用户自定义的语气”？
7) **工具使用方式**：优先使用工具还是直接提供答案？是否需要验证用户身份？

**错误处理：**

- 如果用户回答不完整：请进一步询问缺失的信息。
- 如果用户对自主性级别不确定：解释相关权衡，并建议从“操作员模式”开始设置。
- 如果用户希望跳过某些问题：向用户说明每个问题对代理行为的重要性。

### 第2阶段 - 生成工作空间文件

生成以下文件（构成一个基本的OpenClaw代理配置）：

- `IDENTITY.md`
- `SOUL.md`
- `AGENTS.md`
- `USER.md`
- `HEARTBEAT.md`（默认情况下通常为空）
- `BOOTSTRAP.md`（用于首次运行时的指导）

**可选文件：**

- `MEMORY.md`（仅适用于私有会话）
- `memory/YYYY-MM-DD.md`（记录代理创建时间的日志文件）
- `TOOLS.md`（用户可自定义的跨环境设置）

**文件创建命令：**

```bash
# Create workspace directory
mkdir -p /path/to/workspace/memory

# Create files (use write tool)
# Each file should be created with appropriate content from templates.md
```

**错误处理：**

- 如果目录创建失败：检查权限和路径是否正确。
- 如果文件写入失败：检查磁盘空间及写入权限。
- 如果模板引用失败：确保 `references/templates.md` 文件存在。

**错误恢复措施：**

- 如果目录创建失败：检查父目录的权限，并尝试其他路径。
- 如果文件写入失败：检查磁盘空间和写入权限，然后尝试减少文件内容后再进行写入。
- 如果模板引用失败：确认 `references` 和相关目录的存在性，并检查文件权限。

请使用 `references/templates.md` 中提供的模板，并根据用户的回答进行内容调整。

### 第2.5阶段 - 在OpenClaw中注册代理

**⚠️ 重要警告：避免渠道冲突**

**切勿将新代理绑定到与主代理相同的渠道！**  
否则新代理会占用主代理的渠道，导致无法与主代理进行通信。

**在注册前，请检查现有代理的绑定情况：**

```bash
# List all agents and their bindings
openclaw agents list

# Check which channels are already in use
openclaw channels list
```

**渠道绑定规则：**

1. **主代理**：始终使用指定的Feishu私信渠道。
2. **新代理**：必须使用不同的渠道或子渠道。
3. **测试环境**：可以使用 `/agentname` 命令进行测试绑定。
4. **生产环境**：应为每个代理创建单独的Feishu应用或使用不同的渠道。

**先创建备份配置：**

```bash
# Backup openclaw.json before modification
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.backup
```

**注册代理：**

```bash
# Add agent to OpenClaw configuration
openclaw agents add <agent-name> --workspace /path/to/workspace

# Example:
openclaw agents add my-assistant --workspace /home/user/.openclaw/workspaces/my-assistant
```

**渠道绑定选项：**

**Feishu：**
- **直接绑定**：在Feishu应用设置中进行配置（生产环境推荐）
  - ⚠️ 注意：切勿将新代理绑定到与主代理相同的Feishu应用。
  - 为新代理创建一个新的Feishu应用。
- **命令绑定**：在Feishu消息中使用 `/agentname` 命令进行绑定（测试环境使用）。
  - 这种方式是安全的，不会导致渠道被占用。
- **多渠道绑定**：代理可以同时绑定到多个渠道。

**Telegram：**
- 为每个代理创建单独的机器人令牌。
- 不要在代理之间共享机器人令牌。
- 使用不同的机器人用户名。

**WhatsApp：**
- 为每个代理使用不同的电话号码。
- 不要共享WhatsApp Business API凭证。

**Discord：**
- 为每个代理使用不同的机器人令牌。
- 为每个代理创建单独的Discord应用。
- 不要共享Discord机器人令牌。

**iMessage：**
- 每个代理应使用不同的Apple ID。
- 不要共享iMessage凭证。

**身份验证配置（如需设置）：**

```bash
# Edit auth-profiles.json for external service access
# Location: ~/.openclaw/auth-profiles.json

# Example structure:
{
  "feishu": {
    "appId": "cli_xxxxx",
    "appSecret": "xxxxx"
  },
  "telegram": {
    "botToken": "your-bot-token"
  }
}
```

**⚠️ 重要提示：切勿重复使用主代理的凭证！**

**错误处理：**

- 如果 `openclaw agents add` 命令执行失败：从备份中恢复配置并检查语法。
- 如果身份验证失败：验证 `auth-profiles.json` 文件中的凭证信息。
- 如果绑定失败：检查渠道权限和网络连接情况。
- 如果备份恢复失败：检查 `~/.openclaw/` 目录的写入权限。
- **如果主代理停止响应**：立即从备份中恢复配置并重启OpenClaw。

### 第2.6阶段 - 验证配置

**验证步骤：**

```bash
# 1. Check agent is registered
openclaw agents list

# 2. Verify workspace files exist
ls -la /path/to/workspace/

# 3. Test agent can load (dry run)
openclaw agents test <agent-name>
```

**成功标准：**

- 代理能够出现在 `openclaw agents list` 的输出结果中。
- 所有必要的文件（`IDENTITY.md`, `SOUL.md`, `AGENTS.md`, `USER.md`）都已生成。
- 配置文件中不存在语法错误。
- 代理能够成功加载且无错误。

**如果验证失败：**

1. 检查文件权限。
2. 验证配置文件中的JSON/YAML语法是否正确。
3. 查看 `openclaw agents test` 的错误信息。
- 如有必要，从备份中恢复配置。

**错误恢复措施：**

- 如果代理未出现在列表中：检查 `openclaw.json` 的语法，重新执行第2.5阶段。
- 如果文件缺失：使用正确的路径重新执行第2阶段。
- 如果加载测试失败：检查文件语法，并确认模板内容是否符合OpenClaw的规范。

### 第3阶段 - 安全防护措施检查

确保生成的代理配置包含以下内容：

- 明确要求用户在执行破坏性操作前必须获得确认的规则。
- 明确要求在发送出站消息前必须获得用户确认的规则。
- 当命令行使用出错时停止代理运行的规则。
- 设置最大迭代次数或循环终止机制。
- 规定群组聊天的礼仪规则。
- 将重要安全规则记录在 `AGENTS.md` 文件中。

**错误处理：**

- 如果缺少某些安全防护措施：将其添加到 `AGENTS.md` 或 `SOUL.md` 中。
- 如果防护措施过于严格：询问用户关于所需自主性级别的意见。

### 第4阶段 - 快速验收测试

提供5-10个简短的测试场景，以验证代理的行为，例如：

- “生成草稿但不要发送消息；发送前请先询问用户。”
- “总结当前的工作空间状态，但不要泄露敏感信息。”
- “遇到未知错误时，展示如何使用 `--help` 命令进行恢复。”
- “在群组聊天中，有人提出一般性问题；判断是否应该回复。”

**错误处理：**

- 如果代理在验收测试中失败：检查安全防护措施，调整自主性级别，并核实模板内容。
- 如果测试要求过于严格：调整测试场景以匹配实际需求。

### 第8阶段 - 自动化测试（可选）

**自动化测试命令：**

```bash
# Run OpenClaw's built-in agent tests
openclaw agents test <agent-name> --verbose

# Test workspace file syntax
openclaw validate workspace /path/to/workspace

# Test configuration loading
openclaw config test
```

**测试脚本示例：**

```bash
#!/bin/bash
# test-agent.sh - Automated agent testing script

AGENT_NAME="my-assistant"
WORKSPACE="/path/to/workspace"

echo "Testing agent: $AGENT_NAME"

# Test 1: File existence
echo "Test 1: Checking required files..."
for file in IDENTITY.md SOUL.md AGENTS.md USER.md HEARTBEAT.md; do
  if [ ! -f "$WORKSPACE/$file" ]; then
    echo "❌ Missing: $file"
    exit 1
  fi
done
echo "✅ All required files present"

# Test 2: Configuration syntax
echo "Test 2: Validating configuration..."
openclaw agents list | grep -q "$AGENT_NAME"
if [ $? -eq 0 ]; then
  echo "✅ Agent registered correctly"
else
  echo "❌ Agent not found in configuration"
  exit 1
fi

# Test 3: Agent loading
echo "Test 3: Testing agent load..."
openclaw agents test "$AGENT_NAME"
if [ $? -eq 0 ]; then
  echo "✅ Agent loads successfully"
else
  echo "❌ Agent failed to load"
  exit 1
fi

echo "🎉 All tests passed!"
```

**错误处理：**

- 如果自动化测试失败：查看错误信息，检查文件语法和配置内容。
- 如果测试脚本失败：检查脚本的权限设置和路径是否正确。

### 可选：将代理配置为systemd服务

对于生产环境，可以将代理配置为systemd服务：

**服务文件示例：**

```bash
# Create systemd service file
sudo tee /etc/systemd/system/openclaw-agent.service > /dev/null <<EOF
[Unit]
Description=OpenClaw Agent Service
After=network.target

[Service]
Type=simple
User=<your-username>
WorkingDirectory=/home/<your-username>/.openclaw
ExecStart=/usr/bin/node /home/<your-username>/.npm-global/lib/node_modules/openclaw/dist/index.js
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target


[Install]
WantedBy=multi-user.target
EOF
```

**启用并启动服务：**

```bash
# Reload systemd configuration
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable openclaw-agent.service

# Start service now
sudo systemctl start openclaw-agent.service

# Check status
sudo systemctl status openclaw-agent.service

# View logs
sudo journalctl -u openclaw-agent.service -f
```

**错误处理：**

- 如果服务启动失败：查看 `journalctl` 日志，检查文件路径和用户权限。
- 如果服务崩溃：检查OpenClaw的日志和代理配置，然后重启服务。
- 如果服务无法启用：检查systemd的配置语法，并确认systemd是否正在运行。

## 对现有代理进行改进的流程

在改进现有代理时，请询问以下问题：

1) 代理目前最常见的故障类型有哪些？（例如：无限循环、权限滥用、信息冗余等）
2) 您希望对代理的自主性进行哪些调整？
3) 是否需要设置新的安全限制？
4) 是否需要修改代理的心跳行为？

然后根据这些问题，对以下文件进行针对性的修改：

- `SOUL.md`（代理的角色设定、沟通风格和权限设置）
- `AGENTS.md`（操作规则、数据存储和任务分配）
- `HEARTBEAT.md`（包含必要的检查清单）

请确保修改内容尽可能小且精准。

**错误处理：**

- 如果修改过程中出现问题：检查文件权限和文件是否存在，必要时从备份中恢复配置。
- 如果修改导致代理行为异常：从git仓库或备份中恢复配置，并重新审查修改内容。
- 如果用户拒绝接受修改：请进一步询问用户的意见，并提出其他修改方案。