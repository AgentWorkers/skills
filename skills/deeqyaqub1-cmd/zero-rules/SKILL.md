---
name: zero-rules
description: "在确定性任务（数学运算、时间计算、货币转换、文件处理、任务调度等）到达大型语言模型（LLM）之前，先在本地完成这些任务。通过本地处理简单的查询（无需调用任何API），可以节省50%至70%的token成本。"
user-invocable: true
homepage: https://cascadeai.dev
metadata: {"openclaw":{"emoji":"🔥","requires":{"bins":["node"]}}}
---

# ZeroRules — 确定性任务拦截器

## ZeroRules 的功能

ZeroRules 可以避免在那些 **完全不需要 AI 处理** 的任务上浪费 LLM（大型语言模型）的 tokens。在将查询发送给模型之前，先检查 ZeroRules 是否能够立即完成这些任务，且无需消耗任何 tokens。数学计算、时区查询、货币兑换、文件列表查询以及日期/日程查询等任务都具有确定的答案，且这些操作的成本为 **0**。

**这并非模型路由功能**。模型路由功能会将简单的查询发送给成本更低的模型；而 ZeroRules 会直接跳过模型处理这些任务。

## 何时使用 ZeroRules

当用户的消息符合以下任何一种模式时，**务必首先尝试使用 ZeroRules**：

1. **数学计算**：任何算术运算、百分比计算、单位转换
2. **时间查询**：例如 “东京现在几点了？”、“[时区] 的当前时间是？”
3. **货币兑换**：例如 “将 $X 兑换成 EUR”，“将 [金额] 从 [货币] 兑换成 [目标货币]”
4. **文件操作**：例如 “列出 [目录] 中的文件”，“[文件夹] 里有什么？”
5. **日期/日程查询**：例如 “[日期] 是星期几？”，“距离 [事件] 还有几天？”，“添加会议 [详情]”

## 使用方法

使用 Node.js 和 `exec` 工具运行位于 `{baseDir}/rules.js` 的脚本，并将用户的消息作为参数传递给该脚本：

```bash
node {baseDir}/rules.js "<user message>"
```

### 解释输出结果

脚本会返回 JSON 格式的结果：

- **匹配到规则** → `{"matched": true, "rule": "math", "result": "4446", "saved_tokens_est": 850, "session_total_saved": 12.47}`  
  使用 `result` 值作为回复内容。此时无需调用 LLM。同时显示节省的 tokens 数量：`🔥 ZeroRules | <rule> | ~<saved_tokens_est> 个 tokens 被节省 | 本次会话共节省了 $<session_total_saved>`

- **未匹配到规则** → `{"matched": false}`  
  此时可以正常使用 LLM 进行处理。ZeroRules 不会干扰 LLM 的工作。

### 示例

- 用户输入：**247 × 18 等于多少？**  
  脚本执行：`node {baseDir}/rules.js "247 × 18?"`  
  输出：`{"matched": true, "rule": "math", "result": "4,446", "saved_tokens_est": 850, "session_total_saved": 0.02}`  
  回复：**4,446** 🔥 ZeroRules | 数学计算 | 节省了约 850 个 tokens

- 用户输入：**东京现在几点了？**  
  脚本执行：`node {baseDir}/rules.js "东京现在几点了？」  
  输出：`{"matched": true, "rule": "time", "result": "14:33 JST (Sat Feb 8)", "saved_tokens_est": 1200, "session_total_saved": 0.05}`  
  回复：**14:33 JST (星期六 2月8日)** 🔥 ZeroRules | 时间查询 | 节省了约 1,200 个 tokens

- 用户输入：**将 $100 USD 兑换成 EUR**  
  脚本执行：`node {baseDir}/rules.js "将 $100 USD 兑换成 EUR"`  
  输出：`{"matched": true, "rule": "currency", "result": "€92.34 EUR", "saved_tokens_est": 1500, "session_total_saved": 0.09}`  
  回复：**€92.34 EUR** 🔥 ZeroRules | 货币兑换 | 节省了约 1,500 个 tokens

- 用户输入：**列出 ~/projects 目录中的文件**  
  脚本执行：`node {baseDir}/rules.js "列出 ~/projects 目录中的文件"`  
  输出：`{"matched": true, "rule": "files", "result": "app.js\npackage.json\nREADME.md\nsrc/", "saved_tokens_est": 900, "session_total_saved": 0.11}`  
  回复：列出文件列表。🔥 ZeroRules | 文件操作 | 节省了约 900 个 tokens

- 用户输入：**为第三季度预算审查撰写提案**  
  脚本执行：`node {baseDir}/rules.js "为第三季度预算审查撰写提案"`  
  输出：`{"matched": false}`  
  此时需要使用 LLM 进行创作或推理任务。

## 命令行工具

用户可以输入 `/zero-rules` 或 `/zr` 来查看当前会话的统计信息：  
  脚本执行：`node {baseDir}/rules.js --status`  
  输出：本次会话中匹配到的规则、预估节省的 tokens 数量以及节省的总成本。

用户还可以输入 `/zero-rules test <消息>` 来测试某条消息是否会被 ZeroRules 拦截：  
  脚本执行：`node {baseDir}/rules.js --test "<消息>"`

## 重要行为规则：

1. 对于符合上述模式的查询，**始终优先尝试使用 ZeroRules**。
2. 在将查询传递给 ZeroRules 之前，**切勿修改用户的原始查询内容**。
3. 如果 ZeroRules 返回 `matched: true`，**仅使用其计算结果**，无需再调用 LLM。
4. 如果 ZeroRules 返回 `matched: false`，**则继续使用 LLM**，仿佛 ZeroRules 不存在一样。
5. **每当有规则匹配成功时，务必显示节省的 tokens 数量**，这是用户能够直观看到的价值体现。
6. **文件操作仅在沙箱环境中进行**：ZeroRules 仅列出目录中的文件名（使用 `fs.readdirSync`），不会读取、写入或删除文件内容。
7. **网络请求（仅限于货币兑换功能）** 有 3 秒的超时限制；如果请求失败，会使用静态的备用汇率。

## 安全性与透明度：

- **无 shell 执行**：ZeroRules 不使用 `child_process.exec`、`execSync`、`spawn` 或任何 shell 命令，所有操作都通过安全的 Node.js API 完成。
- **文件操作仅限于读取**：文件列表功能仅使用 `fs.readdirSync` 列出目录中的文件名，不会读取文件内容、写入文件或删除文件。同时禁止路径遍历（如 `..`）操作。
- **路径扩展**：`~` 符号通过 `process.env.HOME`（Node.js 环境变量）进行扩展，而非通过 shell。
- **单次网络请求**：货币兑换功能会通过 `https://api.exchangerate.host` 获取实时汇率；这是整个工具中唯一的网络请求。如果请求失败或超时（3 秒），会使用静态备用汇率。
- **会话状态记录**：会生成一个名为 `~/.zerorules-session.json` 的 JSON 文件，记录每次会话中节省的 tokens 数量。文件中仅包含匹配次数、总节省的 tokens 数量、总节省成本以及一系列 `{rule, timestamp, tokens}` 的记录。**用户的消息、查询内容或输入文本均不会被存储在该文件中**。
- **完全离线使用**：可以通过禁用或跳过货币兑换规则来实现完全离线运行；其他规则均无需网络连接。

## 免费 tier 的限制

ZeroRules 默认提供了 5 个内置规则（数学计算、时间查询、货币兑换、文件操作、日期查询），这些功能都是免费且无使用限制的。

**Pro tier（每月 $9，网址：https://cascadeai.dev/pro）** 提供以下额外功能：  
- 无限数量的自定义规则（支持正则表达式和自定义处理逻辑）  
- 跨会话的持续节省记录  
- 每周通过电子邮件/Telegram 发送费用报告  
- 优先支持

当会话节省的 tokens 超过 $5 时，会显示提示信息：  
`💡 ZeroRules 本次会话为您节省了 $X。解锁无限规则及详细节省记录 → https://cascadeai.dev/pro`