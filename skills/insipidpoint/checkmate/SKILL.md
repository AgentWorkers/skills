---
name: checkmate
description: "**强制任务完成：** 将您的目标转化为“通过/失败”的评判标准，运行相应的任务处理程序（worker），评估输出结果，反馈还缺少哪些内容，并持续循环执行，直到所有评判标准都满足为止。只有在任务真正完成之后，才会将其交付给最终用户。  
**触发条件：** `checkmate: TASK`"
requires:
  cli:
    - openclaw  # platform CLI: sessions.list, agent spawn, message send
privileges: high  # spawned workers inherit full host-agent runtime (exec, OAuth, all skills)
---
# Checkmate

这是一个基于Python的确定性循环脚本（`scripts/run.py`），它用于调用大型语言模型（LLM）来执行工作者（worker）和裁判（judge）的角色。在任务通过之前，没有任何操作会被执行——并且在每个检查点（checkpoint）上，你仍然拥有控制权。

## 要求

- **OpenClaw平台命令行界面（`openclaw`）**：必须已添加到系统的`PATH`环境变量中。该工具用于以下操作：
  - `openclaw gateway call sessions.list`：获取会话的UUID，以便进行任务注入。
  - `openclaw agent --session-id <UUID>`：将检查点消息注入到正在进行的会话中。
  - `openclaw message send`：作为消息传递的备用渠道（例如：Telegram、Signal）。
- **Python 3**：`run.py`脚本仅使用Python的标准库，不需要安装任何额外的`pip`包。
- 不需要单独的API密钥或环境变量——所有通信都通过OpenClaw的现有OAuth机制进行。

## 安全性与权限模型

> ⚠️ **这是一个高权限级别的脚本。** 在批量或自动化模式下使用前，请务必仔细阅读相关说明。

被创建的工作者和裁判会继承宿主代理的所有运行时权限，包括：
- 执行任意shell命令的能力（`exec`）。
- 使用`web_search`和`web_fetch`功能。
- 访问所有已安装的技能（包括那些需要OAuth认证的技能，如Gmail、Drive等）。
- 能够创建子代理（`sessions_spawn`）。

这意味着你提供的任务描述直接决定了工作者的行为——请将其视为一段即将执行的代码，而不仅仅是一条待发送的消息。

**批量模式（`--no-interactive`）**会完全移除人工干预。在交互模式下（默认设置），每次循环开始前都需要用户批准相关标准；而在批量模式下，标准会自动被批准，循环会自动运行至完成。请仅在对任务和环境完全信任的情况下使用批量模式。

**用户输入的处理**：当用户对检查点消息进行回复时，主代理会将其内容原封不动地写入工作区的`user-input.md`文件中。编排器会读取这些回复并据此采取行动。切勿将不可信的第三方内容作为检查点回复进行传递。

## 适用场景

当正确性比速度更重要时，可以使用`checkmate`脚本——即当“第一次尝试就达到合格标准”是不可接受的场合。

**适用场景示例：**
- 需要通过测试或满足特定规范的代码。
- 需要达到特定质量标准的文档或报告。
- 需要彻底完成且覆盖特定范围的调研工作。
- 任何需要手动迭代直至满足要求的任务。

**触发指令**：
- `checkmate: TASK`
- `keep iterating until it passes`
- `don't stop until done`
- `until it passes`
- `quality loop: TASK`
- `iterate until satisfied`
- `judge and retry`
- `keep going until done`

## 架构

### 交互模式（默认设置）：用户需要批准任务标准，并在每次迭代前进行确认。

### 批量模式（`--no-interactive`）：完全自动化运行，无需用户干预。

#### 用户输入处理机制

当编排器需要用户输入时，它会执行以下操作：
1. 创建`workspace/pending-input.json`文件（包含输入类型和工作区路径）。
2. 通过`--recipient`和`--channel`参数发送通知。
3. 每5秒检查一次`workspace/user-input.md`文件（最多等待`--checkpoint-timeout`分钟）。

主代理负责处理用户输入：当`pending-input.json`文件存在且用户已回复时，代理会将用户的回复写入`user-input.md`文件中。编排器会自动读取这些回复。

每个代理会话的创建过程如下：
（具体实现代码位于````bash
openclaw agent --session-id <isolated-id> --message <prompt> --timeout <N> --json
````）

所有通信都通过OpenClaw的WebSocket接口进行，且不需要额外的API密钥。工作者会继承主代理的所有运行时权限，包括执行命令、使用Web搜索和数据获取功能，以及访问所有可用的技能。

## 你的任务（主代理）

当`checkmate`脚本被触发时，你需要执行以下步骤：
1. **获取你的会话UUID**（用于直接注入任务指令）：
   （具体实现代码位于````bash
   openclaw gateway call sessions.list --params '{"limit":1}' --json \
     | python3 -c "import json,sys; s=json.load(sys.stdin)['sessions'][0]; print(s['sessionId'])"
   ````）
   同时记录`--recipient`（用于发送通知的渠道用户ID）和`--channel`（备用通知渠道）。

2. **创建工作区**：
   （具体实现代码位于````bash
   bash <skill-path>/scripts/workspace.sh /tmp "TASK"
   ````）
   打印工作区路径。如有需要，将任务详细信息写入`workspace/task.md`文件中。

3. **启动编排器**（在后台运行）：
   （具体实现代码位于````bash
   python3 <skill-path>/scripts/run.py \
     --workspace /tmp/checkmate-TIMESTAMP \
     --task "FULL TASK DESCRIPTION" \
     --max-iter 10 \
     --session-uuid YOUR_SESSION_UUID \
     --recipient YOUR_RECIPIENT_ID \
     --channel <your-channel>
   ````）
   使用`exec`命令以`background=true`模式运行脚本。脚本会持续运行，直到任务完成。
   如果需要完全自动化运行，可以使用`--no-interactive`参数。

4. **通知用户`checkmate`脚本正在运行中，告知他们当前正在处理的任务内容，并说明他们会通过配置好的渠道收到任务标准和检查点消息以供审核和批准。

5. **处理用户回复**：当用户对检查点消息作出回复时，检查`pending-input.json`文件，并将用户的回复写入`workspace/user-input.md`中。

#### 处理用户回复的机制

当编排器向用户发送任务标准、批准请求或检查点请求时，它会接收用户的回复，并将其保存到`workspace/user-input.md`文件中。编排器会每5秒检查一次该文件。一旦收到回复，脚本会自动继续执行，并删除`pending-input.json`文件。

**各处理环节的响应方式：**
| 处理环节 | 响应内容 | 后续操作 |
|------|----------|----------|
| 标准审核 | “ok”、“approve”、“lgtm” | 允许继续执行或提供反馈 |
| 任务启动 | “go”、“start”、“ok” | 通知用户任务已开始或需要编辑新任务 |
| 迭代检查点 | “continue” | 继续执行；“redirect: DIRECTION” | 指示下一步操作 |
| 停止执行 | “stop” | 中止当前任务 |

## 参数设置

| 参数 | 默认值 | 说明 |
|------|---------|-------|
| `--max-intake-iter` | 5 | 标准审核的迭代次数 |
| `--max-iter` | 10 | 主循环的迭代次数（复杂任务可设置为20） |
| `--worker-timeout` | 3600秒 | 单个工作会话的持续时间 |
| `--judge-timeout` | 300秒 | 单个裁判会话的持续时间 |
| `--session-uuid` | — | 代理会话的UUID（从`sessions.list`获取）；用于直接注入任务指令 |
| `--recipient` | — | 通知接收者的ID（例如：用户聊天ID或电话号码）；注入失败时的备用选项 |
| `--channel` | — | 备用通知的渠道（例如：Telegram、WhatsApp、Signal） |
| `--no-interactive` | off | 禁用用户交互（批量模式） |
| `--checkpoint-timeout` | 60秒 | 每次检查点等待用户回复的时间限制 |

## 工作区布局

（工作区的具体布局结构位于````
memory/checkmate-YYYYMMDD-HHMMSS/
├── task.md               # task description (user may edit pre-start)
├── criteria.md           # locked after intake
├── feedback.md           # accumulated judge gaps + user direction
├── state.json            # {iteration, status} — resume support
├── pending-input.json    # written when waiting for user; deleted after response
├── user-input.md         # agent writes user's reply here; read + deleted by orchestrator
├── intake-01/
│   ├── criteria-draft.md
│   ├── criteria-verdict.md  (non-interactive only)
│   └── user-feedback.md     (interactive: user's review comments)
├── iter-01/
│   ├── output.md         # worker output
│   └── verdict.md        # judge verdict
└── final-output.md       # written on completion
````）

## 任务恢复

如果脚本被中断，只需使用相同的`--workspace`参数重新运行即可。脚本会读取`state.json`文件并跳过已完成的步骤。已锁定的`criteria.md`文件会被重复使用；已完成的`iter-N/output.md`文件不会被再次执行。

## 提示信息

`run.py`脚本使用的提示文件包括：
- `prompts/intake.md`：将任务描述转换为标准格式的草稿。
- `prompts/criteria-judge.md`：用于评估标准的质量（是否通过审核）。
- `prompts/worker.md`：显示给工作者的提示信息（包含任务信息、标准内容、反馈信息、迭代次数和输出路径）。
- `prompts/judge.md`：用于判断输出结果是否符合标准。

**注：**以下文件仅用于参考，不会被`run.py`脚本直接调用：
- `prompts/orchestrator.md`：包含架构设计的详细说明。