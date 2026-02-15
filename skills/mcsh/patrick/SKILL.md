---
name: patrick
description: 访问 Patrick 的专家知识库，该库专注于高管决策支持系统。您可以在此库中列出、获取并管理带有上下文变量的结构化专业知识，这些知识可用于高管简报、决策制定以及战略分析。
homepage: https://patrickbot.io
metadata: {"openclaw":{"emoji":"🤖","requires":{"bins":["patrick-cli"]},"install":[{"id":"patrick-install","kind":"script","script":"install.sh","bins":["patrick-cli"],"label":"Install Patrick CLI"}]}}
---

# Patrick Skill

**Patrick** 是一个经过许可的专业知识管理系统，它通过结构化且具备上下文感知能力的专业知识为高管决策提供支持。

**⚠️ 如果 Patrick 无法正常使用：** 请查看 `{baseDir}/install.md` 以获取完整的设置说明，包括许可证配置和初始化步骤。

## 设置流程

### 1. 安装 CLI

运行安装脚本，从 Patrick 服务器下载 `patrick-cli` 二进制文件：

```bash
./install.sh
```

或者直接使用 `curl` 进行安装：

```bash
curl -fsSL https://portal.patrickbot.io/downloads/latest/install.sh | bash
```

这将为您的平台下载 `patrick-cli`，验证其 SHA256 校验和，并将其保存到 `$PATRICK_DATA_PATH/bin/patrick-cli`（默认路径：`~/.patrick/bin/`）。`Dockerfile` 和 `run.sh` 会自动将此路径添加到 `PATH` 环境变量中，因此您可以直接调用 `patrick-cli`。

### 2. 获取许可证

**访问 [patrickbot.io](https://patrickbot.io)** 获取您的 Patrick 许可证。

获取许可证后，请通过聊天方式将其发送给我：

```
Here's my Patrick license: <paste-your-license-here>
```

我会自动为您配置许可证。或者，您也可以手动进行配置：

```bash
patrick-cli set-license "your-license-here"
```

如果您需要切换账户（请注意，这会清除现有数据，因为数据与您的身份相关联）：

```bash
patrick-cli set-license "new-license" --wipe-data
```

### 3. 初始化 Patrick 上下文

**重要提示：** 在使用任何 Patrick 功能之前，请先初始化上下文：

```bash
patrick-cli fetch initialize
```

这将为 Patrick 提供关于您、您的公司和团队的相关信息。如果不进行初始化，其他专业知识功能将无法正常使用。

### 4. 验证安装

通过列出可用的专业知识来测试安装是否成功：

```bash
patrick-cli list
```

**注意**：服务器默认地址为 `https://portal.patrickbot.io`。对于本地开发环境：
- **主机机器**：`export PATRICK_SERVER_URL="http://localhost:8080"`
- **Docker 容器**：`export PATRICK_SERVER_URL="http://host.docker.internal:8080"`

`patrick-moltbot` Docker 容器已经预配置了正确的服务器地址。

### 4. 设置 Cronjob（非常重要）

**Patrick 需要定期运行的 Cronjob 才能正常工作。** 请阅读该目录下的 `INSTALL.md` 以获取完整的设置说明，包括每日简报和任务跟踪的推荐 Cronjob 时间表。

**Cronjob 中的许可证自动续订：** 在运行任何计划任务之前，请检查许可证是否即将过期，并进行续订：

```bash
# Check license expiry and renew if <1 day remaining
DAYS=$(patrick-cli license 2>&1 | grep "days remaining" | grep -oP '\d+')
if [ -n "$DAYS" ] && [ "$DAYS" -lt 1 ]; then
  patrick-cli renew
fi

# Then run your scheduled expertise
patrick-cli fetch daily-briefing --json
```

`patrick-cli renew` 命令会与服务器通信，验证您的有效订阅信息，并保存包含剩余订阅天数的新许可证。

### 5. 保持 Patrick 的更新

检查是否有更新，并升级到最新版本：

```bash
# Check if update is available
patrick-cli upgrade --check

# Upgrade to latest version
patrick-cli upgrade
```

升级流程如下：
1. 从 Patrick 服务器获取最新版本信息
2. 验证下载的二进制文件的 SHA256 校验和
3. 备份当前版本
4. 安装新版本
5. 显示版本说明

更新内容会经过 Patrick 服务器的加密验证和签名。

## 您将获得什么

当您列出可用的专业知识时，会看到以下信息：
- 专业知识 ID 和版本号
- 名称和描述
- 类别（感知、解释、决策、对齐、执行、学习、报告、智能）
- 响应格式（结构化 JSON、Markdown 或混合格式）
- 所需的上下文变量
- 是否支持双向交互（是否可以接收返回的数据）

## 重要提示：**在使用 Patrick 之前收集上下文**

**对于 AI 代理：** 在运行任何 Patrick 功能之前，您必须：
1. 检查 `/app/company/` 或类似位置是否存在公司数据文件
2. 读取所有可用的上下文信息：
   - 公司数据 JSON 文件
   - Slack 消息记录
   - JIRA 工单
   - Git 提交历史记录
   - 日历事件
   - 任何可用的运营数据
3. 将这些上下文信息加载到工作内存中
4. 然后在使用 Patrick 功能时，确保您已充分了解公司的运营情况

当您拥有完整的情境意识时，Patrick 的功能将最为有效。请务必在收集所有相关数据后再运行相关命令。

## 命令概述

| 命令 | 功能 | 示例 |
|---------|---------|---------|
| `set-license` | 设置或更新您的 Patrick 许可证 | `patrick-cli set-license "LICENSE_TOKEN"` |
| `list` | 列出所有可用的专业知识 | `patrick-cli list` |
| `fetch` | 从服务器获取专业知识模板 | `patrick-cli fetch daily-briefing` |
| `send` | 将结果发送回 Patrick | `patrick-cli send daily-briefing --data @output.json` |
| `get` | 检索之前存储的结果 | `patrick-cli get daily-briefing` |

**关键区别：**
- `fetch`：从服务器获取专业知识模板/提示
- `get`：检索您之前发送回 Patrick 的数据/结果

## 使用专业知识与 LLM（大型语言模型）

### 工作流程概述

1. **列出可用的专业知识**
2. **根据需要获取专业知识（可选上下文变量）**
3. **将专业知识内容发送给 LLM 进行处理**
4. **根据提供的 JSON 架构验证 LLM 的响应**
5. **使用 `send` 将响应结果发送回 Patrick（如果支持双向交互）**
6. **之后使用 `get` 命令检索存储的数据**

### 第 1 步：列出可用的专业知识

```bash
patrick-cli list
```

示例输出：
```
Available Expertise:

  daily-briefing (v1.0.0)
    Name: Daily Executive Briefing
    Category: sense
    Response Format: structured
    Bidirectional: ✓ (stores to 'daily-briefing')
    Required Context: (none)
    Description: What's urgent, developing, changed, and the one question

  decision-framing (v1.0.0)
    Name: Decision Framing
    Category: decide
    Response Format: structured
    Bidirectional: ✓ (stores to 'decision-framing')
    Required Context:
      - decision
    Description: Structures ambiguous decisions into clear trade-offs...
```

### 第 2 步：获取专业知识

**不使用上下文时：**

```bash
patrick-cli fetch daily-briefing
```

**使用上下文变量时：**

```bash
patrick-cli fetch decision-framing \
  --context '{"decision":"Should we raise prices?"}'
```

**为 LLM 集成获取 JSON 格式的输出：**

```bash
patrick-cli fetch daily-briefing \
  --json
```

### 第 3 步：将结果发送给 LLM**

获取专业知识后，您会收到以下内容：
- **content**：需要发送给 LLM 的专业知识文本
- **response_schema**：用于验证 LLM 响应的 JSON 架构
- **response_format**：LLM 应该使用的响应格式（结构化/Markdown/混合格式）

**示例工作流程：**

```bash
# Fetch expertise as JSON
EXPERTISE_DATA=$(patrick-cli fetch daily-briefing --json)

# Extract the content field
EXPERTISE_CONTENT=$(echo "$EXPERTISE_DATA" | jq -r '.content')

# Send to your LLM (pseudo-code)
# LLM_RESPONSE=$(send_to_llm "$EXPERTISE_CONTENT")

# If structured format, validate against schema
RESPONSE_SCHEMA=$(echo "$EXPERTISE_DATA" | jq -r '.response_schema')
# validate_json "$LLM_RESPONSE" "$RESPONSE_SCHEMA"
```

### 第 4 步：存储结果（可选）

对于支持双向交互的专业知识，需要将 LLM 的响应发送回 Patrick：

```bash
# Store the response
patrick-cli send daily-briefing \
  --data @llm-response.json

# Later, retrieve stored data
patrick-cli get daily-briefing
```

## 关键概念

### 上下文变量

许多专业知识功能需要上下文信息来填充模板变量。请使用 `--context` 参数并传入一个 JSON 对象：

```json
{
  "current_phase": "pre-launch",
  "launch_date": "2026-02-15",
  "completed_items": 12,
  "target_platforms": ["iOS", "Android"]
}
```

在专业知识内容中，变量会使用 `{{context.key}}` 语法进行替换。

### 响应格式

- **结构化**：LLM 必须返回符合提供架构的 JSON 数据
- **Markdown**：LLM 返回 Markdown 格式的文本
- **混合格式**：LLM 返回包含 JSON 块的 Markdown 文本

### 双向交互专业知识

某些专业知识功能允许接收来自 LLM 的数据，并将其存储在 Patrick 的数据存储中：
- `✓`（支持存储）：使用 `send` 命令保存响应
- `✗`（单向）：专业知识功能仅支持读取数据，不支持数据存储

## 常见使用模式

### 模式 1：简单获取

```bash
# No context needed
patrick-cli fetch daily-briefing
```

### 模式 2：基于上下文的获取

```bash
# Provide context variables
patrick-cli fetch decision-framing \
  --context '{"decision":"Should we expand to EMEA?"}'
```

### 模式 3：完整的双向交互流程

```bash
# 1. Fetch expertise template
patrick-cli fetch daily-briefing --json > expertise.json

# 2. Process with LLM (pseudo-code)
# llm_process < expertise.json > response.json

# 3. Store response back to Patrick
patrick-cli send daily-briefing --data @response.json

# 4. Later, retrieve stored data
patrick-cli get daily-briefing
```

## 故障排除

### 许可证错误

```
Error: No license found at ~/.patrick/license.jwt
```

**解决方法**：从 [patrickbot.io](https://patrickbot.io) 获取许可证并保存：

```bash
patrick-cli set-license "YOUR_LICENSE_HERE"
```

```
Error: Expertise 'X' not in license
```

**解决方法**：访问 [patrickbot.io](https://patrickbot.io) 以升级许可证或添加新的专业知识功能

### 获取数据错误

```
Error fetching expertise: 401 Unauthorized
```

**解决方法**：检查许可证是否有效且未过期

```
Expertise 'X' not found
```

**解决方法**：使用 `list` 命令列出可用的专业知识，确认哪些功能可用

### 上下文错误

```
Warning: Missing required context variables
```

**解决方法**：检查 `list-prompts` 的输出，确认所需的上下文字段，并通过 `--context` 参数提供这些字段

### 签名验证错误

**原因**：`~/.patrick/data/` 目录中的文件被手动编辑、损坏或由非 Patrick CLI 程序修改

**解决方法**：删除损坏的文件并重新生成数据：

```bash
rm ~/.patrick/data/storage_key.json
# Re-run the command that generates this data
```

**预防措施**：切勿手动编辑 `~/.patrick/` 目录中的文件——所有数据都使用与您客户身份关联的 HMAC-SHA256 签名进行保护

### 切换许可证

```
Error: License belongs to a different account.
```

**原因**：您尝试为不同账户设置许可证。由于存储的数据已使用当前客户身份进行签名，因此无法在另一个账户下访问

**解决方法**：使用 `set-license` 命令并添加 `--wipe-data` 选项来切换账户：

```bash
patrick-cli set-license "NEW_LICENSE" --wipe-data
```

这将删除 `~/.patrick/data/` 目录中的所有数据并保存新许可证。之后您需要重新初始化系统。

## 安全性注意事项

- **切勿将 `licensejwt` 或环境文件与真实凭据一起提交**  
- 每次 API 调用时都会对许可证进行验证  
- 专业知识内容会通过 SHA256 校验和进行验证  
- 只有许可证中列出的专业知识功能才能被访问  

**⚠️ 重要提示：切勿手动编辑 `~/.patrick/` 目录中的文件**

`~/.patrick/` 目录中存储的所有数据都使用与您验证过的客户身份关联的 HMAC-SHA256 签名进行保护：
- `licensejwt`：您的许可证令牌  
- `jwks_cache.json`：用于许可证验证的公钥缓存  
- `data/`：存储的专业知识响应（如果支持双向交互）

手动修改这些文件会导致签名验证失败，从而引发错误（如：```
Error: Stored data signature verification failed
```）。  
如果您需要重置数据，请删除相关文件并重新运行命令——切勿手动编辑文件。

有关 Patrick 的加密签名模型的详细信息，请参阅 `{baseDir}/references/security.md`。

## 参考文档

请查看 `{baseDir}/references/` 目录中的以下文档：
- `prompts-api.md`：完整的 API 文档（现在使用 `/v1/expertise` 端点）
- `prompt-format.md`：专业知识结构规范  
- `llm-integration.md`：LLM 集成模式  
- `security.md`：加密签名和数据完整性模型  

## 高级用法

### 自定义服务器地址

您可以指向自己托管的 Patrick 服务器：

```bash
export PATRICK_SERVER_URL="https://patrick.mycompany.com"
```

### 数据存储路径

配置 Patrick 保存本地数据的路径（指定目录，而非单个文件）：

```bash
export PATRICK_DATA_PATH=~/.patrick  # Default location
```

Patrick 会将客户数据文件保存在 `$PATRICK_DATA_PATH/data/<storage_key>.json` 中。

### 启用详细日志记录

启用详细日志记录功能：

```bash
export RUST_LOG="patrick_cli=debug"
```